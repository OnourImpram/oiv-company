# -*- coding: utf-8 -*-
"""Generate privacy policy + terms pages for the 10 Clocktopus Shipaton apps (2026-09-27).

Template: docs/legal/managergym/index.html (header, footer and head are reused; <main> is rewritten).
Output:  docs/legal/<id>/index.html and docs/tr/yasal/<id>/index.html (privacy at top, terms at #terms).
         The Turkish template is docs/tr/yasal/managergym/index.html.
Run:     python tools/yasal-sayfa-uret.py            (writes all 10)
         python tools/yasal-sayfa-uret.py --check    (rc=1 if any page is missing or stale)
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "legal" / "managergym" / "index.html"
TEMPLATE_TR = ROOT / "docs" / "tr" / "yasal" / "managergym" / "index.html"
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
# Money apps get their own wording for stored data, what we never ask for, and the first term (2026-09-27, JarWise).
FINANCE_APPS = [
    ("jarwise", "JarWise", "an offline envelope-budgeting app that splits your monthly money into visual jars"),
]
FINANCE = {
    "progress": "Your budget stays on your device.",
    "extra": "extra features",
    "stored": ("Your income, jars, expenses, notes, month history, recurring entries, currency, language, theme and "
               "reminder settings are stored only in the app&#x27;s storage on your device and are not sent to us. "
               "JSON and CSV backups you export are not encrypted; you choose where to share them."),
    "never": "<li>We do not connect to banks and never ask for bank logins, card numbers or account numbers.</li>",
    "first_term": ("{n} is a personal budgeting tool. It does not provide financial, investment, tax, credit or legal "
                   "advice, it does not connect to bank accounts and it does not move money. Decisions about your "
                   "money remain yours."),
}


# Advertising section, same Google data lines as src/build.py ads_section (2026-09-27). Inserted before
# "What we do not do" so the page names every AdMob disclosure the Play Data safety form declares.
def ads_block(name, kind="selfhelp"):
    keep = "Your budget entries" if kind == "finance" else "Your entries and progress"
    paras = [
        f"The free version of {name} shows ads from Google AdMob. {name} Premium removes every ad: while Premium is "
        "active, the app does not request or show any ad.",
        "To show, measure and limit ads and to prevent fraud, the Google Mobile Ads SDK collects the following and "
        "shares it with Google: your device&#x27;s advertising ID; your IP address, from which Google derives an "
        "approximate location; device and app information such as model, operating system, language and app version; "
        "diagnostic data such as crash and performance logs; and which ads you were shown and whether you tapped them. "
        "Google uses this data for advertising, analytics and fraud prevention under its own privacy policy.",
        "If you are in the European Economic Area, the United Kingdom or Switzerland, the app first shows Google&#x27;s "
        "consent form (User Messaging Platform) and requests ads only when Google&#x27;s consent status allows it. If you "
        "do not agree to personalised ads, Google can still show non personalised ads, which use the same technical data "
        "for delivery, frequency limits, reporting and fraud prevention but are not based on your past activity. Outside "
        "these regions ads may be personalised.",
        f"{keep} are never sent to AdMob or to any advertiser.",
    ]
    return "<h2>Advertising</h2>" + "".join(f"<p>{p}</p>" for p in paras)


def main_block(pid, name, what, kind="selfhelp"):
    e = html.escape
    fin = kind == "finance"
    summary = (f"{name} is {what}. You can use it without an account. "
               + (FINANCE["progress"] if fin else "Your progress stays on your device.")
               + f" The free version shows ads; {name} Premium removes ads and unlocks "
               + (FINANCE["extra"] if fin else "extra content") + ". We do not sell data.")
    stored = FINANCE["stored"] if fin else ("Your lesson progress, the entries you create in the app, your language, theme and reminder "
                                            "settings are stored only in the app&#x27;s storage on your device and are not sent to us.")
    never = FINANCE["never"] if fin else "<li>We do not ask for health records, diagnoses or contact lists.</li>"
    first_term = (e(FINANCE["first_term"].format(n=name)) if fin else
                  f"{e(name)} offers general self-help education and practice tools. It is not medical, psychological or other "
                  "professional advice, diagnosis or treatment. If you are in crisis, contact your local emergency number or a "
                  "crisis line in your country.")
    return summary, f"""<main id="main" tabindex="-1"><section class="inner-hero dark section" data-od-id="intro"><div class="container"><div class="breadcrumb"><a href="../../index.html">Home</a><span aria-hidden="true">/</span><span>Privacy and terms</span></div><h1>{e(name)} privacy policy and terms</h1><p class="inner-lead">Effective {DATE}. Google Play package: com.hezarfen.{pid}.</p></div></section><section class="section" data-od-id="policy"><div class="container prose"><h2>In short</h2><p>{e(summary)}</p><h2>Who we are</h2><p>{e(name)} is published by ONOUR IMPRAM VENTURES LTD, a company registered in the United Kingdom under company number 17429906, which is responsible for the personal data described here. Contact: <a href="mailto:onour@onourimpram.com">onour@onourimpram.com</a>.</p><h2>Data that stays on your device</h2><p>{stored}</p><h2>Service providers</h2><ul><li><strong>Google AdMob</strong> shows ads in the free version. AdMob may collect your device&#x27;s advertising ID, IP address, device and app information, and ad interaction data to serve, measure and, only with your consent, personalise ads. Consent is requested through Google&#x27;s consent form (User Messaging Platform) where the law requires it, and you can change it in Settings.</li><li><strong>RevenueCat</strong> processes an anonymous app user identifier, purchase state and purchase events so that {e(name)} Premium can be bought and restored through Google Play. Your entries and progress are never sent to RevenueCat.</li><li><strong>Google Play</strong> processes the purchase itself under your Google account.</li></ul><p>Google privacy policy: <a href="https://policies.google.com/privacy">https://policies.google.com/privacy</a>. How Google uses data from partner apps: <a href="https://policies.google.com/technologies/partner-sites">https://policies.google.com/technologies/partner-sites</a>. RevenueCat privacy policy: <a href="https://www.revenuecat.com/privacy">https://www.revenuecat.com/privacy</a>.</p><h2>What we do not do</h2><ul><li>No account, no cloud sync and no analytics service of our own.</li>{never}<li>We do not sell personal data.</li></ul><h2>Permissions</h2><ul><li>Notifications, only if you turn on reminders. Reminders are scheduled on your device.</li><li>Internet and advertising ID, used by the ad and purchase services described above.</li></ul><h2>Your choices and deletion</h2><p>You can reset your data from Settings. Uninstalling the app removes its local data. You can reset or delete your advertising ID in your device settings. Purchase records stay with Google Play and RevenueCat; to ask about those records, email us.</p><h2>Your rights</h2><p>Depending on where you live, you may have rights to access, correct, delete or object to the processing of your personal data. Send requests by email. In the United Kingdom you can also complain to the Information Commissioner&#x27;s Office.</p><h2>Children</h2><p>{e(name)} is intended for adults and is not directed to children under 13.</p><h2 id="terms">Terms of use</h2><ul><li>{first_term}</li><li>{e(name)} Premium is an auto-renewing subscription billed through Google Play. The price and period are shown before you buy. You can cancel at any time in Google Play; access continues until the end of the paid period. Refunds follow Google Play&#x27;s refund policy.</li><li>The app and its content are provided as is. To the extent permitted by law, ONOUR IMPRAM VENTURES LTD is not liable for indirect or consequential loss arising from its use. Nothing in these terms limits rights you have under consumer law.</li><li>These terms are governed by the laws of England and Wales.</li></ul><h2>Changes</h2><p>We update this page before any change to the app&#x27;s data practices is released. The effective date is shown at the top of this page.</p><p class="updated">{DATE} · ONOUR IMPRAM VENTURES LTD</p></div></section></main>"""


def page(tpl, pid, name, what, kind="selfhelp"):
    summary, main = main_block(pid, name, what, kind)
    assert main.count("<h2>What we do not do</h2>") == 1, pid
    main = main.replace("<h2>What we do not do</h2>", ads_block(name, kind) + "<h2>What we do not do</h2>")
    t = re.sub(r"<main id=\"main\".*?</main>", lambda _: main, tpl, flags=re.S)
    title = f"{name} privacy policy and terms | OIV"
    t = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", t)
    t = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"', lambda m: m.group(1) + html.escape(summary) + '"', t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + html.escape(title) + '"', t)
    t = t.replace("/legal/managergym/", f"/legal/{pid}/").replace('data-page="app-managergym"', f'data-page="app-{pid}"')
    t = t.replace("/tr/yasal/managergym/", f"/tr/yasal/{pid}/")
    assert "managergym" not in t.lower(), pid
    return t


# Turkish pages (2026-09-27): same facts as the English page, written as Turkish, not translated line by line.
TR_WHAT = {
    "tidemind": "bugüne neyin sığacağını seçmenize yardım eden sakin bir gün planlayıcısıdır",
    "glowfox": "sakin bir gece rutini kurmanız için akşamları size eşlik eden bir uygulamadır",
    "bloombyte": "bildirimleri ve dijital dikkatinizi yönetmeyi denediğiniz bir alıştırma alanıdır",
    "orbitpal": "işlere küçük ve istediğiniz an durdurabileceğiniz adımlarla başlamanızı kolaylaştıran bir odak arkadaşıdır",
    "mossloop": "yoğun günlerde mola ve destek için yer açmanıza yardım eden bir uygulamadır",
    "pulsepatch": "duygularınızı adlandırıp bir baş etme adımı seçtiğiniz bir alıştırma alanıdır",
    "nestnote": "gündelik konuşmaları ve kişisel sınırlarınızı prova ettiğiniz bir alandır",
    "pebblepath": "ceza olmadan yeniden başlamanıza izin veren küçük alışkanlıklar uygulamasıdır",
    "sproutsprint": "gün içinde herkesin yapabileceği hareket molaları öneren bir uygulamadır",
    "echoharbor": "iş sınırları, açık talepler ve dinlenme konusunda size eşlik eden bir uygulamadır",
    "jarwise": "aylık paranızı görsel kavanozlara bölen, çevrimdışı çalışan bir zarf bütçesi uygulamasıdır",
}
TR_DATE = "27 Eylül 2026"


def tr_ads_block(name, kind="selfhelp"):
    keep = "Bütçe kayıtlarınız" if kind == "finance" else "Girdileriniz ve ilerlemeniz"
    paras = [
        f"{name} uygulamasının ücretsiz sürümü Google AdMob reklamları gösterir. {name} Premium bütün reklamları "
        "kaldırır: Premium etkinken uygulama hiçbir reklam istemez ve göstermez.",
        "Google Mobile Ads SDK, reklamları göstermek, ölçmek ve sınırlamak ve sahteciliği önlemek için şu verileri "
        "toplar ve Google ile paylaşır: cihazınızın reklam kimliği; Google&#x27;ın yaklaşık konum çıkardığı IP "
        "adresiniz; cihaz modeli, işletim sistemi, dil ve uygulama sürümü gibi cihaz ve uygulama bilgileri; çökme ve "
        "performans kayıtları gibi tanılama verileri; size hangi reklamların gösterildiği ve onlara dokunup "
        "dokunmadığınız. Google bu verileri reklamcılık, analiz ve sahtecilik önleme amacıyla kendi gizlilik "
        "politikası kapsamında kullanır.",
        "Avrupa Ekonomik Alanı, Birleşik Krallık veya İsviçre&#x27;deyseniz uygulama önce Google&#x27;ın onay formunu "
        "(User Messaging Platform) gösterir ve reklamı yalnızca Google&#x27;ın onay durumu izin verdiğinde ister. "
        "Kişiselleştirilmiş reklamları kabul etmezseniz Google yine kişiselleştirilmemiş reklam gösterebilir; bu "
        "reklamlar aynı teknik verileri gösterim, sıklık sınırı, raporlama ve sahtecilik önleme için kullanır ama "
        "geçmiş etkinliğinize dayanmaz. Bu bölgelerin dışında reklamlar kişiselleştirilebilir.",
        f"{keep} AdMob&#x27;a ya da herhangi bir reklamverene hiçbir zaman gönderilmez.",
    ]
    return "<h2>Reklamlar</h2>" + "".join(f"<p>{p}</p>" for p in paras)


def tr_main_block(pid, name, kind="selfhelp"):
    e = html.escape
    fin = kind == "finance"
    summary = (f"{name}, {TR_WHAT[pid]}. Hesap açmadan kullanabilirsiniz. "
               + ("Bütçeniz cihazınızda kalır." if fin else "İlerlemeniz cihazınızda kalır.")
               + f" Ücretsiz sürümde reklam gösterilir; {name} Premium reklamları kaldırır ve "
               + ("ek özellikleri" if fin else "ek içerikleri") + " açar. Veri satmayız.")
    stored = ("Gelirleriniz, kavanozlarınız, harcamalarınız, notlarınız, ay geçmişiniz, tekrarlayan kayıtlarınız, para "
              "birimi, dil, tema ve hatırlatıcı ayarlarınız yalnızca cihazınızdaki uygulama depolamasında tutulur ve bize "
              "gönderilmez. Dışa aktardığınız JSON ve CSV yedekleri şifrelenmez; kiminle paylaşacağınıza siz karar "
              "verirsiniz." if fin else
              "Ders ilerlemeniz, uygulamada oluşturduğunuz girdiler, dil, tema ve hatırlatıcı ayarlarınız yalnızca "
              "cihazınızdaki uygulama depolamasında tutulur ve bize gönderilmez.")
    never = ("<li>Bankalara bağlanmayız; banka giriş bilgilerinizi, kart ya da hesap numaralarınızı asla istemeyiz.</li>"
             if fin else "<li>Sağlık kaydı, tanı ya da rehber bilgisi istemeyiz.</li>")
    first_term = (f"{e(name)} kişisel bir bütçe aracıdır. Finansal, yatırım, vergi, kredi ya da hukuki danışmanlık vermez, "
                  "banka hesaplarına bağlanmaz ve para transferi yapmaz. Paranızla ilgili kararlar size aittir." if fin else
                  f"{e(name)} genel öz yardım bilgisi ve alıştırma araçları sunar. Tıbbi, psikolojik ya da başka bir "
                  "profesyonel tavsiye, tanı veya tedavi yerine geçmez. Kriz içindeyseniz bulunduğunuz ülkenin acil "
                  "yardım numarasını ya da bir kriz hattını arayın.")
    return summary, f"""<main id="main" tabindex="-1"><section class="inner-hero dark section" data-od-id="intro"><div class="container"><div class="breadcrumb"><a href="../../../tr/index.html">Ana sayfa</a><span aria-hidden="true">/</span><span>Gizlilik ve koşullar</span></div><h1>{e(name)} gizlilik politikası ve kullanım koşulları</h1><p class="inner-lead">Yürürlük tarihi: {TR_DATE}. Google Play paket kimliği: com.hezarfen.{pid}.</p></div></section><section class="section" data-od-id="policy"><div class="container prose"><h2>Kısaca</h2><p>{e(summary)}</p><h2>Kimiz</h2><p>{e(name)} uygulamasını, Birleşik Krallık&#x27;ta 17429906 şirket numarasıyla kayıtlı ONOUR IMPRAM VENTURES LTD yayımlar ve burada anlatılan kişisel verilerin sorumlusudur. İletişim: <a href="mailto:onour@onourimpram.com">onour@onourimpram.com</a>.</p><h2>Cihazınızda kalan veriler</h2><p>{stored}</p><h2>Hizmet sağlayıcılar</h2><ul><li><strong>Google AdMob</strong> ücretsiz sürümde reklam gösterir. AdMob, reklamları sunmak, ölçmek ve yalnızca onayınız varsa kişiselleştirmek için cihazınızın reklam kimliğini, IP adresinizi, cihaz ve uygulama bilgilerini ve reklam etkileşim verilerini toplayabilir. Yasanın gerektirdiği yerlerde onay, Google&#x27;ın onay formuyla (User Messaging Platform) istenir ve bu tercihi Ayarlar&#x27;dan değiştirebilirsiniz.</li><li><strong>RevenueCat</strong>, {e(name)} Premium&#x27;un Google Play üzerinden satın alınabilmesi ve geri yüklenebilmesi için anonim bir uygulama kullanıcı kimliğini, satın alma durumunu ve satın alma olaylarını işler. Girdileriniz ve ilerlemeniz RevenueCat&#x27;e hiçbir zaman gönderilmez.</li><li><strong>Google Play</strong> satın alma işleminin kendisini Google hesabınız kapsamında işler.</li></ul><p>Google gizlilik politikası: <a href="https://policies.google.com/privacy">https://policies.google.com/privacy</a>. Google&#x27;ın iş ortağı uygulamalardan gelen verileri nasıl kullandığı: <a href="https://policies.google.com/technologies/partner-sites">https://policies.google.com/technologies/partner-sites</a>. RevenueCat gizlilik politikası: <a href="https://www.revenuecat.com/privacy">https://www.revenuecat.com/privacy</a>.</p><h2>Yapmadıklarımız</h2><ul><li>Hesap yok, bulut eşitleme yok, kendimize ait bir analitik hizmeti yok.</li>{never}<li>Kişisel veri satmayız.</li></ul><h2>İzinler</h2><ul><li>Bildirimler, yalnızca hatırlatıcıları açarsanız. Hatırlatıcılar cihazınızda planlanır.</li><li>İnternet ve reklam kimliği; yukarıda anlatılan reklam ve satın alma hizmetleri tarafından kullanılır.</li></ul><h2>Seçimleriniz ve silme</h2><p>Verilerinizi Ayarlar&#x27;dan sıfırlayabilirsiniz. Uygulamayı kaldırmak yerel verilerini de siler. Reklam kimliğinizi cihaz ayarlarından sıfırlayabilir veya silebilirsiniz. Satın alma kayıtları Google Play ve RevenueCat&#x27;te kalır; bu kayıtlarla ilgili sorularınız için bize e-posta gönderin.</p><h2>Haklarınız</h2><p>Bulunduğunuz yerin veri koruma kurallarına göre kişisel verilerinize erişme, düzeltme, silme ve işlenmesine itiraz etme haklarınız olabilir. Taleplerinizi e-postayla iletin. Birleşik Krallık&#x27;ta Information Commissioner&#x27;s Office&#x27;e şikâyette de bulunabilirsiniz.</p><h2>Çocuklar</h2><p>{e(name)} yetişkinler için tasarlanmıştır ve 13 yaşın altındaki çocuklara yönelik değildir.</p><h2 id="terms">Kullanım koşulları</h2><ul><li>{first_term}</li><li>{e(name)} Premium, Google Play üzerinden faturalandırılan ve kendiliğinden yenilenen bir aboneliktir. Fiyat ve dönem satın almadan önce gösterilir. Aboneliği Google Play&#x27;den istediğiniz zaman iptal edebilirsiniz; erişiminiz ödenmiş dönemin sonuna kadar sürer. İadeler Google Play&#x27;in iade politikasına tabidir.</li><li>Uygulama ve içeriği olduğu gibi sunulur. Yasanın izin verdiği ölçüde ONOUR IMPRAM VENTURES LTD, kullanımdan doğan dolaylı zararlardan sorumlu değildir. Bu koşulların hiçbiri tüketici mevzuatından doğan haklarınızı sınırlamaz.</li><li>Bu koşullar İngiltere ve Galler hukukuna tabidir.</li></ul><h2>Değişiklikler</h2><p>Uygulamanın veri uygulamalarındaki bir değişiklik yayımlanmadan önce bu sayfayı güncelleriz. Yürürlük tarihi sayfanın başında yer alır.</p><p class="updated">{TR_DATE} · ONOUR IMPRAM VENTURES LTD</p></div></section></main>"""


def tr_page(tpl, pid, name, kind="selfhelp"):
    summary, main = tr_main_block(pid, name, kind)
    assert main.count("<h2>Yapmadıklarımız</h2>") == 1, pid
    main = main.replace("<h2>Yapmadıklarımız</h2>", tr_ads_block(name, kind) + "<h2>Yapmadıklarımız</h2>")
    t = re.sub(r"<main id=\"main\".*?</main>", lambda _: main, tpl, flags=re.S)
    title = f"{name} gizlilik politikası ve kullanım koşulları | OIV"
    t = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", t)
    t = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"', lambda m: m.group(1) + html.escape(summary) + '"', t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + html.escape(title) + '"', t)
    t = t.replace("/legal/managergym/", f"/legal/{pid}/").replace("/tr/yasal/managergym/", f"/tr/yasal/{pid}/")
    t = t.replace('data-page="app-managergym"', f'data-page="app-{pid}"')
    assert "managergym" not in t.lower(), pid
    return t


def main(argv):
    bad = [a for a in argv if a not in ("--check",)]
    if bad:
        print("unknown flag:", bad[0])
        return 2
    tpl = TEMPLATE.read_text(encoding="utf-8")
    tpl_tr = TEMPLATE_TR.read_text(encoding="utf-8")
    stale = []
    for pid, name, what, kind in [(*a, "selfhelp") for a in APPS] + [(*a, "finance") for a in FINANCE_APPS]:
        for out, want in [(ROOT / "docs" / "legal" / pid / "index.html", page(tpl, pid, name, what, kind)),
                          (ROOT / "docs" / "tr" / "yasal" / pid / "index.html", tr_page(tpl_tr, pid, name, kind))]:
            if "--check" in argv:
                if not out.exists() or out.read_text(encoding="utf-8") != want:
                    stale.append(str(out.relative_to(ROOT)))
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            # newline="\n": the repository stores LF (.gitattributes eol=lf); Windows text mode would write CRLF.
            out.write_text(want, encoding="utf-8", newline="\n")
            print("wrote", out.relative_to(ROOT))
    if "--check" in argv:
        print("STALE/MISSING:", stale or "none")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
