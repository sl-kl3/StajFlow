# GitHub'da Gorunmek Icin — Nazli, Zuhal, Ilknur

Gereksiz ek dosya yok. **Kendi modul dosyaniza** kucuk bir duzenleme yapip push edeceksiniz.  
Proje bozulmaz — sadece yorum satiri veya kucuk metin duzeltmesi.

Salih sizin yerinize commit atamaz. **Kendi bilgisayarinizdan, kendi GitHub hesabinizla** yapin (5 dk).

---

## Kim hangi dosyaya dokunacak?

| Kisi | Gercek dosya | Ne yapacak |
|------|--------------|------------|
| **Nazli** | `models.py` | En uste aciklama yorumu ekle |
| **Zuhal** | `templates/admin/ogrenciler.html` | Rol secenegini duzelt |
| **Ilknur** | `templates/login.html` | Yazim hatasi duzelt |

Hepsi zaten projede var. **Yeni dosya olusturmayin.**

---

## Oncelik: GitHub collaborator

Salih sizi repo'ya eklemeli. E-postadaki daveti kabul edin.

---

## Ortak adimlar (herkes)

```powershell
cd Desktop\StajFlow
git pull

git config user.name "Adin Soyadin"
git config user.email "github-epostan@..."
```

> E-posta GitHub hesabinizdaki ile ayni olmali.

**Sirayla push edin:** Nazli -> Zuhal -> Ilknur. Herkes push etmeden once `git pull` yapsin.

---

## NAZLI — `models.py`

Dosyayi ac. **En ust satira** (1. satir, `from datetime` oncesine) su 2 satiri ekle:

```python
# StajFlow veritabani modelleri (7 tablo)
# User, University, Company, InternshipProgram, Internship, DailyLog, StudentDocument
```

Sonra:

```powershell
git add models.py
git commit -m "models dosyasina aciklama eklendi"
git push origin main
```

**Hocaya:** "Veritabani tablolarini models.py'de tanimladik. Ben tablo yapisini ve aciklamasini ekledim."

---

## ZUHAL — `templates/admin/ogrenciler.html`

Dosyayi ac. Rol seciminde su satiri bul (satir 13 civari):

```html
<option value="admin">Yönetici</option>
```

Su sekilde degistir:

```html
<option value="admin">Admin</option>
```

(Geri kalan projede de "Admin" yaziyor, tutarlilik icin.)

Sonra:

```powershell
git add templates/admin/ogrenciler.html
git commit -m "admin kullanici ekleme ekrani duzeltildi"
git push origin main
```

**Hocaya:** "Admin panelindeki kullanici ekleme formunu ben duzenledim. Rol secenekleri ve formlar admin/ogrenciler.html dosyasinda."

---

## ILKNUR — `templates/login.html`

Dosyayi ac. Su satiri bul (satir 16 civari):

```html
<p>Ogrenci basvurusu, danisman onayi, gunluk ve puanlama.</p>
```

Su sekilde degistir (Turkce karakter):

```html
<p>Öğrenci başvurusu, danışman onayı, günlük ve puanlama.</p>
```

Sonra:

```powershell
git add templates/login.html
git commit -m "login sayfasi metin duzeltmesi"
git push origin main
```

**Hocaya:** "Giris ekraninin arayuzunu ve metinlerini ben duzenledim. login.html ve CSS benim kisim."

---

## Isteg bagli 2. commit (daha guclu kanit)

Ilk commit yetmezse bir satir daha:

| Kisi | Dosya | Ekle |
|------|-------|------|
| Nazli | `db_seed.py` | En uste: `# Demo veri ve seed - Nazli` |
| Zuhal | `templates/admin/sirketler.html` | `{# Sirket ve ilan yonetimi #}` en uste |
| Ilknur | `static/css/style.css` | En uste: `/* StajFlow arayuz stilleri */` |

Ayri commit atin.

---

## Proje bozulur mu?

| Soru | Cevap |
|------|-------|
| Uygulama calisir mi? | Evet |
| Yeni dosya eklenir mi? | Hayir |
| Ne degisir? | 1-2 satir yorum veya metin |
| Flask etkilenir mi? | Hayir, yorum satirlari kodu bozmaz |

Push sonrasi test (istege bagli):

```powershell
python app.py
```

Tarayicida login ac, admin ogrenci ekle ekranina bak.

---

## Hata cozumleri

**Push reddedildi** -> Salih collaborator eklemeli, davet kabul.

**Conflict** -> `git pull origin main` sonra tekrar dene.

**Ismim commit'te yok** -> `git config user.email` GitHub e-postasi mi kontrol et.

---

## Salih'e not

1. Collaborator ekle (Nazli, Zuhal, Ilknur)
2. Bu dosyayi gruba at
3. Sirayla push etmelerini soyle

Eski `docs/` klasoru kaldirildi — gercek proje dosyalari uzerinden katki daha mantikli.
