PANEL_MENUS = {
    'ogrenci': [
        ('ozet', 'Ana Sayfa', 'ti-home'),
        ('ilanlar', 'Staj İlanları', 'ti-building'),
        ('basvurularim', 'Başvurularım', 'ti-file-text'),
        ('gunluk', 'Staj Günlüğüm', 'ti-notebook'),
        ('degerlendirme', 'Değerlendirmem', 'ti-star'),
    ],
    'danisman': [
        ('ozet', 'Ana Sayfa', 'ti-home'),
        ('basvuru-onay', 'Başvuru Onayı', 'ti-briefcase'),
        ('gunluk-onay', 'Günlük Onayı', 'ti-notebook'),
        ('gecmis', 'Son İşlemler', 'ti-history'),
    ],
    'admin': [
        ('ozet', 'Ana Sayfa', 'ti-home'),
        ('ogrenciler', 'Öğrenciler', 'ti-users'),
        ('basvurular', 'Başvurular', 'ti-file-check'),
        ('sirketler', 'Şirketler', 'ti-building'),
        ('raporlar', 'Raporlar', 'ti-chart-bar'),
    ],
}

PANEL_TITLES = {
    'ogrenci': {
        'ozet': ('Ana Sayfa', 'Staj sürecine genel bakış'),
        'ilanlar': ('Staj İlanları', 'Şirket ilanlarına başvur'),
        'basvurularim': ('Başvurularım', 'Staj başvuru durumun'),
        'gunluk': ('Staj Günlüğüm', 'Günlük yaz ve kayıtlarını gör'),
        'degerlendirme': ('Değerlendirmem', 'Danışman onay durumları'),
    },
    'danisman': {
        'ozet': ('Ana Sayfa', 'Onay kuyruğu özeti'),
        'basvuru-onay': ('Başvuru Onayı', 'Staj başvurularını onayla veya reddet'),
        'gunluk-onay': ('Günlük Onayı', 'Öğrenci günlüklerini incele'),
        'gecmis': ('Son İşlemler', 'Geçmiş onay ve red kayıtları'),
    },
    'admin': {
        'ozet': ('Ana Sayfa', 'Sistem özeti ve rol açıklamaları'),
        'ogrenciler': ('Öğrenciler', 'Kayıtlı kullanıcılar'),
        'basvurular': ('Başvurular', 'Tüm staj başvuruları'),
        'sirketler': ('Şirketler', 'Şirket kaydı ve ilan yönetimi'),
        'raporlar': ('Raporlar', 'Sistem istatistikleri'),
    },
}

ROLE_LABELS = {
    'admin': 'Admin',
    'danisman': 'Danışman',
    'ogrenci': 'Öğrenci',
}


def panel_sections(role):
    return [item[0] for item in PANEL_MENUS.get(role, [])]
