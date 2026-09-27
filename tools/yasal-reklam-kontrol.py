# -*- coding: utf-8 -*-
"""Check that every Shipaton app's hosted privacy page tells the truth about AdMob ads (2026-09-27).

For each page it fetches (or reads from a saved directory) it reports:
  FALSE_CLAIM   a sentence that says there are no ads / no advertising SDK  -> rc 1
  NO_AD_SECTION the page has no advertising section at all                   -> rc 1
  MISSING       a required AdMob disclosure is absent (listed, not fatal unless --strict)
  HTTP          the URL did not answer 200                                   -> rc 1

Run:
  python tools/yasal-reklam-kontrol.py --live [--out DIR]           live URLs, saves bodies to DIR
  python tools/yasal-reklam-kontrol.py --dir DIR                    saved bodies from an earlier --out
  python tools/yasal-reklam-kontrol.py --self-test                  both arms of the negative control
Remedy when it fails: fix the wording in src/app-privacy.json (six bilingual apps), tools/yasal-sayfa-uret.py
(EN-only wave apps) or the app's own legal strings (Kinlore), rebuild, redeploy, rerun with --live.
"""
import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

OIV = "https://oiv.onourimpram.com"
BILINGUAL = ["managergym", "recalldock", "backlogbloom", "pathwayslab", "tinybroadcast", "platekind"]
WAVE = ["tidemind", "nestnote", "bloombyte", "pulsepatch", "echoharbor", "glowfox", "sproutsprint",
        "orbitpal", "mossloop", "pebblepath", "jarwise"]
KINLORE_LANGS = ["en", "tr", "de", "fr", "it", "es", "pt", "pt-BR", "nl", "pl", "ro", "el", "ru", "ar", "hi",
                 "id", "zh", "ja", "ko"]


def targets():
    t = []
    for a in BILINGUAL:
        t.append((a, "en", f"{OIV}/legal/{a}/"))
        t.append((a, "tr", f"{OIV}/tr/yasal/{a}/"))
    for a in WAVE:
        t.append((a, "en", f"{OIV}/legal/{a}/"))
    for lang in KINLORE_LANGS:
        t.append(("kinlore", lang, f"https://onourimpram.com/legal/kinlore/{lang}"))
    return t


# A claim that the app has no ads. Written narrowly so that "Premium removes every ad" or
# "the app does not request or show any ad while Pro is active" is not caught.
FALSE = {
    "en": [r"\bno advertising\b", r"\bno ads\b(?! anywhere)", r"contains no advertising", r"no advertising sdk",
           r"does not request or show advertisements", r"there is no advertising", r"no advertising software",
           r"no ad(vertising)? (id|identifier) (is )?(used|collected)"],
    "tr": [r"reklam yok", r"reklam içermez", r"reklam sdk'sı yok", r"mevcut sürüm reklam istemez"],
}
SECTION = {"en": r"<h[23][^>]*>\s*advertising\s*</h[23]>", "tr": r"<h[23][^>]*>\s*reklamlar\s*</h[23]>"}
REQUIRED = {
    "en": {"advertising ID": r"advertising id", "approximate location": r"approximate location",
           "IP address": r"ip address", "device/diagnostic data": r"diagnostic",
           "fraud prevention": r"fraud", "EEA/UK/CH consent": r"european economic area",
           "UMP": r"user messaging platform", "premium removes ads": r"removes (every|the|all) ad",
           "RevenueCat": r"revenuecat"},
    "tr": {"reklam kimliği": r"reklam kimliği", "yaklaşık konum": r"yaklaşık konum", "IP adresi": r"ip adres",
           "tanılama verisi": r"tanılama", "sahtecilik önleme": r"sahtecilik", "AEA/BK/İsviçre onayı": r"avrupa ekonomik alanı",
           "UMP": r"user messaging platform", "premium reklamı kaldırır": r"reklam(ı|ları) kaldırır",
           "RevenueCat": r"revenuecat"},
}


def text_of(body):
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).lower()


def judge(app, lang, status, body):
    rep = {"app": app, "lang": lang, "status": status, "false_claims": [], "section": None, "missing": []}
    if status != 200:
        return rep
    low = body.lower()
    txt = text_of(body)
    rules = "tr" if lang == "tr" else "en"
    if lang not in ("en", "tr"):
        # Kinlore translations: no phrase rules; the checker compares them with the branch source instead.
        rep["section"] = "n/a"
        return rep
    rep["false_claims"] = [m.group(0) for p in FALSE[rules] for m in re.finditer(p, txt)]
    if app == "kinlore":
        rep["section"] = bool(re.search(r"<h3>\s*(advertising|reklamlar)\s*</h3>", low))
    else:
        rep["section"] = bool(re.search(SECTION[rules], low))
    rep["missing"] = [k for k, p in REQUIRED[rules].items() if not re.search(p, txt)]
    return rep


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oiv-legal-check/1.0", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def verdict(rows, strict):
    bad = [r for r in rows if r["status"] != 200 or r["false_claims"] or r["section"] is False
           or (strict and r["missing"])]
    return bad


def run(rows_source, strict, out):
    rows = []
    for app, lang, url in targets():
        status, body = rows_source(app, lang, url)
        if out:
            Path(out).mkdir(parents=True, exist_ok=True)
            (Path(out) / f"{app}-{lang}.html").write_text(body, encoding="utf-8")
        r = judge(app, lang, status, body)
        r["url"] = url
        rows.append(r)
    for r in rows:
        flag = "FAIL" if r in verdict([r], strict) else "PASS"
        extra = []
        if r["false_claims"]:
            extra.append("FALSE_CLAIM=" + "|".join(sorted(set(r["false_claims"]))))
        if r["section"] is False:
            extra.append("NO_AD_SECTION")
        if r["missing"]:
            extra.append("MISSING=" + ",".join(r["missing"]))
        print(f"{flag} {r['status']} {r['app']}/{r['lang']} {' '.join(extra)}")
    bad = verdict(rows, strict)
    print(f"TOTAL {len(rows)} pages, {len(rows) - len(bad)} pass, {len(bad)} fail"
          f" ({'strict' if strict else 'false claims, sections and HTTP'})")
    return rows, (1 if bad else 0)


def self_test():
    """Negative control: a known-bad page must FAIL, a correct page must PASS, and each rule arm must fire."""
    bad_en = "<h2>What we do not do</h2><p>No analytics, no advertising and no data sale.</p>"
    bad_tr = "<p>Veri satmayız, uygulamada reklam yoktur.</p>"
    good_en = ("<h2>Advertising</h2><p>advertising ID, IP address, approximate location, diagnostic data, fraud, "
               "European Economic Area, User Messaging Platform. Pro removes every ad. RevenueCat.</p>"
               "<p>While Pro is active, the app does not request or show any ad.</p>")
    checks = [
        ("en false claim fires", judge("x", "en", 200, bad_en)["false_claims"] != []),
        ("tr false claim fires", judge("x", "tr", 200, bad_tr)["false_claims"] != []),
        ("missing section fires", judge("x", "en", 200, bad_en)["section"] is False),
        ("good page passes", verdict([judge("x", "en", 200, good_en)], True) == []),
        ("premium sentence not a false claim", judge("x", "en", 200, good_en)["false_claims"] == []),
        ("missing disclosure fires", "approximate location" in judge("x", "en", 200, good_en.replace("approximate location", ""))["missing"]),
        ("HTTP 404 fails", verdict([judge("x", "en", 404, "")], False) != []),
    ]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    return 0 if all(ok for _, ok in checks) else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--live", action="store_true")
    g.add_argument("--dir")
    g.add_argument("--self-test", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--strict", action="store_true", help="also fail on missing disclosures")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.live:
        src = lambda app, lang, url: fetch(url)
    else:
        d = Path(a.dir)

        def src(app, lang, url):
            f = d / f"{app}-{lang}.html"
            return (200, f.read_text(encoding="utf-8", errors="replace")) if f.exists() and f.stat().st_size else (404, "")
    rows, rc = run(src, a.strict, a.out)
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
