# StajFlow

Türkiye'deki üniversiteler için staj başvuru, onay ve günlük takip sistemi. Flask + SQLite.

## Ne yapıyor?

- **Yönetici** → şirket kaydı, staj ilanı, kullanıcı yönetimi
- **Öğrenci** → ilana başvuru, günlük ve çalışılan saat girişi
- **Danışman** → başvuru/günlük onayı, staj puanlama

## Kurulum

```bash
pip install -r requirements.txt
python setup_db.py
python app.py
```

Tarayıcı: http://127.0.0.1:5000

## Demo hesaplar

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Yönetici | admin@staj.edu.tr | admin123 |
| Danışman | danisman@staj.edu.tr | danisman123 |
| Öğrenci | ogr@staj.edu.tr | ogr123 |

## Üniversite adını özelleştirme

Windows PowerShell:

```powershell
$env:UNIVERSITY_NAME="İstanbul Teknik Üniversitesi"
python app.py
```

## Dosyalar

- `app.py` — route'lar ve iş mantığı
- `models.py` — veritabanı tabloları
- `db_seed.py` — demo veriler ve hesap onarımı
- `setup_db.py` — veritabanını sıfırlar
- `templates/` — HTML sayfaları
- `static/css/style.css` — arayüz

## Not

`instance/stajflow.db` uygulama çalışınca oluşur. Sıfırlamak için: `python setup_db.py`
