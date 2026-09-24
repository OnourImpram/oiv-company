"""Company-site contract that any design must satisfy. Written before the 2026-09-23 redesign."""
import os
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(os.environ.get("OIV_DOCS") or Path(__file__).resolve().parents[1] / "docs")
PAGES = {"en": ROOT / "index.html", "tr": ROOT / "tr" / "index.html"}
IDENTITY = ["ONOUR IMPRAM VENTURES LTD", "17429906", "235117532", "71-75 Shelton Street",
            "WC2H 9JQ", "onour@onourimpram.com"]
ON_PLAY = {"com.hezarfen.catpulse", "com.hezarfen.dogpulse"}
NOT_ON_PLAY = ["GraceRhythm", "ADHDFlow", "Clocktopus", "Kinlore"]
# Created in Play Console 2026-09-24, not published: listed, never linked to a store.
IN_DEVELOPMENT = ["ManagerGym", "Pathways Lab", "RecallDock", "PlateKind", "Tiny Broadcast",
                  "One Plan Today", "Backlog Bloom"]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.tags, self.text = path, [], []
        self._skip = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)

    def all(self, tag, **kw):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in kw.items())]

    @property
    def body_text(self):
        return re.sub(r"\s+", " ", " ".join(self.text))


class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {lang: Page(p) for lang, p in PAGES.items()}

    def test_identity_facts_visible_in_both_languages(self):
        for lang, p in self.pages.items():
            for fact in IDENTITY:
                self.assertIn(fact, p.body_text, f"{lang}: {fact}")

    def test_lang_canonical_and_alternates(self):
        for lang, p in self.pages.items():
            self.assertEqual(p.all("html")[0].get("lang"), lang)
            canon = p.all("link", rel="canonical")
            self.assertEqual(canon[0]["href"], "https://oiv.onourimpram.com/" + ("" if lang == "en" else "tr/"))
            alts = {a.get("hreflang") for a in p.all("link", rel="alternate")}
            self.assertTrue({"en", "tr"} <= alts, lang)

    def test_one_h1_and_images_described_and_sized(self):
        for lang, p in self.pages.items():
            self.assertEqual(len(p.all("h1")), 1, lang)
            for img in p.all("img"):
                self.assertIn("alt", img, f"{lang}: {img.get('src')}")
                self.assertIn("width", img)
                self.assertIn("height", img)

    def test_store_claims_match_measurement(self):
        # Site-wide: a design may list products on the home page or on a work page.
        site = [Page(f) for f in ROOT.rglob("*.html")]
        play_ids = {re.search(r"id=([a-z0-9._]+)", a["href"]).group(1)
                    for p in site for a in p.all("a") if "play.google.com/store/apps/details" in a.get("href", "")}
        self.assertEqual(play_ids, ON_PLAY)
        for lang in ("en", "tr"):
            text = " ".join(p.body_text for p in site if p.all("html")[0].get("lang") == lang)
            for app in NOT_ON_PLAY + IN_DEVELOPMENT:
                self.assertIn(app, text, f"{lang}: {app} listed")

    def test_no_server_submission_no_third_party_code(self):
        for lang, p in self.pages.items():
            self.assertFalse(p.all("form"), lang)
            csp = p.all("meta", **{"http-equiv": "Content-Security-Policy"})[0]["content"]
            self.assertIn("form-action 'none'", csp)
            self.assertNotIn("unsafe-inline", csp)
            for tag in ("script", "img", "link"):
                for a in p.all(tag):
                    url = a.get("src") or a.get("href") or ""
                    if tag == "link" and a.get("rel") in ("canonical", "alternate"):
                        continue
                    self.assertFalse(urlparse(url).netloc, f"{lang}: external {tag} {url}")

    def test_local_links_and_fragments_resolve(self):
        for lang, p in self.pages.items():
            ids = [a["id"] for _, a in p.tags if "id" in a]
            self.assertEqual(len(ids), len(set(ids)), f"{lang}: duplicate id")
            for _, a in p.tags:
                for key in ("src", "href"):
                    if key not in a:
                        continue
                    u = urlparse(a[key])
                    if u.scheme or u.netloc:
                        continue
                    if not u.path and u.fragment:
                        self.assertIn(unquote(u.fragment), ids, f"{lang}: #{u.fragment}")
                    elif u.path:
                        target = (p.path.parent / unquote(u.path)).resolve()
                        if target.is_dir():
                            target = target / "index.html"
                        self.assertTrue(target.exists(), f"{lang}: {u.path}")

    def test_prose_has_no_em_or_en_dash(self):
        for lang, p in self.pages.items():
            self.assertNotRegex(p.body_text, "[–—]", lang)

    def test_clinical_boundary_stated(self):
        self.assertIn("Clinical practice is separate from the company", self.pages["en"].body_text)
        self.assertIn("Klinik", self.pages["tr"].body_text)

    def test_404_and_fonts_present(self):
        # Design-independent: every font a stylesheet declares is self-hosted and present.
        self.assertTrue((ROOT / "404.html").exists())
        self.assertEqual((ROOT / "CNAME").read_text(encoding="utf-8").strip(), "oiv.onourimpram.com")
        for css in ROOT.rglob("*.css"):
            for url in re.findall(r"@font-face[^}]*?url\(([^)]+)\)", css.read_text(encoding="utf-8")):
                url = url.strip("'\"")
                self.assertFalse(urlparse(url).netloc, f"remote font {url}")
                self.assertTrue((css.parent / url).resolve().exists(), url)


if __name__ == "__main__":
    unittest.main()
