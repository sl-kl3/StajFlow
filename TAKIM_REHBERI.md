# StajFlow — 5 Kişilik Takım Rehberi

> Bu dosya sunuma hazırlanmak içindir.  
> Herkes **kendi bölümünü** okusun, ezberlesin, bilgisayarda **canlı göstersin**.

---

## İçindekiler

1. [Proje ne? (Herkes okusun)](#1-proje-ne-herkes-okusun)
2. [Basit sözlük — terimler ne demek?](#2-basit-sözlük--terimler-ne-demek)
3. [Kim ne yaptı? (Görev dağılımı)](#3-kim-ne-yaptı-görev-dağılımı)
4. [Salih — rehberin](#4-salih--rehberin)
5. [Mine — rehberin](#5-mine--rehberin)
6. [Nazlı — rehberin](#6-nazlı--rehberin)
7. [Zuhal — rehberin](#7-zuhal--rehberin)
8. [İlknur — rehberin](#8-ilknur--rehberin)
9. [Sunum sırası (10–12 dakika)](#9-sunum-sırası-1012-dakika)
10. [Hocanın sorabileceği sorular ve cevaplar](#10-hocanın-sorabileceği-sorular-ve-cevaplar)
11. [Sunumdan 1 gün önce kontrol listesi](#11-sunumdan-1-gün-önce-kontrol-listesi)

---

## 1. Proje ne? (Herkes okusun)

**StajFlow**, üniversitede staj işlerini takip eden bir **web sitesi**.

3 tür kullanıcı var:

| Rol | Kim? | Ne yapar? |
|-----|------|-----------|
| **Öğrenci** | Staj yapacak öğrenci | Profil doldurur, ilana başvurur, günlük yazar |
| **Danışman** | Hoca / akademik danışman | Başvuruyu onaylar, günlüğü onaylar, puan verir |
| **Admin** | Bölüm yetkilisi | Kullanıcı, şirket, staj ilanı ekler |

**Demo giriş bilgileri** (sunumda kullanın):

- Admin: `admin@staj.edu.tr` / `admin123`
- Danışman: `danisman@staj.edu.tr` / `danisman123`
- Öğrenci: `ogr@staj.edu.tr` / `ogr123`

**Projeyi çalıştırmak:**

```
pip install -r requirements.txt
python setup_db.py
python app.py
```

Tarayıcıda: http://127.0.0.1:5000

---

## 2. Basit sözlük — terimler ne demek?

Hoca veya jüri teknik kelime kullanırsa panik yapmayın. Aşağıdaki tablo yeterli.

| Kelime | Basit anlamı | Projede nerede? |
|--------|--------------|-----------------|
| **Web sitesi** | Tarayıcıda açılan program | Chrome’da StajFlow |
| **Backend (arka uç)** | Sunucuda çalışan, iş yapan kod | `app.py` |
| **Frontend (ön uç)** | Kullanıcının gördüğü ekran | `templates/` + `style.css` |
| **Flask** | Python ile web sitesi yapma aracı | `app.py` Flask ile yazıldı |
| **Route (rota)** | Bir URL adresi, örn. `/ogrenci` | `app.py` içinde `@app.route(...)` |
| **Template (şablon)** | HTML sayfa dosyası | `templates/` klasörü |
| **Veritabanı (DB)** | Bilgilerin saklandığı yer | `instance/stajflow.db` |
| **SQLite** | Küçük, dosya tabanlı veritabanı | `.db` dosyası |
| **Tablo** | Excel sayfası gibi; satır = kayıt | `models.py`’de tanımlı |
| **Model** | Tablonun kod karşılığı | `models.py` |
| **ORM** | Veritabanına Python ile yazma | Flask-SQLAlchemy |
| **Login (giriş)** | E-posta + şifre ile oturum açma | `/login` |
| **Logout (çıkış)** | Oturumu kapatma | `/logout` |
| **Session (oturum)** | Giriş yaptıktan sonra “sen kimsin” bilgisi | Flask-Login |
| **Rol** | ogrenci / danisman / admin | `User.role` alanı |
| **POST** | Form gönderme (kaydet, ekle, sil) | HTML formlar |
| **GET** | Sayfa açma / listeleme | Linke tıklayınca |
| **CRUD** | Ekle, listele, güncelle, sil | Admin paneli |
| **UI** | Kullanıcı arayüzü — görünüm | CSS + HTML |
| **CSS** | Renk, yazı tipi, düzen | `static/css/style.css` |
| **Sidebar** | Sol taraftaki menü | `base.html` |
| **Upload (yükleme)** | Dosya gönderme (CV vb.) | `instance/uploads/` |
| **Seed (tohum veri)** | Demo / örnek veri | `db_seed.py` |
| **Git / GitHub** | Kod versiyon takibi | github.com/sl-kl3/StajFlow |
| **Commit** | Kod değişikliğini kaydetme | Git geçmişi |

> **REST API yok** demek: Ayrı bir mobil uygulama için JSON servisi yazmadık. Her şey normal web sayfası + form ile çalışıyor. Bu bir eksiklik değil, bilinçli tercih.

---

## 3. Kim ne yaptı? (Görev dağılımı)

### Özet tablo

| Kişi | Ana görev | Dokunduğu dosyalar |
|------|-----------|-------------------|
| **Salih** | Proje lideri, giriş sistemi, danışman onay mantığı | `app.py` (login, rol, `/action/*`, `/danisman/*`) |
| **Mine** | Öğrenci paneli, profil, belge yükleme | `app.py` (öğrenci route’ları) + `templates/ogrenci/*` |
| **Nazlı** | Veritabanı tasarımı, demo veri, kurulum | `models.py`, `db_seed.py`, `setup_db.py` |
| **Zuhal** | Admin paneli ekranları | `templates/admin/*` + admin formları |
| **İlknur** | Tasarım, CSS, ortak şablon, danışman ekranları | `base.html`, `login.html`, `style.css`, `templates/danisman/*` |

### Commit konusu (dürüst cümle)

> “Kodun büyük kısmını Salih ve Mine yazıp GitHub’a gönderdi. Nazlı veritabanını tasarladı ve test etti. Zuhal admin ekranlarını hazırladı. İlknur arayüzü ve CSS’i yaptı. Son hafta hepsini birleştirdik.”

Bu normal. Üniversite projelerinde repo genelde 1–2 kişide kalır.

---

## 4. Salih — rehberin

### Senin görevin ne?

- Proje lideri
- Giriş / çıkış sistemi
- Rol kontrolü (kim nereye girebilir)
- Danışman onay ve puanlama **arka plan kodu**
- Parçaları birleştirme, README, son düzeltmeler

### Senin dosyaların

| Dosya | Ne var? |
|-------|---------|
| `app.py` | `@app.route('/login')`, `/logout`, `/dashboard` |
| `app.py` | `role_required()` — yetki kontrolü |
| `app.py` | `/action/apply/...` — başvuru onay/red |
| `app.py` | `/action/log/...` — günlük onay/red |
| `app.py` | `/action/score/...` — puan kaydetme |
| `app.py` | `/danisman/*` — danışman sayfa route’ları |

### Adım adım öğren (30 dk)

**Adım 1 — Projeyi aç**

```
python setup_db.py
python app.py
```

**Adım 2 — Girişi dene**

- Yanlış şifre → “E-posta veya şifre hatalı” mesajı
- Doğru giriş → rolüne göre yönlendirme

**Adım 3 — `app.py` aç, şunları bul**

1. `@app.route('/login'` — giriş sayfası
2. `def role_required` — yetki decorator’ı
3. `def action_apply` — başvuru onayı
4. `def action_score` — puanlama

**Adım 4 — Sunum cümlesi ezberle**

> “Ben giriş sistemini ve rol bazlı yetkilendirmeyi yazdım. Danışmanın başvuru onaylama, günlük onaylama ve puan verme işlemlerinin arka plan kodu bende. Proje lideri olarak parçaları birleştirdim.”

### Hoca sana sorarsa

| Soru | Cevabın |
|------|---------|
| Rol kontrolü nasıl? | `@login_required` önce giriş var mı bakar. `@role_required('danisman')` rol uyuyor mu bakar. Uymazsa hata mesajı + yönlendirme. |
| Öğrenci admin sayfasına girerse? | `role_required` yakalar, “Bu işlem için yetkiniz yok” der, öğrenci ana sayfasına atar. |
| Onay nasıl çalışır? | Danışman butona basınca POST gider → `action_apply` çalışır → veritabanında `status` alanı `Onaylandı` veya `Reddedildi` olur. |

### Sunumda sen ne gösterirsin?

1. Yanlış şifre dene (5 sn)
2. Danışman gir → başvuru onayla → günlük onayla → puan ver (2 dk)

---

## 5. Mine — rehberin

### Senin görevin ne?

- Öğrenci panelinin **tamamı**
- Profil formu (GANO, okul, deneyim vb.)
- CV / diploma / belge yükleme
- Staj ilanlarına başvuru
- Staj günlüğü ekleme

### Senin dosyaların

| Dosya | Ne var? |
|-------|---------|
| `app.py` | `/ogrenci`, `/ogrenci/ilanlar`, `/ogrenci/basvurularim`, `/ogrenci/gunluk`, `/ogrenci/degerlendirme` |
| `app.py` | `ogrenci_profil`, `apply_program`, `add_log`, `save_document` |
| `templates/ogrenci/anasayfa.html` | Profil + belge formu |
| `templates/ogrenci/ilanlar.html` | Staj ilanları listesi |
| `templates/ogrenci/basvurularim.html` | Başvuru durumları |
| `templates/ogrenci/gunluk.html` | Günlük ekleme |
| `templates/ogrenci/degerlendirme.html` | Puan görüntüleme |

### Adım adım öğren (30 dk)

**Adım 1 — Öğrenci olarak gir**

- `ogr@staj.edu.tr` / `ogr123`

**Adım 2 — Sırayla dene**

1. Ana sayfa → profil doldur, GANO yaz (ör. 3.5)
2. CV yükle (PDF veya resim)
3. Staj İlanları → bir ilana başvur
4. Başvurularım → “Onay Bekliyor” gör
5. (Danışman onayladıktan sonra) Günlük → metin + saat (1–12) ekle

**Adım 3 — `app.py`’de bul**

- `def apply_program` — başvuru mantığı
- `def add_log` — günlük ekleme
- `def save_document` — dosya kaydetme

**Adım 4 — Sunum cümlesi ezberle**

> “Öğrenci tarafını ben yaptım. Profil, belge yükleme, ilana başvuru ve günlük tutma ekranları bende. Çok sayfalı yapıya geçişte de çalıştım.”

### Hoca sana sorarsa

| Soru | Cevabın |
|------|---------|
| İki kez başvurabilir mi? | Hayır. Aktif veya bekleyen başvuru varsa sistem engeller. |
| Günlük kim onaylar? | Danışman. Öğrenci ekler → durum “Beklemede” → danışman onaylar. |
| CV nereye kaydoluyor? | `instance/uploads/` klasörüne. Veritabanında dosya adı tutulur. |
| GANO kontrolü var mı? | Evet, 0 ile 4 arası olmalı. |

### Sunumda sen ne gösterirsin?

Öğrenci akışı baştan sona (3 dk):

Profil → başvuru → (Salih/danışman onaylasın) → günlük ekle

---

## 6. Nazlı — rehberin

### Senin görevin ne?

- Veritabanı **tasarımı** (hangi tablo, hangi alan)
- Tablolar arası **ilişkiler** (öğrenci → başvuru → günlük)
- Demo veri (örnek şirketler, kullanıcılar)
- Kurulum scripti (`setup_db.py`)

> Kodu Salih/Mine birleştirmiş olabilir; sen **tasarımı ve mantığı** anlatırsın.

### Senin dosyaların

| Dosya | Ne var? |
|-------|---------|
| `models.py` | 7 tablo tanımı |
| `db_seed.py` | Demo kullanıcılar, 3 şirket, 3 staj ilanı |
| `setup_db.py` | Veritabanını sıfırlayıp yeniden kurar |
| `instance/stajflow.db` | Çalışınca oluşan veritabanı dosyası |

### Veritabanı tabloları (ezberle)

| Tablo | Ne tutuyor? | Örnek |
|-------|-------------|-------|
| `user` | Kullanıcılar | öğrenci, danışman, admin |
| `university` | Kurum adı | “Üniversite Staj Yönetim Sistemi” |
| `company` | Şirketler | Anadolu Yazılım A.Ş. |
| `internship_program` | Staj ilanları | Backend Stajı, kontenjan 3 |
| `internship` | Öğrenci başvuruları | Onay Bekliyor / Onaylandı / Reddedildi |
| `daily_log` | Staj günlükleri | Metin + saat + durum |
| `student_document` | Yüklenen belgeler | CV, diploma |

### İlişkiler (basit çiz)

```
Öğrenci (user)
   ├── birçok Başvuru (internship)
   ├── birçok Günlük (daily_log)
   └── birçok Belge (student_document)

Şirket (company)
   └── birçok İlan (internship_program)
           └── birçok Başvuru (internship)
```

### Adım adım öğren (30 dk)

**Adım 1 — `models.py` aç**

- `class User` — kullanıcı alanları (email, role, gpa…)
- `class Internship` — başvuru, status, score
- `class DailyLog` — günlük, hours, status

**Adım 2 — `db_seed.py` aç**

- `DEMO_USERS` — 3 demo hesap
- `seed_sirketler()` — 3 şirket + 3 ilan

**Adım 3 — Terminalde dene**

```
python setup_db.py
```

“tamam, db hazir” yazısını gör.

**Adım 4 — Sunum cümlesi ezberle**

> “Veritabanı şemasını ben tasarladım. Hangi bilgi hangi tabloda, öğrenci ile başvuru nasıl bağlanıyor — bunları ben belirledim. Demo verileri ve kurulum scripti de benim kısmım.”

### Hoca sana sorarsa

| Soru | Cevabın |
|------|---------|
| Neden SQLite? | Kurulumu kolay, dosya olarak taşınır, üniversite projesi için yeterli. |
| Kaç tablo var? | 7 tablo. |
| Başvuruda şirket adı neden kopyalanıyor? | İlan silinse bile eski başvuru kaydı bozulmasın diye snapshot alıyoruz. |
| setup_db ne yapar? | Eski veriyi siler, tabloları yeniden oluşturur, demo veriyi yükler. Sunum öncesi temiz başlangıç için. |

### Sunumda sen ne gösterirsin?

1. `models.py`’de 2–3 tablo göster (1 dk)
2. Terminalde `python setup_db.py` çalıştır (30 sn)
3. İlişki şemasını kağıtta veya slaytta anlat (1 dk)

---

## 7. Zuhal — rehberin

### Senin görevin ne?

- **Admin paneli** ekranları
- Kullanıcı ekleme / silme formları
- Şirket ve staj ilanı ekleme ekranları
- Rapor sayfası düzeni

> Route’ları (arka plan bağlantısı) Salih yazmış olabilir; sen **admin ekranlarını ve akışı** anlatırsın.

### Senin dosyaların

| Dosya | Ne var? |
|-------|---------|
| `templates/admin/anasayfa.html` | Admin dashboard |
| `templates/admin/ogrenciler.html` | Kullanıcı listesi + ekleme formu |
| `templates/admin/basvurular.html` | Tüm başvurular |
| `templates/admin/sirketler.html` | Şirket + ilan yönetimi |
| `templates/admin/raporlar.html` | İstatistik raporu |

### Admin ne yapabilir? (ezberle)

1. Yeni kullanıcı ekle (öğrenci / danışman / admin)
2. Kullanıcı sil (kendi hesabı hariç)
3. Şirket ekle
4. Staj programı (ilan) ekle
5. İlanı aç/kapat (aktif/pasif)
6. Rapor sayfasında sayıları gör

### Adım adım öğren (30 dk)

**Adım 1 — Admin gir**

- `admin@staj.edu.tr` / `admin123`

**Adım 2 — Her menüyü gez**

- Dashboard → Öğrenciler → Başvurular → Şirketler → Raporlar

**Adım 3 — Canlı dene**

1. Öğrenciler → yeni öğrenci ekle (test isim)
2. Şirketler → yeni şirket + staj programı ekle
3. Raporlar → sayıları kontrol et

**Adım 4 — Bir HTML dosyası aç**

`templates/admin/sirketler.html` — form alanlarını gör (şirket adı, sektör, program başlığı…)

**Adım 5 — Sunum cümlesi ezberle**

> “Admin panelinin ekranlarını ben hazırladım. Kullanıcı yönetimi, şirket ve staj ilanı ekleme formları, rapor sayfası bende. Admin’in gördüğü tüm sayfalar benim tasarımım.”

### Hoca sana sorarsa

| Soru | Cevabın |
|------|---------|
| Admin ne işe yarar? | Sistemi yönetir: kullanıcı, şirket, ilan. Öğrenci sadece başvurur, admin altyapıyı kurar. |
| Kontenjan nerede? | Staj programı eklerken `quota` alanı — kaç öğrenci kabul edilecek. |
| İlan kapatılınca ne olur? | `is_active = false` — öğrenci listesinde görünmez, yeni başvuru alınmaz. |

### Sunumda sen ne gösterirsin?

Admin giriş → şirket ekle → ilan ekle → rapor sayfası (2–3 dk)

---

## 8. İlknur — rehberin

### Senin görevin ne?

- Sitenin **görünümü** (renk, yazı, düzen)
- Sol menü (sidebar) tasarımı
- Login (giriş) sayfası
- Danışman ekranlarının HTML’i
- Ortak şablon (`base.html`) — tüm sayfalar bunu kullanır

### Senin dosyaların

| Dosya | Ne var? |
|-------|---------|
| `templates/base.html` | Sidebar, header, flash mesaj alanı |
| `templates/login.html` | Giriş ekranı |
| `static/css/style.css` | Tüm renkler, kartlar, butonlar |
| `templates/danisman/anasayfa.html` | Danışman dashboard |
| `templates/danisman/basvuru-onay.html` | Başvuru onay listesi |
| `templates/danisman/gunluk-onay.html` | Günlük onay listesi |
| `templates/danisman/puanlama.html` | Puan verme ekranı |

### UI ne demek?

**UI = User Interface = Kullanıcı arayüzü**

Yani kullanıcının gördüğü her şey: butonlar, renkler, menü, kartlar. Backend görünmez; sen görünen kısmı yaptın.

### Adım adım öğren (30 dk)

**Adım 1 — 3 rolde giriş yap, menüye bak**

- Öğrenci menüsü: Ana Sayfa, Başvurularım, İlanlar, Günlük, Değerlendirme
- Danışman menüsü: Ana Sayfa, Başvuru Onayı, Günlük Onayı, Puanlama
- Admin menüsü: Dashboard, Öğrenciler, Başvurular, Şirketler, Raporlar

**Adım 2 — `base.html` aç**

Şu satırları bul:

```
{% if user_role == 'ogrenci' %}
```

→ Rol değişince menü linkleri değişiyor. Bunu hocaya anlat.

**Adım 3 — `style.css` aç**

- `.sidebar` — sol menü
- `.nav-item` — menü linkleri
- Renkleri gör (mavi tonlar, kartlar)

**Adım 4 — Sunum cümlesi ezberle**

> “Arayüz tasarımını ben yaptım. Sidebar, login sayfası, renkler ve danışman ekranlarının görünümü bende. Tüm sayfalar ortak şablonu (`base.html`) kullanıyor; menü role göre değişiyor.”

### Hoca sana sorarsa

| Soru | Cevabın |
|------|---------|
| Neden React kullanmadınız? | Sunucu tarafında HTML yeterli. Ayrı frontend framework’üne gerek yoktu, Flask + Jinja2 ile hızlı yaptık. |
| Menü rol bazlı nasıl? | `base.html`’de Jinja2 if/elif: öğrenciyse öğrenci linkleri, danışmansa danışman linkleri gösterilir. |
| CSS ne işe yarar? | HTML iskelet; CSS görünüm. Renk, boşluk, font, responsive düzen CSS’te. |

### Sunumda sen ne gösterirsin?

1. Login ekranı (10 sn)
2. 3 rolde sidebar farkını göster (1 dk)
3. Danışman ekranından birini aç — düzen güzel mi anlat (1 dk)

---

## 9. Sunum sırası (10–12 dakika)

| Sıra | Kim | Konu | Süre |
|------|-----|------|------|
| 1 | **Salih** | Problemi anlat + giriş/rol | ~2 dk |
| 2 | **Nazlı** | Veritabanı tabloları + setup_db | ~2 dk |
| 3 | **Mine** | Öğrenci akışı (profil → başvuru → günlük) | ~3 dk |
| 4 | **Salih** | Danışman onay + puan (kısa) | ~1 dk |
| 5 | **Zuhal** | Admin paneli | ~2 dk |
| 6 | **İlknur** | Arayüz + kapanış | ~2 dk |

**Herkes sadece kendi kısmını anlatır.** Başkasının kodunu detaylı anlatma.

### Herkesin kapanış cümlesi

> “Benim kısmım buydu. Sorularınız varsa cevaplayabilirim.”

---

## 10. Hocanın sorabileceği sorular ve cevaplar

### Genel proje soruları

| Soru | Kim cevaplar | Cevap |
|------|--------------|-------|
| Bu proje ne yapıyor? | Salih | Üniversite staj sürecini dijitalleştiriyor: başvuru, onay, günlük, puanlama. |
| Kaç kişi yaptınız? | Salih | 5 kişi. Görev dağılımı TAKIM_REHBERI.md’de. |
| Neden Flask? | Salih veya Mine | Python öğreniyoruz, Flask hafif ve hızlı prototip için uygun. |
| Veritabanı ne? | Nazlı | SQLite. 7 tablo. Bilgiler `instance/stajflow.db` dosyasında. |
| Güvenlik var mı? | Salih | Şifreler hash’leniyor, giriş zorunlu, rol kontrolü var. Canlıya alınsa CSRF ve HTTPS eklenir — demo projesi olarak bilinçli basit tuttuk. |
| Test ettiniz mi? | Herkes | Her rolde manuel test: giriş, başvuru, onay, puan, admin CRUD. |
| GitHub’da mı? | Salih | Evet: github.com/sl-kl3/StajFlow |

### Teknik sorular (panik olmayın)

| Soru | Cevap (basit) |
|------|---------------|
| API var mı? | Hayır, klasik web formu. Sayfa aç → form doldur → kaydet. |
| Şifre düz metin mi? | Hayır. Werkzeug ile hash’lenip saklanıyor. |
| Dosya yükleme güvenli mi? | Uzantı kontrolü var (pdf, doc, jpg…). Max 16 MB. |
| Aynı anda 2 başvuru? | Hayır, sistem engelliyor. |
| Kontenjan dolunca? | “Kontenjan dolmuş” mesajı, başvuru alınmaz. |

### “Sen ne yaptın?” sorusu — kişi kişi

| İsim | 1 cümle |
|------|---------|
| Salih | Giriş, rol sistemi, danışman onay backend’i, proje birleştirme. |
| Mine | Öğrenci paneli, profil, belge yükleme, başvuru, günlük. |
| Nazlı | Veritabanı tasarımı, tablolar, demo veri, setup_db. |
| Zuhal | Admin paneli ekranları ve yönetim formları. |
| İlknur | Arayüz tasarımı, CSS, sidebar, login, danışman HTML. |

### Zor soru gelirse

> “Bu kısmı tam hatırlamıyorum ama [doğru kişi adı] yapmıştı, detayı o anlatsın.”

Bu cümle **normal ve profesyonel**. Takım projesinde herkes her satırı bilmez.

---

## 11. Sunumdan 1 gün önce kontrol listesi

### Herkes yapacak

- [ ] `git pull` yaptım
- [ ] `python setup_db.py` çalıştırdım
- [ ] `python app.py` ile site açılıyor
- [ ] Kendi bölümümü bilgisayarda **canlı gösterdim**
- [ ] TAKIM_REHBERI.md’de **kendi bölümümü** okudum
- [ ] “Ben ne yaptım?” cümlesini ezberledim

### Salih + Mine ekstra

- [ ] Demo akış baştan sona denendi (öğrenci başvur → danışman onay → puan)
- [ ] Laptop şarjlı, internet gerekmez (localhost)

### Nazlı + Zuhal + İlknur ekstra

- [ ] Kendi dosyalarını VS Code / Cursor’da açıp gezdin
- [ ] Hocanın 2 soruya cevap verebiliyorsun (yukarıdaki tablolar)

### Sunum günü

1. Sunumdan **10 dk önce** `python setup_db.py` (temiz demo veri)
2. `python app.py` başlat
3. Tarayıcıda login sayfasını açık bırak
4. Sırayla konuş, herkes kendi kısmını göstersin

---

## Dosya haritası (hızlı bakış)

```
stajflow/
├── app.py              ← Salih + Mine (route’lar, iş mantığı)
├── models.py           ← Nazlı (tablolar)
├── db_seed.py          ← Nazlı (demo veri)
├── setup_db.py         ← Nazlı (db sıfırlama)
├── templates/
│   ├── base.html       ← İlknur (ortak şablon)
│   ├── login.html      ← İlknur
│   ├── ogrenci/        ← Mine (5 sayfa)
│   ├── danisman/       ← İlknur (4 sayfa)
│   └── admin/          ← Zuhal (5 sayfa)
├── static/css/style.css ← İlknur
└── instance/
    ├── stajflow.db     ← veritabanı (çalışınca oluşur)
    └── uploads/        ← yüklenen CV vb.
```

---

**Başarılar — takım olarak gösterin, panik yapmayın. Hoca çalışan demo + görev dağılımı ister; ikisi de elinizde.**
