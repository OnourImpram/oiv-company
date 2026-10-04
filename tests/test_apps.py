"""Google Play app pages: a contract for the 23 published apps. Offline, standard library only."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

from expected_apps import APPS

ROOT = Path(__file__).resolve().parents[1] / "docs"
SITE = "https://oiv.onourimpram.com"
EN_DIR, TR_DIR = "apps", "tr/uygulamalar"
# Claims the brief forbids on these pages: ratings, reviews, download counts, awards, superlatives,
# "ad-free" wording and medical promises. Matched on the visible text only.
FORBIDDEN = re.compile(
    r"\b(rating|ratings|rated|reviews?|downloads?|installs?|awards?|award-winning|best|top-rated|ad-free|ads-free|no ads|"
    r"diagnos\w*|treatment|therapy|cure[sd]?)\b|#\s?1\b|reklams[ıi]z|ücretsiz reklamsız|derecelendirme|ödül|en iyi|tedavi|teşhis",
    re.I)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.tags, self.text, self.ld, self._skip, self._ld = path, [], [], [], 0, False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag == "script":
            self._skip += 1
            self._ld = a.get("type") == "application/ld+json"
            self._buf = []
        if tag == "style":
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
            if tag == "script" and self._ld:
                self.ld.append("".join(self._buf))
                self._ld = False

    def handle_data(self, data):
        if self._skip:
            if self._ld:
                self._buf.append(data)
        else:
            self.text.append(data)

    def all(self, tag, **kw):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in kw.items())]

    @property
    def body_text(self):
        return re.sub(r"\s+", " ", " ".join(self.text))


def url_of(rel):
    return SITE + "/" + re.sub(r"(^|/)index\.html$", r"\1", rel)


class AppPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {a["package"]: a for a in json.loads((ROOT.parent / "src/apps.json").read_text(encoding="utf-8"))["apps"]}
        cls.pages = {}
        for pkg, (slug, _name) in APPS.items():
            cls.pages[pkg] = {"en": Page(ROOT / EN_DIR / slug / "index.html"), "tr": Page(ROOT / TR_DIR / slug / "index.html")}

    def test_generator_data_matches_the_measured_package_list(self):
        self.assertEqual(set(self.data), set(APPS))
        for pkg, a in self.data.items():
            self.assertEqual(a["slug"], APPS[pkg][0], pkg)
            self.assertEqual(a["name"], APPS[pkg][1], pkg)
            self.assertTrue((ROOT / "assets/img" / a["image"]).is_file(), a["image"])

    def test_icons_are_real_176_pixel_pngs(self):
        for pkg, a in self.data.items():
            raw = (ROOT / "assets/img" / a["image"]).read_bytes()
            self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n", pkg)
            self.assertEqual(int.from_bytes(raw[16:20], "big"), 176, pkg)
            self.assertEqual(int.from_bytes(raw[20:24], "big"), 176, pkg)

    def test_play_button_is_the_primary_call_to_action(self):
        for pkg, pair in self.pages.items():
            for lang, p in pair.items():
                play = [a["href"] for a in p.all("a") if "play.google.com/store/apps/details" in a.get("href", "")]
                self.assertEqual(play, [f"https://play.google.com/store/apps/details?id={pkg}"], f"{lang} {pkg}")
                button = [a for a in p.all("a") if a.get("class") == "button button-ink"]
                self.assertEqual([a["href"] for a in button], play, f"{lang} {pkg}: first button is not the Play link")

    def test_metadata_canonical_hreflang_and_og(self):
        for pkg, pair in self.pages.items():
            slug = APPS[pkg][0]
            en, tr = url_of(f"{EN_DIR}/{slug}/index.html"), url_of(f"{TR_DIR}/{slug}/index.html")
            for lang, p in pair.items():
                self.assertEqual(p.all("html")[0]["lang"], lang)
                self.assertEqual(p.all("link", rel="canonical")[0]["href"], en if lang == "en" else tr)
                alts = {a["hreflang"]: a["href"] for a in p.all("link", rel="alternate")}
                self.assertEqual(alts, {"en": en, "tr": tr, "x-default": en}, f"{lang} {pkg}")
                og = {a.get("property"): a.get("content") for a in p.all("meta") if a.get("property")}
                self.assertEqual(og["og:url"], en if lang == "en" else tr)
                self.assertTrue(og["og:image"].startswith(SITE + "/"))
                self.assertTrue(og["og:title"] and og["og:description"])
                self.assertEqual(len(p.all("h1")), 1)
                desc = p.all("meta", name="description")[0]["content"]
                self.assertTrue(40 <= len(desc) <= 175, f"{lang} {pkg}: description {len(desc)} chars")

    def test_structured_data_parses_and_is_honest(self):
        for pkg, pair in self.pages.items():
            a = self.data[pkg]
            for lang, p in pair.items():
                blocks = [json.loads(x) for x in p.ld]
                kinds = [b["@type"] for b in blocks]
                self.assertEqual(kinds, ["Organization", "SoftwareApplication", "BreadcrumbList"], f"{lang} {pkg}")
                sa = blocks[1]
                self.assertEqual(sa["name"], a[lang]["title"])
                self.assertEqual(sa["operatingSystem"], "Android")
                self.assertTrue(sa["applicationCategory"])
                self.assertEqual(sa["installUrl"], f"https://play.google.com/store/apps/details?id={pkg}")
                self.assertEqual(sa["publisher"]["name"], "ONOUR IMPRAM VENTURES LTD")
                self.assertEqual(sa["offers"], {"@type": "Offer", "price": "0", "priceCurrency": a["priceCurrency"]})
                self.assertNotIn("aggregateRating", sa)
                self.assertNotIn("review", sa)

    def test_no_forbidden_claims_and_diacritics_survive(self):
        for pkg, pair in self.pages.items():
            for lang, p in pair.items():
                text = p.body_text
                found = FORBIDDEN.search(text)
                self.assertIsNone(found, f"{lang} {pkg}: {found.group(0) if found else ''}")
        # Turkish pages keep their letters: the shared chrome alone carries ç ğ ı ö ş ü İ somewhere on every page.
        for pkg, pair in self.pages.items():
            self.assertTrue(set("çğıöşüİ") & set(pair["tr"].body_text), pkg)

    def test_premium_line_only_when_listing_declares_ads_and_purchases(self):
        for pkg, pair in self.pages.items():
            a = self.data[pkg]
            en = pair["en"].body_text
            self.assertEqual("Free with ads; Premium removes ads." in en, bool(a["ads"] and a["iap"]), pkg)
            tr = pair["tr"].body_text
            self.assertEqual("Premium reklamları kaldırır." in tr, bool(a["ads"] and a["iap"]), pkg)

    def test_privacy_link_resolves_and_is_never_invented(self):
        for pkg, pair in self.pages.items():
            a = self.data[pkg]
            for lang, p in pair.items():
                hrefs = [x["href"] for x in p.all("a") if x.get("class") == "text-link" and x["href"] not in
                         (f"../../work.html#apps", f"../../../work.html#apps")]
                privacy = [h for h in hrefs if "legal/" in h or "yasal/" in h or h == a.get("privacyUrl")]
                self.assertEqual(len(privacy), 1, f"{lang} {pkg}: {hrefs}")
                href = privacy[0]
                if href.startswith("http"):
                    self.assertEqual(href, a["privacyUrl"])
                    self.assertEqual(a["privacyHttp"], 200, pkg)
                else:
                    self.assertTrue((p.path.parent / href / "index.html").resolve().is_file(), f"{lang} {pkg}: {href}")

    def test_work_pages_list_every_app_with_store_and_app_page(self):
        for lang, rel, apps_dir in (("en", "work.html", "apps"), ("tr", "tr/calismalar.html", "uygulamalar")):
            p = Page(ROOT / rel)
            cards = [a for a in p.all("article") if a.get("class") == "app-card"]
            self.assertEqual(len(cards), len(APPS), lang)
            hrefs = [a["href"] for a in p.all("a")]
            for pkg, (slug, name) in APPS.items():
                self.assertIn(f"https://play.google.com/store/apps/details?id={pkg}", hrefs, f"{lang} {pkg}")
                self.assertTrue(any(h.endswith(f"{apps_dir}/{slug}/index.html") for h in hrefs), f"{lang} {slug}")
                self.assertIn(name, p.body_text)
            self.assertNotIn("22 September", p.body_text)
            self.assertNotIn("22 Eylül", p.body_text)
            # The only app still without a store link stays in the workshop list.
            self.assertEqual(len(p.all("span", **{"class": "app-status"})), 1, lang)
            self.assertIn("One Plan Today", p.body_text)

    def test_sitemap_lists_every_app_page_with_alternates(self):
        sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for pkg, (slug, _n) in APPS.items():
            for rel in (f"{EN_DIR}/{slug}/", f"{TR_DIR}/{slug}/"):
                self.assertIn(f"<loc>{SITE}/{rel}</loc>", sm, rel)
        self.assertEqual(sm.count("<loc>"), sm.count("<url>"))
        # Every legal folder on disk is listed, in both languages.
        for kind in ("legal", "tr/yasal"):
            for d in (ROOT / kind).iterdir():
                self.assertIn(f"<loc>{SITE}/{kind}/{d.name}/</loc>", sm, f"{kind}/{d.name}")


if __name__ == "__main__":
    unittest.main()
