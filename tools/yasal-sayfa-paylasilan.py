# -*- coding: utf-8 -*-
"""Move the shared portfolio policy to the company site as a per-app page (2026-10-26, Addendum 90).

Apps: DogPulse, DoomScroll (same shared policy, same source files). Source: the shared policy that the Play listing links to, https://onourimpram.github.io/portfolio-41/privacy-policy
(EN) and privacy-policy.tr (TR), file docs/privacy-policy.md and docs/privacy-policy.tr.md of OnourImpram/portfolio-41 at commit
74b41b527b733b0d5989c7ffbb6ac75e1b36cb53. Copies: src/paylasilan-politika.en.md and .tr.md. The text is copied verbatim; the only
substitutions are the heading (page title names the app), the address (the files carry {{EMAIL}}, filled from src/content.json)
and markdown -> html. One section is added: "Data deletion" / "Veri silme" with id="data-deletion", made only of sentences already
on the sibling pages (CatPulse "controls").
Languages: EN and TR only. Visibility: the template carries noindex; /legal/ and /yasal/ stay out of the sitemap.
Run:  python tools/yasal-sayfa-paylasilan.py          (writes the two pages)
      python tools/yasal-sayfa-paylasilan.py --check  (rc=1 if stale or missing)
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = {"dogpulse": "DogPulse", "doomscroll": "DoomScroll"}
TEMPLATE = {"en": ROOT / "docs" / "legal" / "managergym" / "index.html", "tr": ROOT / "docs" / "tr" / "yasal" / "managergym" / "index.html"}
SRC = {"en": ROOT / "src" / "paylasilan-politika.en.md", "tr": ROOT / "src" / "paylasilan-politika.tr.md"}
EMAIL = json.loads((ROOT / "src" / "content.json").read_text(encoding="utf-8"))["site"]["email"]
DEL_HEAD = {"en": "Data deletion", "tr": "Veri silme"}
# Verbatim from the CatPulse entry of src/app-privacy.json ("controls"), the same family of apps (backup, restore, reset in Settings).
DEL_TEXT = {
    "en": "You can export, restore or permanently delete your local records from Settings. Deleting local records does not remove records held by RevenueCat, Google Play, Sentry or Google AdMob; to ask about those records, email us.",
    "tr": "Yerel kayıtlarınızı Ayarlar'dan dışa aktarabilir, geri yükleyebilir veya kalıcı olarak silebilirsiniz. Yerel kayıtları silmek RevenueCat, Google Play, Sentry veya Google AdMob'da tutulan kayıtları silmez; bu kayıtlarla ilgili talepleriniz için bize e-posta gönderin.",
}
# DoomScroll (live vc8, read statically from the Play-generated universal APK, 2026-10-26): Settings has "Reset All Data" (confirm text "This will
# permanently delete all data"); the Export/Import rows are gone (settings.tsx comment HUKUM M2). So no export/restore claim. The first sentence
# in each language is NEW (reader list); the second is verbatim from the sibling pages (tinybroadcast, managergym).
DEL_OVERRIDE = {
    "doomscroll": {
        "en": "You can permanently delete all your local data from Settings. Purchase records stay with Google Play and RevenueCat; to ask about those records, email us.",
        "tr": "Yerel verilerinizin tümünü Ayarlar'dan kalıcı olarak silebilirsiniz. Satın alma kayıtları Google Play ve RevenueCat'te kalır; bu kayıtlarla ilgili talepleriniz için bize e-posta gönderin.",
    }
}
# Effective date of the page, per app (Addendum 134 item 3, 2026-10-27): DogPulse's new release takes effect on 27 October 2026, so its page
# says so; the shared source copy keeps 2026-10-26 and DoomScroll's pages keep reading it. One exact substitution per language, asserted.
EFFECTIVE = {
    "dogpulse": {
        "en": ("Effective 2026-10-26.", "Effective 27 October 2026."),
        "tr": ("Yürürlük tarihi 2026-10-26.", "Yürürlük tarihi 27 Ekim 2026."),
    }
}
# Which kind of ads the app requests, per app (Addendum 137 item 2, 2026-10-27). The shared source copy lists six apps as "non-personalised only";
# that is no longer true for DogPulse and CatPulse, and DoomScroll's live and upgrade builds differ, so each page now states only its own app.
# The three npa sentences of the source (the two bullets under "Sent to Google AdMob" and the "Right to withdraw consent" sentence) are
# replaced per page; every other line of the copy is kept. Exact line prefixes are asserted once per language.
#  - DogPulse: the same consent paragraph src/build.py ads_section renders for the other AdMob apps (verbatim; true for the live build and
#    the candidate: ads may be personalised, in the EEA, UK and Switzerland the consent form asks first).
#  - DoomScroll: true for both builds. Live vc8 (rewarded request with requestNonPersonalizedAdsOnly: true, ads.ts:191 at e854b4f where
#    versionCode became 8, ads.ts:226 at e2f7efb, the last commit with the key) and the upgrade tip 2dd8ef3e (request without options,
#    ads.ts:277, comment :274-276) differ, so the page says what holds for both: personalised ads only when Google's consent status allows
#    it; the consent form is shown first (ads.ts:96-97 at e854b4f, :142-143 at the tip); one optional rewarded ad on the game-over screen
#    (SessionSummaryScreen.tsx:62,128), no banner (AdBanner.tsx:15).
BUILD_CONSENT = {
    "en": ("If you are in the European Economic Area, the United Kingdom or Switzerland, the app first shows Google’s consent form (User Messaging Platform) and requests ads only when Google’s consent status allows it. "
           "If you do not agree to personalised ads, Google can still show non personalised ads, which use the same technical data for delivery, frequency limits, reporting and fraud prevention but are not based on your past activity. "
           "Outside these regions ads may be personalised. To change or withdraw your consent, email us; you can reset or delete your advertising ID in Android settings."),
    "tr": ("Avrupa Ekonomik Alanı, Birleşik Krallık veya İsviçre’deyseniz uygulama önce Google’ın User Messaging Platform onay formunu gösterir ve reklamı yalnızca Google’ın onay durumu izin verdiğinde ister. "
           "Kişiselleştirilmiş reklamları kabul etmezseniz Google yine kişiselleştirilmemiş reklamlar gösterebilir; bunlar aynı teknik verileri gösterim, sıklık sınırı, raporlama ve sahtecilik önleme için kullanır ama geçmiş etkinliğinize dayanmaz. "
           "Bu bölgelerin dışında reklamlar kişiselleştirilebilir. Onayınızı değiştirmek veya geri çekmek için bize e-posta gönderin; reklam kimliğinizi Android ayarlarından sıfırlayabilir veya silebilirsiniz."),
}
ADS_BULLET = {
    "dogpulse": {"en": "* **DogPulse: consent decides.** " + BUILD_CONSENT["en"], "tr": "* **DogPulse: onay belirler.** " + BUILD_CONSENT["tr"]},
    "doomscroll": {
        "en": ("* **DoomScroll.** DoomScroll shows one kind of ad: an optional rewarded ad that you start yourself on the game-over screen to earn a hint. It never shows a banner. "
               "Personalised ads are requested only when Google’s consent status allows it. If you are in the European Economic Area, the United Kingdom or Switzerland, "
               "the app first shows Google’s consent form (User Messaging Platform). To change or withdraw your consent, email us."),
        "tr": ("* **DoomScroll.** DoomScroll tek tür reklam gösterir: oyun bitiş ekranında bir ipucu kazanmak için kendiniz başlattığınız, isteğe bağlı bir ödüllü reklam. Hiçbir zaman banner göstermez. "
               "Kişiselleştirilmiş reklamlar yalnızca Google’ın onay durumu izin verdiğinde istenir. Avrupa Ekonomik Alanı, Birleşik Krallık veya İsviçre’deyseniz "
               "uygulama önce Google’ın User Messaging Platform onay formunu gösterir. Onayınızı değiştirmek veya geri çekmek için bize e-posta gönderin."),
    },
}
WITHDRAW = {
    "dogpulse": {"en": "To change or withdraw your consent for personalised ads, email us at **{EMAIL}**.",
                 "tr": "Kişiselleştirilmiş reklamlar için onayınızı değiştirmek veya geri çekmek için **{EMAIL}** adresine e-posta gönderin."},
    "doomscroll": {"en": "In DoomScroll, personalised ads are requested only when Google’s consent status allows it; to change or withdraw your consent, email us at **{EMAIL}**.",
                   "tr": "DoomScroll’da kişiselleştirilmiş reklamlar yalnızca Google’ın onay durumu izin verdiğinde istenir; onayınızı değiştirmek veya geri çekmek için **{EMAIL}** adresine e-posta gönderin."},
}
ADS_PREFIX = {"en": ("* **Only non-personalised ads (", "* **Consent decides (", "In the apps that ask for personalisation consent ("),
              "tr": ("* **Yalnızca kişiselleştirilmemiş reklamlar (", "* **Onay belirler (", "Kişiselleştirme onayı isteyen uygulamalarda (")}
WITHDRAW_TAIL = {"en": " You can stop sending crash reports", "tr": " Mevcut olduğunda Ayarlar"}


def per_app_ads(md, slug, lang):
    if slug not in ADS_BULLET:
        return md
    npa_p, consent_p, withdraw_p = ADS_PREFIX[lang]
    lines = md.split("\n")
    i = [k for k, l in enumerate(lines) if l.startswith(npa_p)]
    j = [k for k, l in enumerate(lines) if l.startswith(consent_p)]
    w = [k for k, l in enumerate(lines) if l.startswith(withdraw_p)]
    assert len(i) == len(j) == len(w) == 1 and j[0] == i[0] + 1, (slug, lang, i, j, w)
    tail = lines[w[0]][lines[w[0]].index(WITHDRAW_TAIL[lang]):]          # raises if the tail sentence is not there
    lines[w[0]] = WITHDRAW[slug][lang].replace("{EMAIL}", EMAIL) + tail   # later line first, so the earlier indices stay valid
    lines[i[0]:j[0] + 1] = [ADS_BULLET[slug][lang]]
    return "\n".join(lines)


CRUMB = {"en": '<a href="../../index.html">Home</a><span aria-hidden="true">/</span><span>Privacy</span>',
         "tr": '<a href="../../../tr/index.html">Ana sayfa</a><span aria-hidden="true">/</span><span>Gizlilik</span>'}
TITLE = {"en": "{n} privacy policy", "tr": "{n} gizlilik politikası"}
SLUG_RE = re.compile(r"[^\w\- ]", re.U)


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


FOLD = str.maketrans("ıçğöşüâî", "icgosuai")


def anchor(t):
    # ASCII-folded, because the shared policy links to #uygulama-kapsami while the heading reads "kapsamı"
    return SLUG_RE.sub("", t.lower().translate(FOLD)).strip().replace(" ", "-")


def md_to_html(md, lang, slug):
    lines = md.replace("\r\n", "\n").split("\n")
    assert lines[0].startswith("# ")
    out, i, para, lst = [], 1, [], None
    used = set()

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            tag = lst[0]
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in lst[1]) + f"</{tag}>")
            lst = None

    # lead = the bold brand line + operator line (the first paragraph after the H1)
    j = 1
    while not lines[j].strip():
        j += 1
    lead = []
    while lines[j].strip():
        lead.append(lines[j].strip()); j += 1
    lead_html = inline(" ".join(lead))
    deleted = False
    for l in lines[j:]:
        m = re.match(r"^(#{2,3}) (.+)$", l)
        if m:
            flush()
            lvl = len(m.group(1))
            if lvl == 2 and m.group(2).startswith(("Changes to this policy", "Bu politikadaki değişiklikler", "Politika değişiklikleri")) and not deleted:
                out.append(f'<h2 id="data-deletion">{DEL_HEAD[lang]}</h2><p>{html.escape(DEL_OVERRIDE.get(slug, DEL_TEXT)[lang], quote=False)}</p>')
                deleted = True
            a = anchor(m.group(2)); base = a; n = 2
            while a in used or a == "data-deletion":
                a = f"{base}-{n}"; n += 1
            used.add(a)
            out.append(f'<h{lvl} id="{a}">{inline(m.group(2))}</h{lvl}>')
        elif re.match(r"^[*-] ", l):
            if not lst or lst[0] != "ul":
                flush(); lst = ("ul", [])
            lst[1].append(l[2:])
        elif re.match(r"^\d+\. ", l):
            if not lst or lst[0] != "ol":
                flush(); lst = ("ol", [])
            lst[1].append(re.sub(r"^\d+\. ", "", l))
        elif l.strip() == "---":
            flush(); out.append("<hr>")
        elif not l.strip():
            flush()
        else:
            if lst:
                lst[1][-1] += " " + l.strip()
            else:
                para.append(l.strip())
    flush()
    if not deleted:
        raise SystemExit("anchor heading for the data-deletion section not found in " + lang)
    return lead_html, "".join(out)


def page(tpl, slug, lang):
    name = SLUGS[slug]
    md = SRC[lang].read_text(encoding="utf-8").replace("{{EMAIL}}", EMAIL)
    if slug in EFFECTIVE:
        old, new = EFFECTIVE[slug][lang]
        assert md.count(old) == 1, (slug, lang, old)
        md = md.replace(old, new)
    md = per_app_ads(md, slug, lang)
    lead, body = md_to_html(md, lang, slug)
    title = TITLE[lang].format(n=name)
    main = (f'<main id="main" tabindex="-1"><section class="inner-hero dark section" data-od-id="intro"><div class="container">'
            f'<div class="breadcrumb">{CRUMB[lang]}</div><h1>{html.escape(title)}</h1><p class="inner-lead">{lead}</p></div></section>'
            f'<section class="section" data-od-id="policy"><div class="container prose">{body}</div></section></main>')
    t = re.sub(r"<main id=\"main\".*?</main>", lambda _: main, tpl, flags=re.S)
    full = html.escape(title + " | OIV")
    first = re.search(r"<p>(.*?)</p>", body).group(1)
    desc = html.escape(re.sub(r"<[^>]+>", "", html.unescape(first)))
    t = re.sub(r"<title>.*?</title>", lambda _: f"<title>{full}</title>", t)
    t = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"', lambda m: m.group(1) + desc + '"', t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + full + '"', t)
    t = t.replace("/legal/managergym/", f"/legal/{slug}/").replace("/tr/yasal/managergym/", f"/tr/yasal/{slug}/")
    t = t.replace('data-page="app-managergym"', f'data-page="app-{slug}"')
    assert "managergym" not in t.lower()
    return t


def main(argv):
    if [a for a in argv if a != "--check"]:
        print("unknown flag")
        return 2
    tpl = {l: p.read_text(encoding="utf-8") for l, p in TEMPLATE.items()}
    stale = []
    for slug in SLUGS:
        for lang, rel in (("en", Path("docs/legal") / slug), ("tr", Path("docs/tr/yasal") / slug)):
            out = ROOT / rel / "index.html"
            want = page(tpl[lang], slug, lang)
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
