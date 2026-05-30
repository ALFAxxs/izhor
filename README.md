# Izhor Platform — 1-qadam: Modellar va Tuzilma

## Loyiha tuzilmasi

```
izhor/
├── apps/
│   ├── accounts/        # Foydalanuvchilar (User modeli)
│   ├── merchants/       # Do'konlar (Merchant, plan)
│   ├── templates_app/   # Shablonlar (IzhorTemplate, TemplateConfig, Category)
│   ├── qr_system/       # QR kodlar (QRCode, ScanLog) + utils
│   └── viewer/          # Public ko'rinish /i/<slug>
├── config/              # settings, urls
├── static/
├── media/
└── manage.py
```

## Modellar

| Model           | Vazifasi                                    |
|-----------------|---------------------------------------------|
| User            | Admin va merchant foydalanuvchilari         |
| Merchant        | Do'kon, plan (free/basic/premium/business)  |
| Category        | Sevgi, Do'stlik, Tug'ilgan kun...           |
| IzhorTemplate   | Shablon — asosiy yozuv                      |
| TemplateConfig  | Background, title, message, decorations     |
| AudioFile       | Merchant yuklagan musiqa fayllar            |
| QRCode          | Har bir shablon uchun unique slug + QR rasm |
| ScanLog         | Har bir scan logi (device, IP, vaqt)        |


