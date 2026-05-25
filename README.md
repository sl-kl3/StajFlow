# StajFlow

Bilgisayar Mühendisliği staj takip projesi.

## Sistem

| Rol | Görev |
|-----|--------|
| **Sistem yöneticisi** | Şirket kaydı, staj ilanı yayınlama (şirketlerin ayrı hesabı yok) |
| **Öğrenci** | Şirket ilanlarına başvuru, staj günlüğü |
| **Danışman** | Başvuru ve günlük onayı |

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
| Yönetici | admin@staj.edu.tr | admin123 |
| Danışman | hoca@staj.edu.tr | hoca123 |
| Öğrenci | ogr@staj.edu.tr | ogr123 |
