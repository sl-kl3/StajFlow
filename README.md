# StajFlow

Bilgisayar Mühendisliği staj takip sistemi (Flask + SQLite).

## Roller

- **Admin** — şirket ve ilan ekler
- **Öğrenci** — ilanlara başvurur, günlük yazar
- **Danışman** — başvuru ve günlük onaylar

## Kurulum

```bash
pip install -r requirements.txt
python setup_db.py
python app.py
```

Tarayıcı: http://127.0.0.1:5000

## Test hesapları

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Admin | admin@staj.edu.tr | admin123 |
| Danışman | danisman@staj.edu.tr | danisman123 |
| Öğrenci | ogr@staj.edu.tr | ogr123 |

## Dosya yapısı

```
app.py          → ana uygulama, route'lar
models.py       → veritabanı tabloları
db_seed.py      → demo veriler
setup_db.py     → veritabanını sıfırlama
templates/      → html şablonları
static/css/     → stil dosyası
```
