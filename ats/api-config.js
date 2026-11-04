/* =====================================================================
   ATS – API BAĞLANTI DOSYASI
   Sistemin tamamı hazırdır; yalnızca bu dosyadaki URL ve anahtarları
   doldurun, ardından demo: false yapın. Ayrıntılı kurulum: KURULUM.md
   ===================================================================== */
window.ATS_CONFIG = {
  // true: tüm bağlantılar simüle edilir (mail gönderilmez, sınav sonuçları örnektir)
  // false: aşağıdaki gerçek bağlantılar kullanılır
  demo: true,

  sirket: 'Şirketiniz A.Ş.',
  gonderen: 'ik@sirketiniz.com',

  // Aday "Sınav Aşaması"na geçince 3 sınav daveti otomatik oluşturulsun mu?
  autoInvite: true,

  // 1) E-POSTA – tüm otomatik bilgilendirme mailleri (Gmail için: gmail-apps-script.gs ve KURULUM.md)
  //    Power Automate: "When an HTTP request is received" → "Send an email (V2)"
  //    Gelen veri: { from, to, subject, text }
  mail: {
    mode: 'webhook',          // 'gmail' (Google Apps Script) | 'webhook' (Power Automate/Outlook) | 'mailto' (taslak açar)
    url: '',                  // gmail: Apps Script .../exec URL'si  |  webhook: Power Automate HTTP POST URL'si
    key: ''                   // gmail: script içindeki SECRET ile aynı  |  webhook: gerekmiyorsa boş
  },

  // 2) OUTLOOK TAKVİM – "Mülakat Planla" ile aday + görüşmeciye toplantı daveti
  //    Power Automate: "When an HTTP request is received" → "Create event (V4)"
  //    Gelen veri: { subject, start, end, timeZone, location, online, attendees[], body }
  calendar: { url: '', key: '' },

  // 3) SINAV / ENVANTER SAĞLAYICILARI
  //    POST {url}/invitations  → { id, url }
  //    GET  {url}/results/{id} → { status: 'pending'|'completed', score, report_url, level, profile }
  //    Sağlayıcı formatı farklıysa araya Power Automate / Azure Function çevirici konur.
  assessments: {
    eng: { name: 'İngilizce Sınavı Sağlayıcısı', url: '', key: '', test: '', min: 60 },
    apt: { name: 'Genel Yetenek Sağlayıcısı',    url: '', key: '', test: '', min: 50 },
    per: { name: 'Kişilik Envanteri Sağlayıcısı', url: '', key: '', test: '', min: 0 }
  },

  // 4) İK SİSTEMİ (SuccessFactors vb.) – aday "İşe Alındı" olunca bilgileri gönderilir
  //    Gelen veri: { talepNo, aday, tc, email, tel, pozisyon, lokasyon, direktorluk, mudurluk, yonetici, baslangic, kaynak }
  hris: { url: '', key: '' },

  // 5) İLAN SİTELERİ (Kariyer.net, LinkedIn vb.) – "İlanlardan Başvuru Çek" butonu
  //    GET {url} → [ { talepNo, ad, email, tel, kaynak, kvkk } ]
  jobBoards: { url: '', key: '' },

  // Yönetici bildirimleri ve takvim davetleri için ad → e-posta eşleştirmesi
  yoneticiMail: {
    'Yönetici 1': 'yonetici1@sirketiniz.com',
    'Yönetici 2': 'yonetici2@sirketiniz.com'
  }
};
