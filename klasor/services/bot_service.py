
from flask import Flask, request, render_template_string
import requests, random, string, traceback
from models.bot_model import BotModel
from models.finance_model import FinanceModel
from models.inventory_model import InventoryModel
from models.return_model import ReturnModel
from models.customer_model import CustomerModel

app = Flask(__name__)

# Modelleri tanımlıyoruz
db_bot = BotModel()
db_finance = FinanceModel()
db_inv = InventoryModel()
db_ret = ReturnModel()
db_cust = CustomerModel()

# NGROK ADRESİNİ BURAYA SABİT VE DOĞRU YAZ
MY_NGROK_URL = "https://parakeet-improve-garden.ngrok-free.app"



def send_meta_message(sender_id, text, page_access_token):
    try:
        response = requests.post(
            f"https://graph.facebook.com/v19.0/me/messages?access_token={page_access_token}",
            json={"recipient": {"id": sender_id}, "message": {"text": text}}
        )
        if response.status_code != 200:
            print(f"❌ [META GÖNDERİM HATASI]: {response.text}")
    except Exception as e:
        print(f"Sistemsel Gönderim Hatası: {e}")

# ============================================================
# 🤖 WEBHOOK VE BOT MANTIĞI
# ============================================================
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        settings = db_bot.get_bot_settings()
        if not settings:
            print("❌ HATA: Bot ayarları veritabanında bulunamadı!")
            return "Ayarlar eksik", 500

        # Verileri sırasıyla değil, güvenli sözlük (get) metoduyla çekiyoruz
        FB_PAGE_TOKEN = settings.get('fb_page_token', '')
        FB_VERIFY_TOKEN = settings.get('fb_verify_token', '')
        IG_PAGE_TOKEN = settings.get('ig_page_token', '')
        IG_VERIFY_TOKEN = settings.get('ig_verify_token', '')

        # --- 1. DOĞRULAMA (GET) ---
        if request.method == 'GET':
            incoming_token = request.args.get('hub.verify_token')
            if incoming_token in [FB_VERIFY_TOKEN, IG_VERIFY_TOKEN]:
                return request.args.get('hub.challenge'), 200
            return 'Doğrulama Başarısız', 403

        # --- 2. MESAJ İŞLEME (POST) ---
        if request.method == 'POST':
            data = request.json

            # 🔵 FACEBOOK'TAN GELEN MESAJLAR
            if data.get('object') == 'page':
                for entry in data['entry']:
                    for event in entry.get('messaging', []):
                        if event.get('message'):
                            # 🛑 YANKI FİLTRESİ: Eğer bu botun kendi gönderdiği mesajsa yoksay!
                            if event['message'].get('is_echo'):
                                continue

                            sender_id = event['sender']['id']
                            text = event['message'].get('text', '').lower()

                            print(f"📘 [FACEBOOK] Müşteri: {sender_id} | Mesaj: {text}")
                            cevap = process_facebook_bot(sender_id, text)
                            send_meta_message(sender_id, cevap, FB_PAGE_TOKEN)

            # 🟣 INSTAGRAM'DAN GELEN MESAJLAR
            elif data.get('object') == 'instagram':
                for entry in data['entry']:
                    for event in entry.get('messaging', []):
                        if event.get('message'):
                            # 🛑 YANKI FİLTRESİ: Eğer bu botun kendi gönderdiği mesajsa yoksay!
                            if event['message'].get('is_echo'):
                                continue

                            sender_id = event['sender']['id']
                            text = event['message'].get('text', '').lower()

                            print(f"📸 [INSTAGRAM] Müşteri: {sender_id} | Mesaj: {text}")
                            cevap = process_instagram_bot(sender_id, text)
                            send_meta_message(sender_id, cevap, IG_PAGE_TOKEN)

            return 'EVENT_RECEIVED', 200

    except Exception as e:
        print("\n❌ [BOT SUNUCUSU HATASI] ❌")
        traceback.print_exc()
        return "Internal Error", 500

    return 'EVENT_RECEIVED', 200
# ============================================================
# 🔵 1. FACEBOOK BOTUNUN BEYNİ
# ============================================================
def process_facebook_bot(sender_id, text):
    text = text.strip()

    if text in ['merhaba', 'selam', 'geri']:
        return ("📘 Facebook Mağazamıza Hoşgeldiniz!\n\n"
                "1 - Sipariş Durumu Sorgula\n"
                "2 - İade Talebi Oluştur\n"
                "3 - Ürünleri Listele ve Satın Al\n"
                "4 - Profil Bilgilerim\n\n"
                "💡 Menüye dönmek için 'GERI' yazabilirsiniz.")

    return ortak_bot_mantigi(sender_id, text)


# ============================================================
# 🟣 2. INSTAGRAM BOTUNUN BEYNİ
# ============================================================
def process_instagram_bot(sender_id, text):
    text = text.strip()

    if text in ['merhaba', 'selam', 'geri']:
        return ("📸 Instagram Butiğimize Hoşgeldiniz ✨\n\n"
                "1 ⭐ Sipariş Takibi\n"
                "2 ⭐ Kolay İade\n"
                "3 ⭐ Trend Ürünleri İncele\n"
                "4 ⭐ Bilgilerimi Düzenle\n\n"
                "DM üzerinden 7/24 hizmetinizdeyiz!")

    return ortak_bot_mantigi(sender_id, text)


# ============================================================
# ⚙️ ORTAK VERİTABANI VE İŞLEM MANTIĞI (Tüm komutlar burada)
# ============================================================
def ortak_bot_mantigi(sender_id, text):
    # 3. ÜRÜNLERİ LİSTELEME
    if text == '3':
        msg = "🛍️ Mevcut Ürünlerimiz:\n"
        for p in db_inv.get_inventory():
            if p['stock'] > 0:
                msg += f"ID: {p['id']} | {p['product_name']} | Fiyat: {p['price']} TL (Stok: {p['stock']})\n"
        msg += "\nSatın almak için: AL ÜrünID-KartNo-Ay-Yıl-CVV\nÖrnek: AL 1-5890040000000016-12-28-123\nAna menü: GERI"
        return msg

    # 4. PROFİL BİLGİLERİ
    elif text == '4':
        profile = db_cust.get_customer(sender_id)
        if profile:
            return f"👤 PROFİLİNİZ:\n📝 Ad: {profile['full_name']}\n📞 Tel: {profile['phone']}\n📍 Adres: {profile['address']}\n\nGüncellemek için:\nGÜNCELLE Ad Soyad - Tel - Adres"
        return "👤 Profil bulunamadı. Kayıt için yazın:\nGÜNCELLE Ad Soyad - Tel - Adres"

    # GÜNCELLE KOMUTU (Türkçe karakter uyumlu)
    elif text.startswith('guncelle ') or text.startswith('güncelle '):
        veri = text[9:].split('-')
        if len(veri) < 3: return "❌ Eksik format.\nKullanım: GÜNCELLE Ad Soyad - Tel - Adres"
        ad = veri[0].strip().title()
        tel = veri[1].strip()
        adres = "-".join(veri[2:]).strip().title()
        db_cust.save_or_update_customer(sender_id, ad, tel, adres)
        return f"✅ Profil Güncellendi!\n📝 {ad}\nArtık '3' yazarak alışveriş yapabilirsiniz."

    # AL KOMUTU (Satın Alma)
        # AL KOMUTU (Sadece Ürün ID ile çalışır)
        # AL KOMUTU
    elif text.startswith('al '):
        profile = db_cust.get_customer(sender_id)
        if not profile: return "❌ Önce profil oluşturun! Yazın: GÜNCELLE Ad Soyad - Tel - Adres"

        urun_id_str = text[3:].strip()
        if not urun_id_str.isdigit(): return "❌ Hatalı format. Örn: AL 1"

        try:
            p_id = int(urun_id_str)
            product = db_inv.get_inventory()
            sel = next((p for p in product if p['id'] == p_id), None)

            if sel and sel['stock'] > 0:
                # DİKKAT: Ngrok adresini kendininki ile değiştir!
                sunucu_adresi = "https://parakeet-improve-garden.ngrok-free.dev"

                # Müşteriye İyzico yerine kendi sitemizin (Ngrok) linkini gönderiyoruz
                odeme_linki = f"{sunucu_adresi}/odeme/{p_id}?uid={sender_id}"

                return f"🛒 {sel['product_name']} siparişiniz oluşturuldu.\n\n🔒 Ödemenizi güvenle tamamlamak için aşağıdaki linke tıklayın:\n{odeme_linki}"

            return "❌ Ürün stoklarda tükendi veya hatalı ID."
        except Exception as e:
            print(f"Sipariş Oluşturma Hatası: {e}")
            return "❌ İşlem başarısız, lütfen tekrar deneyin."
    # 1. SİPARİŞ DURUMU
    elif text == '1':
        orders = db_ret.get_customer_orders(sender_id)
        if not orders: return "❌ Size ait sipariş bulunamadı.\nAna menü: GERI"
        msg = "📦 SİPARİŞ DURUMUNUZ:\n\n"
        for o in orders: msg += f"🔹 Ürün: {o['product_name']}\n📌 Durum: {o['status']}\n---\n"
        return msg + "Ana menü: GERI"

    # 2. İADE EDİLEBİLİR SİPARİŞLER
    elif text == '2':
        orders = db_ret.get_customer_orders(sender_id)
        if not orders: return "❌ İade edilebilecek siparişiniz yok.\nAna menü: GERI"
        msg = "🔄 İADE EDİLEBİLİR SİPARİŞLER:\n\n"
        for o in orders: msg += f"Sipariş No: {o['id']} | {o['product_name']}\n"
        return msg + "\nİade talebi oluşturmak için yazın:\nİADE-SiparişNo"

    # İADE TALEBİ OLUŞTURMA (Türkçe karakter uyumlu)
    elif text.startswith('iade-') or text.startswith('i̇ade-') or text.startswith('ıade-'):
        try:
            o_id = int(text.split('-')[1].strip())
            orders = db_ret.get_customer_orders(sender_id)
            sel = next((o for o in orders if o['id'] == o_id), None)
            if sel:
                code = "IADE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                db_ret.add_return_request(sel['id'], code)
                return f"✅ İade Kodu: {code}\nLütfen paketin üzerine bu kodu yazınız.\nAna menü: GERI"
            return "❌ Sipariş bulunamadı veya size ait değil."
        except Exception as e:
            print(f"İade Hatası: {e}")
            return "❌ Hatalı format. Örnek: İADE-1"

    # BİLİNMEYEN KOMUTLAR
    else:
        return "Lütfen geçerli bir seçim yapın. Ana menüye dönmek için 'GERI' yazabilirsiniz."


@app.route('/odeme/<int:p_id>', methods=['GET'])
def odeme_sayfasi(p_id):
    sender_id = request.args.get('uid')
    if not sender_id: return "Geçersiz işlem", 400

    sel = next((p for p in db_inv.get_inventory() if p['id'] == p_id), None)
    profile = db_cust.get_customer(sender_id)

    if not sel or not profile:
        return "❌ Ürün bulunamadı veya profil eksik.", 404

    # İyzico form kodunu al
    form_script = db_finance.create_checkout_form(
        p_id, sel['product_name'], sel['price'],
        sender_id, profile['full_name'], profile['phone'], profile['address'],
        MY_NGROK_URL
    )

    if not form_script:
        return "❌ Ödeme altyapısına şu an ulaşılamıyor."

    return render_template_string("""
    <!DOCTYPE html><html><body>
    <h2>💳 Güvenli Ödeme</h2>
    <div id="iyzipay-checkout-form" class="responsive"></div>
    {{ form_script|safe }}
    </body></html>""", form_script=form_script)


# ============================================================
# 💳 İYZİCO ÖDEME SONUCU (Düzeltildi)
# ============================================================
@app.route('/odeme-sonuc', methods=['POST'])  # Sadece POST yapalım
def odeme_sonuc():
    print("📢 İyzico POST isteği geldi!")

    # İyzico token'ı POST form verisi içinde gönderir
    token = request.form.get('token')

    if not token:
        # Eğer POST gelmezse, terminalde hatayı görelim
        print("❌ HATA: Token POST ile gelmedi!")
        return "Token eksik", 400

    # 2. İyzico'dan onayı al
    result = db_finance.check_payment_result(token)

    if result and result.get('status') == 'success':
        # ... (Sipariş kaydetme kodların aynı kalsın) ...
        # Siparişi kaydedince müşteriye şık bir mesaj dön
        return render_template_string("<h1>✅ Ödeme Başarılı!</h1><p>Siparişiniz kaydedildi.</p>")

    return "❌ Ödeme onaylanamadı.", 400


# ============================================================
# 📄 FATURA GÖRÜNTÜLEME
# ============================================================
@app.route('/fatura/<invoice_no>', methods=['GET'])
def goster_fatura(invoice_no):
    fatura = db_finance.db.get_order_by_invoice(invoice_no)
    if not fatura: return "❌ Fatura bulunamadı.", 404
    # ... (Mevcut fatura HTML şablonunu buraya ekle) ...
    return "Fatura sayfası"


if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)