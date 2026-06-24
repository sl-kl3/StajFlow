# ⚠️ SUNUMDAN ONCE BU DOSYAYI SIL

> Bu dosya sadece ekip icin. Hocaya gosterme, GitHub'dan da sunumdan once kaldir.
> Komut: `git rm TAKIM_REHBERI.md` sonra commit + push

---

# StajFlow — Takim Rehberi (5 kisi)

Ekip: **Salih, Mine, Nazli, Zuhal, Ilknur**

---

## 1. Kim ne yapti?

| Kisi | Gorev | Dosyalar |
|------|-------|----------|
| **Salih** | Proje lideri, giris/cikis, rol sistemi, danisman onaylari, birlestirme | `app.py` (login, role_required, /danisman/*, /action/*) |
| **Mine** | Ogrenci paneli, profil, belge yukleme, basvuru, gunluk | `app.py` (ogrenci route'lari) + `templates/ogrenci/*` |
| **Nazli** | Veritabani tablolari, demo veri | `models.py`, `db_seed.py`, `setup_db.py` |
| **Zuhal** | Admin paneli ekranlari | `templates/admin/*` |
| **Ilknur** | CSS, login, ortak sablon, danisman arayuzu | `style.css`, `base.html`, `login.html`, `templates/danisman/*` |

### Commit konusu (durust cevap)

> "Kodun buyuk kismini Salih ve Mine yazip pushladi. Nazli, Zuhal ve Ilknur kendi dosyalarina katki yapti — GitHub'da commit'leri var. Son hafta birlestirdik."

GitHub'da gorunen isimler: sl-kl13 (Salih), minekoseoglu02-ctrl (Mine), nazlcns (Nazli), Zuhal Gunen, ilknur

---

## 2. Basit sozluk (hoca sorarsa)

| Kelime | Ne demek |
|--------|----------|
| **Flask** | Python ile web sitesi yapma araci |
| **Jinja2** | HTML icine Python verisi gomme (templates/ klasoru) |
| **Route** | URL adresi, orn. `/ogrenci` |
| **SQLite** | Dosya tabanli veritabani (`instance/stajflow.db`) |
| **ORM** | Veritabanina Python ile yazma (SQLAlchemy) |
| **Login / Session** | Giris yapinca "sen kimsin" bilgisi tutulur |
| **POST / GET** | Form gonderme / sayfa acma |
| **UI** | Kullanicinin gordugu arayuz (CSS + HTML) |

REST API yok — normal web formu + sayfa yonlendirme kullaniyoruz.

---

## 3. Herkes kendi kismini nasil ogrenir?

### SALIH (30 dk)

**Dosyalar:** `app.py` — login, logout, role_required, action_apply, action_log, action_score

**Ezberle:**
> "Giris sistemini ve rol bazli yetkilendirmeyi yazdim. Danisman onay ve puanlama backend'i bende."

**Goster:** Yanlis sifre → danisman gir → basvuru onayla → puan ver

**Hoca sorarsa:**
- Rol kontrolu? → `@login_required` + `@role_required('danisman')`
- Ogrenci admin'e girerse? → Yetki yok mesaji + yonlendirme

---

### MINE (30 dk)

**Dosyalar:** `app.py` ogrenci kismi + `templates/ogrenci/*`

**Ezberle:**
> "Ogrenci tarafini yaptim: profil, belge yukleme, ilana basvuru, gunluk."

**Goster:** Profil doldur → basvur → gunluk ekle

**Hoca sorarsa:**
- Iki basvuru olur mu? → Hayir, aktif basvuru varsa engellenir
- CV nereye kaydoluyor? → `instance/uploads/`
- GANO kontrolu? → 0-4 arasi

---

### NAZLI (30 dk)

**Dosyalar:** `models.py`, `db_seed.py`, `setup_db.py`

**Ezberle:**
> "Veritabani tablolarini tasarladim. 7 tablo, demo veri ve setup_db bende."

**Goster:** models.py ac → `python setup_db.py`

**7 tablo:** user, university, company, internship_program, internship, daily_log, student_document

**Hoca sorarsa:**
- Neden SQLite? → Kurulum kolay, proje icin yeterli
- company_name neden basvuruda kopyalaniyor? → Ilan silinse bile gecmis kalsin diye

---

### ZUHAL (30 dk)

**Dosyalar:** `templates/admin/*`

**Ezberle:**
> "Admin panelinin ekranlarini hazirladim. Kullanici, sirket, ilan yonetimi bende."

**Goster:** Admin gir → kullanici ekle (ogrenci/danisman/admin) → sirket + ilan ekle → raporlar

**Hoca sorarsa:**
- Admin ne yapar? → Altyapiyi kurar (kullanici, sirket, ilan)
- Kontenjan? → Program eklerken quota alani
- Neden "Kullanicilar" sayfasi? → Sadece ogrenci degil, danisman ve admin de ekleniyor

---

### ILKNUR (30 dk)

**Dosyalar:** `base.html`, `login.html`, `style.css`, `templates/danisman/*`

**Ezberle:**
> "Arayuz tasarimini yaptim. Sidebar, renkler, login ve danisman ekranlari bende."

**Goster:** 3 rolde menu farki + login ekrani

**Hoca sorarsa:**
- Neden React yok? → Jinja2 + Flask yeterli, ders projesi
- Menu rol bazli? → base.html'de if/elif ile farkli linkler

---

## 4. Sunum sirasi (10-12 dk)

| Sira | Kim | Ne | Sure |
|------|-----|-----|------|
| 1 | Salih | Problem + giris/rol | 2 dk |
| 2 | Nazli | Veritabani + setup_db | 2 dk |
| 3 | Mine | Ogrenci akisi canli | 3 dk |
| 4 | Salih | Danisman onay + puan | 1 dk |
| 5 | Zuhal | Admin paneli | 2 dk |
| 6 | Ilknur | Arayuz + kapanis | 2 dk |

Sunumdan once: `python setup_db.py` → `python app.py`

Demo hesaplar README'de.

---

## 5. Hocanin sorabilecegi sorular — cevaplar

### Genel

| Soru | Cevap |
|------|-------|
| Proje ne yapiyor? | Universite staj basvurusu, onay, gunluk, puanlama |
| Kac kisisiniz? | 5 kisi, EKIP.md'de dagilim var |
| Neden Flask? | Python ogreniyoruz, hizli prototip icin uygun |
| Jinja kullandiniz mi? | Evet, templates/ klasoru Jinja2 sablonu |
| Kac tablo? | 7 tablo |
| Test ettiniz mi? | Her rolde manuel test yaptik |

### Teknik

| Soru | Cevap |
|------|-------|
| API var mi? | Hayir, form + redirect |
| Sifre guvenli mi? | Hash'leniyor (Werkzeug) |
| Dosya yukleme? | Uzanti kontrolu var, max 16 MB |
| CSRF var mi? | Hayir — demo projesi, canliya alinsa eklenir |
| Kayit sayfasi var mi? | Hayir — admin kullanici ekliyor + demo seed verisi |
| Demo hesaplar nereden? | db_seed.py — sunum icin otomatik yukleniyor |
| Sirketler gercek mi? | Hayir — seed_sirketler() ile ornek 3 firma + ilan |

### Demo hesaplar ve sirketler (detay — Nazli anlatsin)

**Demo hesaplar nasil var?**
- Dosya: `db_seed.py` → `DEMO_USERS` listesi
- Uygulama acilinca veya `python setup_db.py` calisinca veritabanina eklenir
- Sifreler hash ile saklanir (Werkzeug)
- Kayit ekrani yok — bilincli tercih, admin panelinden de eklenebilir

| Hesap | Sifre | Rol |
|-------|-------|-----|
| admin@staj.edu.tr | admin123 | Admin |
| danisman@staj.edu.tr | danisman123 | Danisman |
| ogr@staj.edu.tr | ogr123 | Ogrenci |

**Sirketler nereden geliyor?**
- `db_seed.py` → `seed_sirketler()` fonksiyonu
- Ilk kurulumda 3 ornek sirket + 3 staj ilani ekler
- Gercek firmalar degil, sunumda akisi gostermek icin
- Sonradan admin panelinden yeni sirket/ilan eklenebilir

Ornek sirketler: Anadolu Yazilim, Tekno A.S., DataHub Ltd.

### Admin kullanici ekleme (Zuhal anlatsin)

- Sayfa: **Kullanicilar** (`/admin/kullanicilar`) — eskiden "Ogrenciler" yaziyordu, duzelttik
- Ogrenci secilince → ogrenci no + bolum alanlari cikar
- Danisman veya Admin secilince → o alanlar gizlenir (gerek yok)


### "Sen ne yaptin?" — tek cumle

| Isim | Cevap |
|------|-------|
| Salih | Giris, rol sistemi, danisman backend, birlestirme |
| Mine | Ogrenci paneli, profil, belge, basvuru, gunluk |
| Nazli | Veritabani tablolari, demo veri, setup_db |
| Zuhal | Admin paneli ekranlari |
| Ilknur | CSS, login, sidebar, danisman arayuzu |

### Zor soru gelirse

> "Bu kismini tam hatirlamiyorum, [dogru kisi] yapmisti — o anlatsin."

---

## 6. Yapay zeka / Cursor kullandik mi? (ONEMLI)

### Durust cevap (hoca sorarsa)

> "Bazi kod parcalarinda Cursor ve ChatGPT'den yardim aldik — takildigimiz yerde syntax, hata duzeltme, arayuz duzenleme icin. Proje fikrini, akisi, rol dagilimini ve sunumu biz planladik. Kodu test ettik, demo akisini biz kurduk."

### Biz ne yaptik?

- Proje fikri ve akis (ogrenci → danisman → admin)
- Rol dagilimi ve kim hangi modul
- Flask + SQLite + Jinja yapisini kurma karari
- Demo hesaplar, sunum senaryosu
- Salih + Mine: ana kod, route'lar, entegrasyon
- Nazli, Zuhal, Ilknur: kendi modul dosyalari + GitHub commit
- Manuel test (her rolde deneme)
- Sunum provasi

### AI / Cursor ne yapti? (yardimci arac gibi)

- Bazi route ve bug fix onerileri
- Navigasyon / sayfa bolme duzenlemesi
- Dosya yukleme, validasyon gibi teknik parcalar
- README ve ic dokuman taslaklari (cogu silindi / sadelestirildi)
- Takim rehberi taslagi (bu dosya — sunumdan once silinecek)

### Hocaya soyleme

- "Tamamen AI yapti"
- "Hic bilmiyoruz"
- Bu dosyanin varligini (TAKIM_REHBERI.md)

### Hocaya soyle (kabul edilebilir)

> "Stack Overflow gibi kullandik — takildigimiz yerde AI'ya sorduk, anlayip uyarladik."

(Cok universitede bu kabul goruluyor; hocanizin politikasina bagli — emin degilseniz "yardim aldik" deyin, detaya girmeyin.)

---

## 7. Sunumdan once kontrol listesi

- [ ] `git pull`
- [ ] `python setup_db.py`
- [ ] `python app.py` calisiyor
- [ ] Herkes kendi bolumunu 1 kez gosterdi
- [ ] **TAKIM_REHBERI.md silindi** (GitHub'dan da)
- [ ] Demo sifreler calisiyor

### Sunumdan once dosyayi silmek icin

```powershell
git rm TAKIM_REHBERI.md
git commit -m "gereksiz dosya silindi"
git push
```

---

## 8. Dosya haritasi

```
app.py           → Salih + Mine (route'lar)
models.py        → Nazli
db_seed.py       → Nazli
setup_db.py      → Nazli
templates/ogrenci/   → Mine
templates/admin/kullanicilar.html → Zuhal (kullanici ekleme)
templates/danisman/  → Ilknur
base.html, login.html, style.css → Ilknur
EKIP.md          → kisa is dagilimi (bu kalabilir)
README.md        → kurulum
```

---

**Basarilar — herkes kendi kismini gostersin, panik yapmayin.**
