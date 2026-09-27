# -*- coding: utf-8 -*-
"""Generate privacy policy + terms pages for the 10 Clocktopus Shipaton apps (2026-09-27).

Template: docs/legal/managergym/index.html (header, footer and head are reused; <main> is rewritten).
Output:  docs/legal/<id>/index.html  (privacy at top, terms at #terms).
Run:     python tools/yasal-sayfa-uret.py            (writes all 10)
         python tools/yasal-sayfa-uret.py --check    (rc=1 if any page is missing or stale)
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "legal" / "managergym" / "index.html"
DATE = "27 September 2026"

APPS = [
    ("tidemind", "TideMind", "a gentle day planner that helps you choose what fits into today"),
    ("glowfox", "GlowFox", "an evening wind-down companion for building a calm night routine"),
    ("bloombyte", "BloomByte", "a practice space for managing notifications and digital attention"),
    ("orbitpal", "OrbitPal", "a focus companion for starting tasks with small, pausable steps"),
    ("mossloop", "MossLoop", "a companion for making room for breaks and support on busy days"),
    ("pulsepatch", "PulsePatch", "a practice space for naming feelings and choosing a coping step"),
    ("nestnote", "NestNote", "a rehearsal space for everyday conversations and personal boundaries"),
    ("pebblepath", "PebblePath", "a small-habits companion that lets you restart without penalties"),
    ("sproutsprint", "SproutSprint", "a companion for accessible movement breaks during the day"),
    ("echoharbor", "EchoHarbor", "a companion for work boundaries, clear requests and rest"),
]


def main_block(pid, name, what):
    e = html.escape
    summary = (f"{name} is {what}. You can use it without an account. Your progress stays on your device. "
               f"The free version shows ads; {name} Premium removes ads and unlocks extra content. We do not sell data.")
    return summary, f"""<main id="main" tabindex="-1"><section class="inner-hero dark section" data-od-id="intro"><div class="container"><div class="breadcrumb"><a href="../../index.html">Home</a><span aria-hidden="true">/</span><span>Privacy and terms</span></div><h1>{e(name)} privacy policy and terms</h1><p class="inner-lead">Effective {DATE}. Google Play package: com.hezarfen.{pid}.</p></div></section><section class="section" data-od-id="policy"><div class="container prose"><h2>In short</h2><p>{e(summary)}</p><h2>Who we are</h2><p>{e(name)} is published by ONOUR IMPRAM VENTURES LTD, a company registered in the United Kingdom under company number 17429906, which is responsible for the personal data described here. Contact: <a href="mailto:onour@onourimpram.com">onour@onourimpram.com</a>.</p><h2>Data that stays on your device</h2><p>Your lesson progress, the entries you create in the app, your language, theme and reminder settings are stored only in the app&#x27;s storage on your device and are not sent to us.</p><h2>Service providers</h2><ul><li><strong>Google AdMob</strong> shows ads in the free version. AdMob may collect your device&#x27;s advertising ID, IP address, device and app information, and ad interaction data to serve, measure and, only with your consent, personalise ads. Consent is requested through Google&#x27;s consent form (User Messaging Platform) where the law requires it, and you can change it in Settings.</li><li><strong>RevenueCat</strong> processes an anonymous app user identifier, purchase state and purchase events so that {e(name)} Premium can be bought and restored through Google Play. Your entries and progress are never sent to RevenueCat.</li><li><strong>Google Play</strong> processes the purchase itself under your Google account.</li></ul><p>Google privacy policy: <a href="https://policies.google.com/privacy">https://policies.google.com/privacy</a>. How Google uses data from partner apps: <a href="https://policies.google.com/technologies/partner-sites">https://policies.google.com/technologies/partner-sites</a>. RevenueCat privacy policy: <a href="https://www.revenuecat.com/privacy">https://www.revenuecat.com/privacy</a>.</p><h2>What we do not do</h2><ul><li>No account, no cloud sync and no analytics service of our own.</li><li>We do not ask for health records, diagnoses or contact lists.</li><li>We do not sell personal data.</li></ul><h2>Permissions</h2><ul><li>Notifications, only if you turn on reminders. Reminders are scheduled on your device.</li><li>Internet and advertising ID, used by the ad and purchase services described above.</li></ul><h2>Your choices and deletion</h2><p>You can reset your data from Settings. Uninstalling the app removes its local data. You can reset or delete your advertising ID in your device settings. Purchase records stay with Google Play and RevenueCat; to ask about those records, email us.</p><h2>Your rights</h2><p>Depending on where you live, you may have rights to access, correct, delete or object to the processing of your personal data. Send requests by email. In the United Kingdom you can also complain to the Information Commissioner&#x27;s Office.</p><h2>Children</h2><p>{e(name)} is intended for adults and is not directed to children under 13.</p><h2 id="terms">Terms of use</h2><ul><li>{e(name)} offers general self-help education and practice tools. It is not medical, psychological or other professional advice, diagnosis or treatment. If you are in crisis, contact your local emergency number or a crisis line in your country.</li><li>{e(name)} Premium is an auto-renewing subscription billed through Google Play. The price and period are shown before you buy. You can cancel at any time in Google Play; access continues until the end of the paid period. Refunds follow Google Play&#x27;s refund policy.</li><li>The app and its content are provided as is. To the extent permitted by law, ONOUR IMPRAM VENTURES LTD is not liable for indirect or consequential loss arising from its use. Nothing in these terms limits rights you have under consumer law.</li><li>These terms are governed by the laws of England and Wales.</li></ul><h2>Changes</h2><p>We update this page before any change to the app&#x27;s data practices is released. The effective date is shown at the top of this page.</p><p class="updated">{DATE} · ONOUR IMPRAM VENTURES LTD</p></div></section></main>"""


def page(tpl, pid, name, what):
    summary, main = main_block(pid, name, what)
    t = re.sub(r"<main id=\"main\".*?</main>", lambda _: main, tpl, flags=re.S)
    title = f"{name} privacy policy and terms | OIV"
    t = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", t)
    t = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"', lambda m: m.group(1) + html.escape(summary) + '"', t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + html.escape(title) + '"', t)
    t = t.replace("/legal/managergym/", f"/legal/{pid}/").replace('data-page="app-managergym"', f'data-page="app-{pid}"')
    t = re.sub(r'<link rel="alternate" hreflang="tr"[^>]*>', "", t)
    t = re.sub(r'<a href="../../tr/yasal/managergym/index.html"[^>]*>TR</a>', "", t)
    t = t.replace("../../legal/managergym/index.html", f"../../legal/{pid}/index.html")
    assert "managergym" not in t.lower(), pid
    return t


def main(argv):
    bad = [a for a in argv if a not in ("--check",)]
    if bad:
        print("unknown flag:", bad[0])
        return 2
    tpl = TEMPLATE.read_text(encoding="utf-8")
    stale = []
    for pid, name, what in APPS:
        out = ROOT / "docs" / "legal" / pid / "index.html"
        want = page(tpl, pid, name, what)
        if "--check" in argv:
            if not out.exists() or out.read_text(encoding="utf-8") != want:
                stale.append(pid)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(want, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
    if "--check" in argv:
        print("STALE/MISSING:", stale or "none")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
