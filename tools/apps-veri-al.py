# -*- coding: utf-8 -*-
"""Build src/apps.json, the single content source for the Google Play app pages (2026-10-04).

Inputs
  --olcum  canli-listing-olcumu.json, the measured live Play listing data (title, short description,
           first 250 characters of the long description, category, ads and in-app purchase flags).
  network  one public Play detail page per package (hl=en) for three facts the measurement does not carry:
           the offer price (ld+json), the privacy policy URL listed on Play, and the icon URL.
Output
  src/apps.json     written with sorted, stable keys; every field is a measured value or a documented rule.
  --ikon-indir      also saves the Play icon (176x176 PNG) as docs/assets/img/<slug>.png when that file is missing.
Run:   py -3 tools/apps-veri-al.py --olcum <path> [--ikon-indir]

Rules (nothing is written by hand):
  about    the first paragraph of the long description. The measurement keeps only 250 characters, so a paragraph
           that is cut off is shortened to its last complete sentence. A first paragraph shorter than 80 characters
           (a tagline) is followed by the next complete paragraph that fits inside the 250 characters.
  trAscii  a Turkish paragraph of 60+ characters with no Turkish letter at all is treated as an ASCII-degraded
           store text and is NOT published (the page falls back to the short description).
"""
import argparse
import json
import re
import struct
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}
SLUG = {"com.brilliant.wellbeing": "clocktopus", "com.hezarfen.kinlore.app": "kinlore", "com.hezarfen.managergym": "leadrehearse"}
# Legal pages on this site keep their original slug even where the product was renamed.
LEGAL_SLUG = {"com.hezarfen.managergym": "managergym"}
TR_LETTERS = set("çğıöşüÇĞİÖŞÜ")
CUT = 250


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return r.status, (body if binary else body.decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, (b"" if binary else "")
    except Exception as e:  # network failure is reported, never guessed around
        return -1, (b"" if binary else str(e))


def short_name(title):
    return re.split(r"\s*[:—]\s*", title, maxsplit=1)[0].strip()


def about(long250, short=""):
    """First paragraph(s) of the long description, complete sentences only; never repeats the short description."""
    cut_inside = len(long250) >= CUT
    paras = [p.strip() for p in re.split(r"\n+", long250)]
    complete = paras[:-1] if cut_inside else paras      # the last chunk of a cut text may end mid-word
    out = []
    if paras and not complete:                           # first paragraph itself is cut
        m = list(re.finditer(r"[.!?](?=\s|$)", paras[0]))
        if m:
            out.append(paras[0][: m[-1].end()].strip())
        return out
    for p in complete:
        if not p or p.startswith("•"):
            break
        if p.isupper() or p == short.strip():            # a section heading, or the lead sentence again
            continue
        out.append(p)
        if len(p) >= 80:
            break
    return out


def degraded_tr(paragraphs):
    return any(len(p) >= 60 and not (set(p) & TR_LETTERS) for p in paragraphs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--olcum", required=True)
    ap.add_argument("--ikon-indir", action="store_true")
    a = ap.parse_args()
    m = json.loads(Path(a.olcum).read_text(encoding="utf-8"))
    apps = []
    for pkg, v in m["paketler"].items():
        en, tr = v["en"], v["tr"]
        assert en["yayinda"] and tr["yayinda"], pkg
        slug = SLUG.get(pkg, pkg.split(".")[-1])
        st, h = fetch(f"https://play.google.com/store/apps/details?id={pkg}&hl=en&gl=US")
        assert st == 200, (pkg, st)
        ld = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S)
        offer = (json.loads(ld[0]).get("offers") or [{}])[0] if ld else {}
        pv = re.search(r'aria-label="Privacy Policy (https?://[^ "]+) will open', h)
        pv = pv.group(1) if pv else None
        pv_http = fetch(pv)[0] if pv else None
        og = re.search(r'<meta property="og:image" content="([^"]+)"', h)
        entry = {
            "package": pkg, "slug": slug, "name": short_name(en["baslik"]), "image": f"{slug}.png",
            "legalSlug": LEGAL_SLUG.get(pkg, slug),
            "play": f"https://play.google.com/store/apps/details?id={pkg}",
            "ads": bool(en["reklam_icerir"]), "iap": bool(en["uygulama_ici_satin_alma"]),
            "price": offer.get("price"), "priceCurrency": offer.get("priceCurrency"),
            "privacyUrl": pv if pv_http == 200 else None, "privacyHttp": pv_http,
            "checked": en["okuma_zamani"][:10],
        }
        for lang, d in (("en", en), ("tr", tr)):
            ab = about(d["uzun_aciklama_ilk250"], d["kisa_aciklama_meta"])
            dropped = lang == "tr" and degraded_tr(ab)
            entry[lang] = {"title": d["baslik"], "short": d["kisa_aciklama_meta"], "category": d["kategori"],
                           "about": [] if dropped else ab, "aboutDropped": dropped}
        apps.append(entry)
        if a.ikon_indir and og:
            target = ROOT / "docs" / "assets" / "img" / f"{slug}.png"
            if not target.exists():
                s, b = fetch(og.group(1).split("=")[0] + "=s176", binary=True)
                assert s == 200 and b[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", b[16:24]) == (176, 176), (pkg, s)
                target.write_bytes(b)
                print("icon saved", target.name)
        print(slug, entry["price"], entry["privacyHttp"], len(entry["en"]["about"]), len(entry["tr"]["about"]), "tr-dropped" if entry["tr"]["aboutDropped"] else "")
        time.sleep(0.4)
    apps.sort(key=lambda e: e["name"].lower())
    out = {"_meta": {"measured": m["meta"]["olculdu"], "source": "canli-listing-olcumu.json (live Google Play listing, 23 of 23 published)",
                     "extra": "price, privacy URL and icon read from the public Play page; see tools/apps-veri-al.py"},
           "apps": apps}
    (ROOT / "src" / "apps.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print("apps:", len(apps))


if __name__ == "__main__":
    sys.exit(main())
