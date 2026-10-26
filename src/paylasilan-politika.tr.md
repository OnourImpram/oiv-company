# Gizlilik Politikası

**Hezarfen Mobil Portföyü**
ONOUR IMPRAM VENTURES LTD tarafından işletilmektedir. Son güncelleme 2026-10-26. Yürürlük tarihi 2026-10-26.

Bu gizlilik politikası, Hezarfen Mobil Portföyü markası altında yayımlanan her mobil uygulama için geçerlidir. Portföy şu anda 41 uygulamadan oluşmaktadır. Tam liste aşağıdaki [Uygulama kapsamı](#uygulama-kapsami) bölümündedir. Her uygulama burada açıklanan uygulamalara uyar.

## Hızlı özet

Bir Hezarfen uygulamasını kullanırken ürettiğiniz verilerin çoğu cihazınızdan hiç ayrılmaz. Uygulamalar çevrimdışı öncelikli kullanım için tasarlanmıştır. Kayıtlar, skorlar ve ayarlar telefonunuzda yerel bir SQLite veritabanında yaşar. Hesap sistemi yoktur. Kişisel verilerinizi saklayan, bizim işlettiğimiz bir sunucu yoktur.

Bir uygulamanın reklam destekli sürümünü kullandığınızda Google AdMob, reklam sunabilmek için bir reklam tanımlayıcısı alır. Bir premium yükseltme satın aldığınızda RevenueCat, anonim bir işlem kaydı alır. Uygulama çöktüğünde Sentry, çökme raporunu alır. Bu üçüncü tarafların hiçbiri bizden e-postanızı, adınızı veya telefon numaranızı almaz.

BlockZen ve StroopSprint, Sentry'ye çökme raporu göndermez; bu uygulamaların çökme ve performans verileri Google Play Console'daki Android vitals üzerinden gelir.

## İşletmeci ve iletişim

Bu portföydeki her uygulamanın işletmecisi, Birleşik Krallık'ta 17429906 şirket numarasıyla kayıtlı ONOUR IMPRAM VENTURES LTD'dir. Şirket, uygulamaları Hezarfen Mobil Portföyü markası altında yayımlar ve bu politikada açıklanan kişisel verilerden sorumludur.

Gizlilik soruları, veri erişim talepleri veya silme talepleri için **{{EMAIL}}** adresine "Privacy request" konu satırı ve sorduğunuz uygulamanın adı ile yazın. Otuz gün içinde yanıt vereceğiz. AB sakinleri için bu adres aynı zamanda GDPR veri sahibi haklarının da kullanıldığı yoldur. Kaliforniya sakinleri için bu adres CCPA taleplerinin yoludur.

## Uygulama kapsamı

Bu politika aşağıdaki tüm Hezarfen uygulamalarını kapsar.

### Hayvan ve bitki bakım uygulamaları (21)

aqualog, beepulse, birdpulse, bonsaipulse, carnivorouslog, catpulse, chickencoop, compostlog, curepulse, dogpulse, exopetpulse, farmpulse, fermentpulse, ferretcare, horsepulse, insectlog, mushroomlog, plantpulse, reptilelog, rodentpulse, turtlepond.

### Günlük mini oyunlar (20)

blockzen, catstack, colorsort, doomscroll, dotdash, dropmerge, emojislide, gridrecall, habitloop, impostortest, mergemood, onelink, perfectstop, reflexring, shapematch, speedtap, stroopsprint, tapbalance, vibecheck, wordblitz.

Bu politikayı, yukarıdaki listelerde görünmeyen bir uygulamanın uygulama mağazası ilanından okuyorsanız, o uygulama bu portföyün parçası değildir ve bu politika ona uygulanmaz.

## Topladığımız veriler

### Yalnızca cihazınızda yerel olarak saklanır

Her Hezarfen uygulaması, `expo-sqlite` kütüphanesi aracılığıyla gömülü bir SQLite veritabanı kullanır. Uygulama içinde oluşturduğunuz her şey, siz silene kadar cihazınızdaki bu veritabanında yaşar.

Yerel SQLite veritabanında yaşayan veri türleri uygulamaya göre değişir ve şunları içerebilir.

* Oluşturduğunuz bakım kayıtları (besleme zamanları, sulama programları, veteriner ziyaretleri, notlar).
* Etkinlik kayıtları (sayımlar, gözlemler, eklediğiniz fotoğraflar).
* Oyun ilerlemesi (en yüksek skorlar, seviye tamamlama durumu, seriler, ayarlar).
* Kullanıcı tercihleri (tema, dil, bildirim anahtarları).

Bu veritabanından asla okumayız. Uzak yedeğimiz yoktur. Uygulamayı kaldırırsanız, telefonunuzun kendi yedekleme özelliğini (Google Drive Backup, iCloud) kullanmadıysanız bu veri gider, bu da bizim kontrolümüz dışındadır.

### Google AdMob'a gönderilir (yalnızca reklam destekli sürümlerde)

Bir Hezarfen uygulamasının reklam destekli bir sürümünü kullanıyorsanız Google AdMob SDK etkindir. AdMob şunları alır.

* Android reklam tanımlayıcınız veya App Tracking Transparency aracılığıyla izlemeye izin verdiğinizde iOS reklam tanımlayıcınız.
* Google'ın IP adresinizden türettiği yaklaşık coğrafi bölge.
* Standart cihaz meta verileri (işletim sistemi sürümü, uygulama sürümü, ekran boyutu).

Bu veri, size hangi reklamın gösterileceğini seçmek için kullanılır. Bu veriyi biz asla görmeyiz. O noktada Google'ın gizlilik uygulamaları geçerlidir. Ayrıntılar için [Google'ın Reklam Politikaları](https://policies.google.com/technologies/ads) ve [Google, hizmetlerimizi kullanan site veya uygulamalardan gelen bilgileri nasıl kullanır](https://policies.google.com/technologies/partner-sites) bağlantılarına bakın.

Bir uygulamanın ne tür reklamlar isteyeceği uygulamaya bağlıdır:

* **Yalnızca kişiselleştirilmemiş reklamlar (BlockZen, StroopSprint, AquaLog, CatPulse, DogPulse, DoomScroll).** Bu uygulamaların Google Play hedef kitlesi 18 yaşın altındaki kullanıcıları içerir. Bu uygulamaların her biri, her kullanıcı için ve her bölgede yalnızca kişiselleştirilmemiş reklamlar ister. Kişiselleştirilmiş reklamlar hiçbir zaman istenmediğinden, sizden kişiselleştirme onayı istenmez ve bunu reddetmeniz gerekmez.
* **Onay belirler (18 yaş ve üzeri yetişkinlere yönelik olan CarnivorousLog ve yukarıdaki listelerde yer alıp bir önceki maddede adı geçmeyen diğer tüm uygulamalar).** Avrupa Ekonomik Alanında, Birleşik Krallık ve İsviçre'de, ilk açılışta size kişiselleştirilmiş reklamları reddetmenize olanak tanıyan bir onay ekranı gösterilir. Seçiminizi uygulama içinde Ayarlar, AdMob tercihleri yolundan istediğiniz zaman değiştirebilirsiniz. Seçiminiz aynı zamanda AdMob'a iletilir.

### RevenueCat'e gönderilir (yalnızca premium yükseltme satın aldığınızda)

Premium yükseltme için bir satın alma düğmesine dokunursanız RevenueCat fatura doğrulamasını yönetir. RevenueCat şunları alır.

* Sizinle ilişkilendirmediğimiz rastgele bir anonim tanımlayıcı (`$RCAnonymousID`, kurulum başına üretilir).
* Google Play veya App Store işlem makbuzunuz (satın almayı doğrulamak için gereklidir).
* Satın aldığınız mağazadan türetilen ülkeniz.

RevenueCat adınızı, e-postanızı veya başka bir tanımlayıcıyı **almaz**. Daha sonra bir iade talebi ile bizimle iletişime geçerseniz, eşleştirebilmemiz için Google Play veya App Store hesabınızdan işlem kimliğini isteyeceğiz. Size ulaşmamız için başka bir arama yolumuz yoktur.

RevenueCat'in gizlilik uygulamaları [revenuecat.com/privacy](https://www.revenuecat.com/privacy) adresinde açıklanmıştır.

### Sentry'e gönderilir (yalnızca çökme durumunda)

BlockZen ve StroopSprint, Sentry'ye çökme raporu göndermez; bu uygulamaların çökme ve performans verileri Google Play Console'daki Android vitals üzerinden gelir.

Uygulama çökerse veya iç bir hataya yakalanırsa `@sentry/react-native` kütüphanesi hatayı Frankfurt (AB) veri bölgesindeki Sentry'e raporlar. Sentry şunları alır.

* Çökmenin kodda nerede gerçekleştiğini açıklayan bir yığın izi.
* Çökmeye giden anonim kırıntılar (son altmış saniyede hangi ekranları açtığınız, hangi düğmelere dokunduğunuz).
* Standart cihaz meta verileri (işletim sistemi sürümü, uygulama sürümü, cihaz modeli).
* Uygulamayı her yeniden yüklediğinizde sıfırlanan rastgele üretilmiş bir kurulum kimliği.

Adınızı, e-postanızı, konumunuzu veya uygulamaya yazdığınız hiçbir şeyi bilinçli olarak **göndermeyiz**. Kırıntılar, serbest metin yüklerini kaldıran bir `beforeSend` filtresi tarafından temizlenir.

Çökme raporları ve teşhisler (çökme analitiği), hataları belirlememize ve düzeltmemize yardımcı olur. Doksan gün saklanır ve sonra silinir. Sentry'nin gizlilik uygulamaları [sentry.io/privacy](https://sentry.io/privacy/) adresinde açıklanmıştır.

### Expo'ya gönderilir (yalnızca Hezarfen build altyapısı)

Uygulamaları Expo'nun EAS Build hizmetinde derliyoruz. Expo, derleme sırasında ona gönderdiğimiz kaynak kodu ve bir derleme çıktısını alır. Expo, uygulamayı kullandığınızda verilerinizi **almaz**. Expo ilişkisi yalnızca bizimle (geliştirici) Expo (derleme hizmeti) arasındadır, sizinle Expo arasında değildir.

### Yerel ayar ve saat dilimi (`expo-localization` üzerinden)

Uygulamalar, tarihleri biçimlendirmek ve doğru çeviriyi seçmek için telefonunuzun seçili dilini ve saat diliminizi okur. Bu, işletim sisteminizden yerel olarak okunur. Hiçbir yere **gönderilmez**. Buradaki en yakın veri kategorisi "konum" değil "yerel ayar"dır.

## Açıkça toplamadığımız veriler

Bir uygulama, isteme anında size açıkça söylemediği sürece, hiçbir Hezarfen uygulaması aşağıdaki verilerden hiçbirini toplamaz. Bir uygulama veri kategorisini kullanıyorsa, uygulama içi istem size tam olarak nedenini söyler ve reddedebilirsiniz.

* Kesin coğrafi konum (GPS yok, ince konum izni istenmez).
* Kişi listeniz.
* Arama geçmişiniz.
* SMS geçmişiniz.
* Apple Health veya Google Fit'ten sağlık veya fitness verisi.
* Biyometrik veri.
* Mikrofon sesi.
* Bir uygulama girişine kendiniz eklediğiniz fotoğraflar dışında kamera görüntüleri, bu fotoğraflar da yerel SQLite'ta kalır.

## Üçüncü taraflar

Yukarıda açıklandığı gibi veri alabilecek üçüncü tarafların tam listesi şudur.

* **Google AdMob**, reklam destekli sürümlerde reklam için. [Google'ın gizlilik politikası](https://policies.google.com/privacy).
* **RevenueCat**, uygulama içi satın alma fatura doğrulaması için. [RevenueCat'in gizlilik politikası](https://www.revenuecat.com/privacy).
* **Sentry**, AB bölgesinde çökme raporlaması için. [Sentry'nin gizlilik politikası](https://sentry.io/privacy/).
* **Expo**, derleme ve güncelleme altyapısı için (kullanıcıya yönelik değil). [Expo'nun gizlilik politikası](https://expo.dev/privacy).

Verilerinizi kimseye satmıyoruz. Verilerinizi reklam veri komisyoncularıyla paylaşmıyoruz. Kişiselleştirilmiş reklamlar isteyen uygulamalarda AdMob'un reklam kişiselleştirmesi için yaptığı dışında (yukarıdaki "Google AdMob'a gönderilenler" bölümüne bakın) çapraz uygulama veya çapraz cihaz takibi kullanmıyoruz; bunu da bu uygulamalarda reddedebilirsiniz.

## Haklarınız

### Avrupa Birliği, Birleşik Krallık, İsviçre (GDPR)

Hakkınızda tuttuğumuz kişisel verilere erişme, düzeltme, taşıma ve silme hakkına sahipsiniz. Uygulamada, neredeyse her şey cihazınızda kaldığı için "hakkınızda tuttuğumuz veri" esasen sıfırdır. İstisnalar şunlardır.

1. Google AdMob tarafından tutulan reklam tanımlayıcısı ve reklam sunum kayıtları. Bu kayıtlara karşı haklarınızı kullanmak için [Google'ın Reklam Gizliliği](https://policies.google.com/technologies/ads) kanallarını kullanarak doğrudan Google ile iletişime geçin.
2. RevenueCat tarafından tutulan işlem makbuzu. Bu kayıtlara karşı haklarınızı kullanmak için işlem kimliği ile bizimle iletişime geçin, silme talebini ileteceğiz.
3. Sentry tarafından tutulan çökme raporları. Çökme raporları doksan gün sonra otomatik olarak silinir. Daha erken silme talebi için çökmenin zaman damgası ve telefon modelinizle bizimle iletişime geçin, eşleşen olayları temizleyeceğiz.

Ayrıca yerel veri koruma otoritenize şikâyette bulunma hakkına sahipsiniz.

### Kaliforniya (CCPA / CPRA)

Sahip olduğumuz kişisel bilgileri öğrenme, silme, düzeltme ve herhangi bir satış veya paylaşımdan çıkma hakkına sahipsiniz. CCPA anlamında verilerinizi satmıyor veya paylaşmıyoruz. Yukarıdaki istisnalar (Google, RevenueCat, Sentry) hâlâ geçerlidir.

### Onayı geri çekme hakkı

Kişiselleştirme onayı isteyen uygulamalarda ("Google AdMob'a gönderilenler" altındaki "Onay belirler" grubu), kişiselleştirilmiş reklamlar için onayınızı uygulamanın Ayarlar ekranındaki AdMob tercihleri bölümünden istediğiniz zaman geri çekebilirsiniz. BlockZen, StroopSprint, AquaLog, CatPulse, DogPulse ve DoomScroll bu onayı istemez ve yalnızca kişiselleştirilmemiş reklamlar ister, bu nedenle bunlarda geri çekilecek bir şey yoktur. Mevcut olduğunda Ayarlar'daki "Tanılama dışı bırakma" seçeneğini etkinleştirerek çökme raporlarını göndermeyi durdurabilirsiniz.

## Çocukların gizliliği

Bu portföydeki uygulamalar **13 yaş ve üzeri kullanıcılar için** derecelendirilmiştir. 13 yaş altı çocuklardan bilerek kişisel bilgi toplamayız. Ebeveyn veya vasi iseniz ve 13 yaş altı bir çocuğun bir Hezarfen uygulaması kullandığına ve veri toplandığına inanıyorsanız {{EMAIL}} adresinden bizimle iletişime geçin, eşleşen kayıtları en iyi gayret esasına göre temizleyeceğiz. Her şey cihazda kaldığı için en güvenilir kaldırma yolu uygulamayı kaldırmaktır.

Uygulamalar, uygulanabilir olduğunda Google Play'in Aileler için Tasarlandı programı yönergelerine ve Apple'ın Çocuklar Kategorisi yönergelerine uyar, ancak mağaza ilanı bunu açıkça söylemediği sürece bu programlara kayıtlı değildir.

## Uluslararası veri aktarımları

AdMob, RevenueCat ve Expo'ya yönlendirilen veriler Amerika Birleşik Devletleri'nde veya diğer bölgesel veri merkezlerinde işlenebilir. Sentry çökme raporları AB'de (Frankfurt) işlenir. Aktarımların gerçekleştiği yerlerde Standart Sözleşme Hükümlerine (SCC) ve sağlayıcıların kendi veri aktarım mekanizmalarına dayanıyoruz.

## Güvenlik

Yerel SQLite veritabanları işletim sisteminin uygulama korumalı alanı tarafından korunur. Uygulama katmanında varsayılan olarak şifrelenmezler, dolayısıyla kilidi açılmış bir cihaza fiziksel erişimi olan kararlı bir saldırgan onları okuyabilir. Bunu hafifletmek için telefonunuzun ekran kilidini kullanın.

Aktarımdaki veriler için AdMob, RevenueCat, Sentry ve Expo'ya yapılan her bağlantı TLS 1.2 veya daha yüksek ile HTTPS kullanır.

## Bu politikadaki değişiklikler

Bu politikayı değiştirdiğimizde en üstteki "Son güncelleme" tarihini güncelleriz. Önemli değişiklikler (topladığımız veriyi veya alanları genişleten herhangi bir değişiklik), değişiklikten sonraki ilk açılışta uygulama içi bir bildirim tetikler. Bu politikanın eski sürümleri, GitHub deposunun commit geçmişi incelenerek bu URL'den erişilebilir. Depo herkese açıktır.

## İletişim

E-posta: **{{EMAIL}}**

Gizlilik talepleri için konu satırı: "Privacy request - [uygulama adı]".

Posta adresi (yalnızca yasal olarak gerekli olduğunda kullanılır): e-posta ile talep edildiğinde sağlanır.

---

Bu belge statik içerik olarak yayımlanır. Kanonik, makine tarafından okunabilir kopya https://onourimpram.github.io/portfolio-41/privacy-policy adresindedir. Diğer her kopya türevdir ve güncel olmayabilir.
