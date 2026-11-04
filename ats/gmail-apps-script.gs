/* ATS → Gmail köprüsü (Google Apps Script)
   1) script.google.com → Yeni proje → bu kodu yapıştırın.
   2) SECRET değerini değiştirin; aynısını api-config.js → mail.key alanına yazın.
   3) Dağıt → Yeni dağıtım → Web uygulaması → Yürüten: Ben, Erişimi olan: Herkes.
   4) Oluşan .../exec URL'sini api-config.js → mail.url alanına yazın.            */

const SECRET = 'BURAYA-UZUN-BIR-SIFRE-YAZIN';
const SENDER_NAME = 'İnsan Kaynakları';

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    if (d.secret !== SECRET) return out({ ok: false, error: 'Yetkisiz istek (SECRET eşleşmiyor)' });
    if (!d.to || !d.subject) return out({ ok: false, error: 'Alıcı veya konu eksik' });
    const opt = { name: SENDER_NAME };
    if (d.from) opt.replyTo = d.from;
    GmailApp.sendEmail(d.to, d.subject, d.text || '', opt);
    return out({ ok: true });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

// Tarayıcıda URL'yi açınca kalan günlük gönderim kotasını gösterir
function doGet() {
  return out({ ok: true, kalanGunlukKota: MailApp.getRemainingDailyQuota() });
}

function out(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
