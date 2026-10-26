# -*- coding: utf-8 -*-
"""Move three policy pages from the founder's personal site to the company site (2026-10-26).

Apps: ADHDFlow, GraceRhythm, Kinlore. Source text: src/tasinan-legal.json, the card text of the personal-site pages
(https://onourimpram.com/legal/<slug>/<lang>), copied verbatim; only the Cloudflare-obfuscated address link was replaced by its
decoded value, which equals the company address; the data file carries {{EMAIL}} and this tool fills it from src/content.json (site.email).
Added: one deletion-request sentence per language, copied from the existing oiv sibling pages (tinybroadcast, managergym).
Languages: the sibling sentence exists in English and Turkish only, so only EN and TR are produced here. The other 17 languages
of the personal pages are not produced (a new translation of the sentence is not allowed).
Template: docs/legal/managergym and docs/tr/yasal/managergym (head, header, footer). Visibility follows src/build.py is_legal:
the template carries noindex, the sitemap skips /legal/ and /yasal/, and no home or navigation link is added.
Output: docs/legal/<slug>/index.html and docs/tr/yasal/<slug>/index.html (privacy first, terms at #terms).
Run:    python tools/yasal-sayfa-tasi.py            (writes the pages of SLUGS)
        python tools/yasal-sayfa-tasi.py --check    (rc=1 if any page is missing or stale)
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = {"en": ROOT / "docs" / "legal" / "managergym" / "index.html",
            "tr": ROOT / "docs" / "tr" / "yasal" / "managergym" / "index.html"}
SRC = ROOT / "src" / "tasinan-legal.json"
SITE_EMAIL = json.loads((ROOT / "src" / "content.json").read_text(encoding="utf-8"))["site"]["email"]   # the address is never written into the data file
SLUGS = ("adhdflow", "gracerhythm", "kinlore")
# 2026-10-26 ruling (revenubrain): GraceRhythm TR "Dua ettiğin ... reklam yoktur" and Kinlore EN "collects no personal data" were replaced
# verbatim by the sibling pages' Google data lines (src/build.py ads_section), so canli-iddia gives rc 0; everything else stays verbatim.
# Verbatim from the sibling pages (src/app-privacy.json, tinybroadcast and managergym, "controls" field).
DELETION = {
    "en": "Purchase records stay with Google Play and RevenueCat; to ask about those records, email us.",
    "tr": "Satın alma kayıtları Google Play ve RevenueCat'te kalır; bu kayıtlarla ilgili talepleriniz için bize e-posta gönderin.",
}
CHROME = {
    "en": ('<a href="../../index.html">Home</a><span aria-hidden="true">/</span><span>Privacy and terms</span>', "Privacy and terms"),
    "tr": ('<a href="../../../tr/index.html">Ana sayfa</a><span aria-hidden="true">/</span><span>Gizlilik ve koşullar</span>', ""),
}


def card_html(c, with_sentence, lang):
    inner = c["html"]
    if with_sentence:
        assert inner.count("</p>") >= 1
        inner = inner + f"<p>{html.escape(DELETION[lang], quote=False)}</p>"
    return f"<h3>{c['h']}</h3>{inner}"


def main_block(slug, lang, d):
    x = d[slug][lang]
    p, t = x["privacy"], x["terms"]
    # The deletion sentence goes into the privacy "Contact" card (the last privacy card), next to the address.
    last = len(p["cards"]) - 1
    priv = "".join(card_html(c, i == last, lang) for i, c in enumerate(p["cards"]))
    terms = "".join(card_html(c, False, lang) for c in t["cards"])
    crumb = CHROME[lang][0]
    title = x["title"]
    return (f'<main id="main" tabindex="-1"><section class="inner-hero dark section" data-od-id="intro"><div class="container">'
            f'<div class="breadcrumb">{crumb}</div><h1>{title}</h1><p class="inner-lead">{p["sub"]}</p></div></section>'
            f'<section class="section" data-od-id="policy"><div class="container prose"><h2 id="privacy">{p["h1"]}</h2>{priv}'
            f'<h2 id="terms">{t["h1"]}</h2><p>{t["sub"]}</p>{terms}<p>{x["fine"]}</p></div></section></main>'), title


def page(tpl, slug, lang, d):
    main, title = main_block(slug, lang, d)
    t = re.sub(r"<main id=\"main\".*?</main>", lambda _: main, tpl, flags=re.S)
    full = html.escape(re.sub(r"<[^>]+>", "", title) + " | OIV")
    first = re.search(r"<p>(.*?)</p>", d[slug][lang]["privacy"]["cards"][0]["html"]).group(1)
    desc = html.escape(re.sub(r"<[^>]+>", "", first))
    t = re.sub(r"<title>.*?</title>", lambda _: f"<title>{full}</title>", t)
    t = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"', lambda m: m.group(1) + desc + '"', t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + full + '"', t)
    t = t.replace("/legal/managergym/", f"/legal/{slug}/").replace("/tr/yasal/managergym/", f"/tr/yasal/{slug}/")
    t = t.replace('data-page="app-managergym"', f'data-page="app-{slug}"')
    assert "managergym" not in t.lower(), slug
    return t


def main(argv):
    bad = [a for a in argv if a != "--check"]
    if bad:
        print("unknown flag:", bad[0])
        return 2
    d = json.loads(SRC.read_text(encoding="utf-8").replace("{{EMAIL}}", SITE_EMAIL))
    tpl = {l: p.read_text(encoding="utf-8") for l, p in TEMPLATE.items()}
    stale = []
    for slug in SLUGS:
        for lang, rel in (("en", Path("docs/legal") / slug), ("tr", Path("docs/tr/yasal") / slug)):
            out = ROOT / rel / "index.html"
            want = page(tpl[lang], slug, lang, d)
            if "--check" in argv:
                if not out.exists() or out.read_text(encoding="utf-8") != want:
                    stale.append(str(rel / "index.html"))
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(want, encoding="utf-8", newline="\n")
            print("wrote", rel / "index.html")
    if "--check" in argv:
        print("STALE/MISSING:", stale or "none")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
