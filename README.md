# StajFlow

BM staj projesi. Flask ile yaptik.

## Ne var icinde?

Admin sirket/ilan ekliyor, ogrenci basvurup gunluk yaziyor, danisman onayliyor ve puan veriyor.
Ogrenci profil doldurup cv falan da yukleyebiliyor.

## Nasil calistirilir

```
git pull
pip install -r requirements.txt
python setup_db.py
python app.py
```

http://127.0.0.1:5000

## Giris (demo)

- admin@staj.edu.tr / admin123
- danisman@staj.edu.tr / danisman123
- ogr@staj.edu.tr / ogr123

## Dosyalar

- app.py - route lar burda
- models.py - db tablolari
- db_seed.py - ornek veri
- setup_db.py - db sifirla (sunumdan once calistir)
- templates/ - html ler
- static/css/style.css - css

## instance klasoru

Programi acinca olusuyor, icinde veritabani ve yuklenen dosyalar var. Git e gitmez normal.
Sorun olursa setup_db.py tekrar calistir.

## Uni adi degistirmek icin (istege bagli)

PowerShell:
```
$env:UNIVERSITY_NAME="Bizim Universite"
python app.py
```
