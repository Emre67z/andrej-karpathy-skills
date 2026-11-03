# EPİAŞ Piyasa Mesaj Sistemi Raporu

Piyasa Mesaj Sistemi verilerini her 60 saniyede bir EPİAŞ Şeffaflık API'sinden çeken rapor arayüzü.

## Çalıştırma

```bash
python3 server.py
```

Tarayıcıda http://localhost:8000 adresini açın ve EPİAŞ Şeffaflık hesabınızla giriş yapın.
Yalnızca Python 3 gerekir; ek paket kurulumu yoktur.

## Neden küçük bir sunucu var?

EPİAŞ API'si tarayıcıdan doğrudan yapılan isteklere izin vermez (CORS). `server.py`:
- `index.html` dosyasını yayınlar,
- girişte `giris.epias.com.tr` üzerinden TGT alır ve süresi dolunca yeniler,
- `/api/...` isteklerine `TGT` başlığını ekleyip EPİAŞ'a iletir.

Kullanıcı adı ve şifre yalnızca sunucu çalıştığı sürece bellekte tutulur, diske yazılmaz.

## Kullanılan servisler

| Servis | Yöntem | Yol |
|---|---|---|
| Piyasa mesajları | POST | `v1/markets/data/market-message-system` |
| Dışa aktarma (XLSX/CSV/PDF) | POST | `v1/markets/export/market-message-system` |
| Mesaj tipleri | GET | `v1/markets/data/umm-message-type-list` |
| Organizasyona göre santraller | POST | `v1/markets/data/power-plant-list-by-organization-id` |
