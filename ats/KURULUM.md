# ATS Kurulum – API Bağlantıları

Sistem hazırdır. Canlıya almak için yalnızca `api-config.js` doldurulur.

## 1. Barındırma
`index.html` ve `api-config.js` aynı klasörde, şirket içi bir adreste yayınlanır
(SharePoint, intranet, Azure Static Web Apps). claude.ai bağlantısı yalnızca demo içindir;
orada dış adreslere istek gönderilemez.

## 2a. Gmail ile e-posta (ücretsiz)
1. https://script.google.com → **Yeni proje** → `gmail-apps-script.gs` içeriğini yapıştırın.
2. `SECRET` değerini kendinize özel uzun bir şifreyle değiştirin → Kaydet.
3. **Dağıt → Yeni dağıtım** → tür: **Web uygulaması** → Yürüten: **Ben** → Erişimi olan: **Herkes** → Dağıt.
4. Google izin ister → hesabınızı seçin → *Gelişmiş → (proje adı)'na git* → İzin ver.
5. Çıkan `https://script.google.com/macros/s/.../exec` adresini kopyalayın.
6. `api-config.js`:
   ```js
   demo: false,
   gonderen: 'sizin.adresiniz@gmail.com',
   mail: { mode: 'gmail', url: 'https://script.google.com/macros/s/.../exec', key: 'SECRET ile aynı' },
   ```
7. `index.html`'i açın → **Entegrasyonlar → Test Maili Gönder**. Test maili gonderen adresine gelir.

Notlar:
- Kişisel Gmail ile günde yaklaşık 100 alıcıya, Google Workspace ile yaklaşık 1.500 alıcıya gönderim yapılabilir.
- Script kodunu değiştirirseniz yeni sürüm oluşturun: *Dağıt → Dağıtımları yönet → Düzenle → Yeni sürüm*.

## 2b. Outlook e-posta (Power Automate)
1. Power Automate → Yeni akış → **Anlık bulut akışı** → tetikleyici: *When an HTTP request is received*.
2. İstek gövdesi şeması:
   ```json
   {"type":"object","properties":{"from":{"type":"string"},"to":{"type":"string"},"subject":{"type":"string"},"text":{"type":"string"}}}
   ```
3. Adım ekle: *Office 365 Outlook → Send an email (V2)*. Kime = `to`, Konu = `subject`, Gövde = `text`.
4. Kaydedin, oluşan **HTTP POST URL**'sini `mail.url` alanına yapıştırın.

Not: HTTP tetikleyicisi Power Automate **Premium** lisansı gerektirir.

## 3. Outlook takvim (Power Automate)
Aynı yöntemle ikinci bir akış kurulur. Bu akışta adım olarak *Office 365 Outlook → Create event (V4)* seçilir.
Alanlar şöyle eşlenir: Başlık = `subject`, Başlangıç = `start`, Bitiş = `end`, Saat dilimi = `timeZone`,
Konum = `location`, Katılımcılar = `join(attendees, ';')`.
Oluşan URL'yi `calendar.url` alanına yapıştırın.

## 4. Sınav / envanter sağlayıcıları
Sağlayıcıdan API adresi, anahtar ve test numarası alınır, `assessments` altına girilir.
ATS şu çağrıları yapar:

| Çağrı | Gönderilen | Beklenen yanıt |
|---|---|---|
| `POST {url}/invitations` | `{test_id, candidate:{name,email}, reference, position}` | `{id, url}` |
| `GET {url}/results/{id}` | – | `{status, score, report_url, level, profile}` |

Sağlayıcının formatı farklıysa araya bir Power Automate akışı veya Azure Function konur ve bu formata çevrilir.
Tarayıcıdan doğrudan çağrı yapılabilmesi için sağlayıcının veya çevirici akışın CORS izni vermesi gerekir.

## 5. İK sistemi ve ilan siteleri (opsiyonel)
- `hris.url`: Aday "İşe Alındı" olunca bilgileri bu adrese POST edilir.
- `jobBoards.url`: "İlanlardan Başvuru Çek" butonu bu adresten başvuru listesini GET ile alır.

## 6. Canlıya geçiş
1. `yoneticiMail` alanına yöneticilerin e-posta adreslerini girin.
2. `demo: false` yapın.
3. Entegrasyonlar sayfasında **Bağlantıyı Test Et** ile kontrol edin.
