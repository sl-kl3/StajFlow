# StajFlow

Bilgisayar Mühendisliği staj takip sistemi (Flask + SQLite).

## Roller

- **Admin** — şirket ve ilan ekler
- **Öğrenci** — ilanlara başvurur, günlük yazar
- **Danışman** — başvuru ve günlük onaylar

## Kurulum

```bash
git pull
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

## Dosyalar (GitHub'da olanlar)

| Dosya / Klasör | Ne işe yarar? |
|----------------|---------------|
| `app.py` | Ana program. Giriş, paneller, başvuru, onay route'ları burada. |
| `models.py` | Veritabanı tabloları (User, Company, Internship, DailyLog vb.) |
| `db_seed.py` | İlk açılışta demo kullanıcı ve örnek şirket/ilan ekler |
| `setup_db.py` | Veritabanını sıfırlayıp demo verileri yeniden kurar |
| `requirements.txt` | Kurulacak Python kütüphaneleri listesi |
| `.gitignore` | GitHub'a gitmemesi gereken dosyaları belirler |
| `templates/` | HTML sayfaları (login, panel, admin, öğrenci, danışman) |
| `static/css/style.css` | Site görünümü (renkler, sidebar, kartlar) |

## GitHub'a gitmeyenler (normal, silinebilir)

| Klasör | Açıklama |
|--------|----------|
| `instance/` | SQLite veritabanı (`stajflow.db`). `app.py` veya `setup_db.py` çalışınca otomatik oluşur. |
| `__pycache__/` | Python'un geçici önbelleği. Silinsin, tekrar oluşur. |
| `venv/` | Sanal ortam (varsa). Herkes kendi bilgisayarında kurar. |
