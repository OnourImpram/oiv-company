# oiv-company

ONOUR IMPRAM VENTURES LTD, kurumsal site (EN + TR). Statik, derleme adımı yok:
`index.html`, `tr/index.html`, `assets/style.css`, `assets/apps/*.png`. Yollar
görelidir, yani site hem proje sayfası adresinde hem özel alan adında çalışır.

## Tasarım kararı

Konsept, ana sitenin (onourimpram.com) iki dünya kimliğinin kardeşidir: gece
tarafı atölyedir, orada yapılan işler durur; altın bir dikiş geçer; gündüz
tarafı kayıttır, sicil orada yazılıdır. Metafor değiştirilmedi, şirkete
uyarlandı.

Tipografi ev fontlarıdır: Fraunces (display), IBM Plex Sans (gövde), IBM Plex
Mono (tanımlayıcılar). İmgelem uydurma değil, kendi ürettiğimiz uygulama
ikonlarıdır.

## Neden var

Samsung, Galaxy Store kurumsal satıcı başvurusunu 2026-09-21'de reddetti. Dört
gerekçeden ikisi satıcı e-postasının alan adıyla şirketin resmî sitesinin alan
adının eşleşmesini istiyor. Bu sayfa o site: tescilli unvan, şirket numarası,
D-U-N-S, kayıtlı ofis, yönetici, iletişim ve şirketin yayımladığı yazılımlar.

## Özel alan adı

`CNAME.bekliyor` hedef adresi tutar (`oiv.onourimpram.com`). DNS kaydı
açıldıktan sonra dosya `CNAME` olarak yeniden adlandırılır:
Cloudflare, onourimpram.com, CNAME `oiv`, hedef `onourimpram.github.io`, proxy
kapalı (DNS only; sertifikayı GitHub kessin). O ana kadar site proje sayfası
adresinden yayındadır.

## Yayın öncesi ölçülenler

320, 360, 390, 768, 1024 ve 1440 pikselde yatay taşma yok. axe-core WCAG A/AA
iki dilde sıfır serious/critical. On metin katmanının kontrastı piksel üzerinden
ölçüldü, en düşüğü 6.20. Uzun tire taraması temiz
(`06-Altyapi/scripts/uzun-tire-kapisi.py`).
