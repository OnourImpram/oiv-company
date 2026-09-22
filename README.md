# oiv-company

ONOUR IMPRAM VENTURES LTD, kurumsal site (EN + TR). Statik, derleme adımı yok:
`index.html`, `tr/index.html`, `assets/style.css`, `assets/fonts.css`. Yollar
görelidir, yani site hem proje sayfası adresinde hem özel alan adında çalışır.

## Tasarım kararı

Konsept, ana sitenin (onourimpram.com) iki dünya kimliğinin kardeşidir ve onu
yapı olarak alır. Sahne evin hero grameridir: iki yanda dev başlık, ortada bir
nesne; evde nesne bir portre, burada şirketin işareti. Altında iki oda yan
yana: gece odası (açık kaynak, araştırma, değerlendirme) ve gündüz odası
(uygulamalar, danışmanlık, yayıncılık).

İmza dikiştir: işaretin altından doğar, siyah künye şeridinin altından geçer,
iki odanın arasından iner ve sicil bandının kuralında logodaki elmasla aynı
bir düğümde biter. Tipografi evin "tek aile, iki ses" kuralıdır: Fraunces gece
tarafında keskin (opsz 144, SOFT 0), gündüz tarafında yumuşak (opsz 32, SOFT
80); gövde IBM Plex Sans, tanımlayıcılar IBM Plex Mono. Takımyıldız ve botanik
dokular ev sitesinin kendi SVG sanatından üretildi (`assets/art/`).

## Fontlar

Fontlar yerel olarak gömülüdür (`assets/fonts/`, latin + latin-ext alt
kümeleri; Türkçe harfler latin-ext'tedir). Lisans: SIL Open Font License 1.1,
üç ailenin kanonik OFL.txt metni `assets/fonts/OFL.txt` içinde. Önceki sürüm
Google Fonts'tan yüklüyordu ve istek URL'si HTTP 400 dönüyordu; o sürüm hiçbir
zaman ev fontlarıyla görünmedi.

## Neden var

Samsung, Galaxy Store kurumsal satıcı başvurusunu 2026-09-21'de reddetti. Dört
gerekçeden ikisi satıcı e-postasının alan adıyla şirketin resmî sitesinin alan
adının eşleşmesini istiyor. Bu sayfa o site: tescilli unvan, şirket numarası,
D-U-N-S, kayıtlı ofis, yönetici, iletişim ve şirketin yayımladığı yazılımlar.

## İçerik kuralı

Sayfadaki her olgu kaynağında ölçülmüştür. Uygulama rafı ölçülen durumu söyler:
"On Google Play" herkese açık mağaza sayfası 200 dönen uygulamalardır; "Submitted
to Google Play" Play Developer API'de production sürümü bulunan ama herkese açık
sayfası henüz açılmamış olanlardır. Bir uygulamanın durumu değişince raf
yeniden ölçülür.

## Özel alan adı

`CNAME.bekliyor` hedef adresi tutar (`oiv.onourimpram.com`). DNS kaydı
açıldıktan sonra dosya `CNAME` olarak yeniden adlandırılır:
Cloudflare, onourimpram.com, CNAME `oiv`, hedef `onourimpram.github.io`, proxy
kapalı (DNS only; sertifikayı GitHub kessin). O ana kadar site proje sayfası
adresinden yayındadır.

## Yayın öncesi ölçülenler (2026-09-22, son düzenlemeden sonra)

- Yatay taşma: 320, 360, 390, 768, 1024, 1440 px, iki dil, 12 koşumda 0.
- Metin kontrastı piksel üzerinden (metin saydam yapılıp gerçek zemin
  okunarak, zeminin 5. ve 95. yüzdeliğine karşı): 1440 ve 390 px, iki dil,
  düşen rol 0, en düşüğü 4,96 (mobilde sol kicker, eşik 4,5).
- Bağlantı alt çizgisi metne bağlı (text-decoration), kural kontrastı 2,68 ile
  2,86 arası.
- Fontlar tarayıcıda yüklendi olarak doğrulandı (Fraunces, Plex Sans, Plex
  Mono); negatif kol: eski Google Fonts URL'siyle sıfır yüz yüklendi.
- Dikiş sürekliliği dört birleşimde 0,00 px.
- Azaltılmış harekette animasyon yok; dokunma hedefi 24 px altı yok.
- Dış bağlantılar: 16 bağlantının hepsi 200 (yönlendirme izlenerek).
- Odak halkası: klavyeyle 39 durakta zemine karşı en düşük 5,91.
- axe-core WCAG A/AA: iki dil, masaüstü ve mobil, 0 ihlal.
- Uzun tire taraması temiz.

Her kolun negatif kontrolü aynı koşumda ateşledi (kasıtlı düşük kontrast,
bozuk font URL'si, bilinen 404, zemine yakın odak halkası).
