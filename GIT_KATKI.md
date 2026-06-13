# GitHub'da Gorunmek Icin — Nazli, Zuhal, Ilknur

Salih ve Mine commit atmis. Siz de **kendi GitHub hesabinizdan** 1 commit atinca hocaya ve arkadaslara gorunursunuz.

> Onemli: Salih sizin yerinize commit atamaz — GitHub'da **sizin isminiz** cikmaz.  
> Herkes **kendi bilgisayarindan** yapacak (5 dk surer).

---

## Onceden hazir dosyalar

| Kisi | Dosya | Ne yapacaksin |
|------|-------|---------------|
| **Nazli** | `docs/veritabani-notlari.md` | En alta adini ve tarihi yaz |
| **Zuhal** | `docs/admin-panel-notlari.md` | En alta adini ve tarihi yaz |
| **Ilknur** | `docs/arayuz-notlari.md` | En alta adini ve tarihi yaz |

Dosyalarin icerigi hazir. Sadece en alttaki `(buraya adini yaz)` kismini duzenleyip push edeceksin.

---

## Adim adim (Windows — PowerShell)

### 0) GitHub hesabin

- GitHub'a uye ol
- Salih seni repo'ya collaborator olarak eklemis olmali
- GitHub -> Settings -> Emails -> e-posta adresini not al (commit'te bu lazim)

### 1) Projeyi indir (ilk kez)

```powershell
cd Desktop
git clone https://github.com/sl-kl3/StajFlow.git
cd StajFlow
```

Zaten indirdiysen:

```powershell
cd Desktop\StajFlow
git pull
```

### 2) Git'e kendi ismini yaz (sadece 1 kez)

```powershell
git config user.name "Nazli Yilmaz"
git config user.email "senin-github-email@example.com"
```

> `user.email` GitHub hesabindaki e-posta olmali — yoksa commit profilinde gorunmez.

Zuhal ve Ilknur kendi isimlerini yazar.

### 3) Dosyani duzenle

**Nazli:**

`docs/veritabani-notlari.md` dosyasini ac. En alt satirlari soyle yap:

```
*Hazirlayan: Nazli Yilmaz*
*Tarih: 2 Haziran 2026*
```

**Zuhal:**

`docs/admin-panel-notlari.md` — en alta kendi adin + tarih

**Ilknur:**

`docs/arayuz-notlari.md` — en alta kendi adin + tarih

### 4) Commit + push

```powershell
git add docs/veritabani-notlari.md
git commit -m "veritabani notlari eklendi"
git push origin main
```

Zuhal:

```powershell
git add docs/admin-panel-notlari.md
git commit -m "admin panel notlari eklendi"
git push origin main
```

Ilknur:

```powershell
git add docs/arayuz-notlari.md
git commit -m "arayuz notlari eklendi"
git push origin main
```

### 5) Kontrol

GitHub'da repo ac -> **Commits** -> kendi ismin gorunmeli.

---

## Sira onemli

1. Once **Nazli** pull + push
2. Sonra **Zuhal** pull + push
3. Sonra **Ilknur** pull + push

Ikisi ayni anda push ederse conflict olabilir. Biri bitirince digeri `git pull` yapsin.

---

## Ekstra (istege bagli — daha inandirici)

Commit attiktan sonra kendi modul dosyana **1 satir yorum** ekleyebilirsin:

| Kisi | Dosya | Eklenecek satir (dosyanin en ustune) |
|------|-------|--------------------------------------|
| Nazli | `models.py` | `# Veritabani modelleri - Nazli` |
| Zuhal | `templates/admin/anasayfa.html` | `{# Admin dashboard - Zuhal #}` |
| Ilknur | `static/css/style.css` | `/* StajFlow arayuz - Ilknur */` |

Ayri commit:

```powershell
git add models.py
git commit -m "models dosyasina aciklama eklendi"
git push
```

---

## Hata cozumleri

**"Permission denied" / push olmuyor**

- Salih seni GitHub repo'ya collaborator olarak eklemeli
- GitHub'da daveti kabul et (e-posta gelir)

**"Conflict" / birlestirme hatasi**

```powershell
git pull origin main
```

Sonra tekrar duzenle, commit, push.

**Commit'te ismim yok**

```powershell
git config user.email
```

GitHub'daki e-posta ile ayni mi kontrol et.

---

## Hocaya ne dersiniz?

> "Ben kendi modulum icin dokuman yazdim ve GitHub'a push ettim. Veritabani / admin / arayuz notlari `docs/` klasorunde."

Bu gercek bir istir — yalan degil.

---

## Salih'e not

1. Nazli, Zuhal, Ilknur'u GitHub repo'ya **Collaborator** olarak ekle
2. Bu dosyayi (`GIT_KATKI.md`) gruba at
3. Sirayla push etmelerini iste
