# StajFlow

BM staj takip projesi. Flask + SQLite kullandik.

## Ne yapiyor bu site?

- Admin -> sirket kaydi, staj ilani acma
- Ogrenci -> ilana basvuru, staj gunlugu yazma
- Danisman -> basvuru ve gunluk onaylama / reddetme

## Calistirmak icin

Projeyi cektikten sonra sirayla:

    pip install -r requirements.txt
    python setup_db.py
    python app.py

Sonra tarayicidan: http://127.0.0.1:5000

(Ekip arkadasiysan once git pull at.)

## Giris bilgileri (test)

- Admin -> admin@staj.edu.tr / admin123
- Danisman -> danisman@staj.edu.tr / danisman123
- Ogrenci -> ogr@staj.edu.tr / ogr123

## Dosyalar ne?

- app.py -> asil kod, sayfalar ve islemler burda
- models.py -> veritabani tablolari
- db_seed.py -> demo kullanici ve ornek sirketler
- setup_db.py -> db'yi sifirlayip bastan kurar
- requirements.txt -> lazim olan kutuphaneler
- templates/ -> html sayfalari
- static/css/style.css -> gorunum

## instance ve __pycache__ niye cikiyor?

Programi calistirinca kendiliginden olusuyorlar, normal.

- instance/ -> veritabani dosyasi (stajflow.db) burda duruyor
- __pycache__/ -> python'un cache klasoru

Ikisini de silebilirsin ama python app.py deyince yine gelir. GitHub'a zaten gitmiyor (.gitignore'da var).

Veritabanini sifirlamak istersen: python setup_db.py
