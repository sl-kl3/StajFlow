# StajFlow

Bilgisayar Mühendisliği staj takip projesi.

## Sistem

| Rol | Görev |
|-----|--------|
| **Admin** | Şirket kaydı, staj ilanı yayınlama (şirketlerin ayrı hesabı yok) |
| **Öğrenci** | Şirket ilanlarına başvuru, staj günlüğü |
| **Danışman** | Başvuru ve günlük onayı |

## Panel menüleri

Her rol için sol menü ayrı sayfaya gider (kaydırma değil, gerçek sayfa geçişi):

| Rol | Menü |
|-----|------|
| **Öğrenci** | Ana Sayfa, Staj İlanları, Başvurularım, Staj Günlüğüm, Değerlendirmem |
| **Danışman** | Ana Sayfa, Başvuru Onayı, Günlük Onayı, Son İşlemler |
| **Admin** | Ana Sayfa, Öğrenciler, Başvurular, Şirketler, Raporlar |

## Kurulum

```bash
pip install -r requirements.txt
python setup_db.py
python app.py
```

http://127.0.0.1:5000

## Test hesapları

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Admin | admin@staj.edu.tr | admin123 |
| Danışman | danisman@staj.edu.tr | danisman123 |
| Öğrenci | ogr@staj.edu.tr | ogr123 |
