import iyzipay
import json
from datetime import datetime
from database.db_manager import DBManager


class FinanceModel:
    def __init__(self):
        self.db = DBManager()

    # ==========================================
    # 1. TEMEL FİNANS VE SİPARİŞ İŞLEMLERİ (MVC)
    # ==========================================
    def get_orders(self):
        """Arayüzdeki siparişler tablosunu doldurur"""
        return self.db.get_all_orders()

    def get_expenses(self):
        """Arayüzdeki masraflar tablosunu doldurur"""
        return self.db.get_all_expenses()

    def add_expense(self, name, amount):
        """Yeni masraf ekler"""
        try:
            self.db.insert_expense(name, amount)
            return True
        except Exception as e:
            print(f"Masraf ekleme hatası: {e}")
            return False

    def update_invoice_number(self, order_id, invoice_no):
        """Siparişe fatura numarası işler"""
        try:
            self.db.update_order_invoice(order_id, invoice_no)
            return True
        except Exception as e:
            print(f"Fatura güncelleme hatası: {e}")
            return False

    def assign_tracking_code(self, order_id, tracking_code):
        """Siparişe kargo takip kodu atar"""
        try:
            self.db.update_order_tracking(order_id, tracking_code)
            return True
        except Exception as e:
            print(f"Kargo kodu atama hatası: {e}")
            return False

    def get_financial_summary(self):
        """Finans ekranındaki Günlük/Aylık kazanç panolarını hesaplar"""
        orders = self.db.get_all_orders() or []
        expenses = self.db.get_all_expenses() or []
        # Not: Basitlik için iade tutarlarını da orders üzerinden statüye göre hesaplıyoruz

        today_str = datetime.now().strftime("%d.%m.%Y")
        month_str = datetime.now().strftime(".%m.%Y")

        d_sales = sum(float(o.get('price', 0)) for o in orders if
                      o.get('date', '').startswith(today_str) and o.get('status') != 'İade Edildi')
        m_sales = sum(float(o.get('price', 0)) for o in orders if
                      month_str in o.get('date', '') and o.get('status') != 'İade Edildi')

        d_exp = sum(float(e.get('amount', 0)) for e in expenses if e.get('date', '').startswith(today_str))
        m_exp = sum(float(e.get('amount', 0)) for e in expenses if month_str in e.get('date', ''))

        d_returns = sum(float(o.get('price', 0)) for o in orders if
                        o.get('date', '').startswith(today_str) and o.get('status') == 'İade Edildi')
        m_returns = sum(float(o.get('price', 0)) for o in orders if
                        month_str in o.get('date', '') and o.get('status') == 'İade Edildi')

        d_net = d_sales - d_returns - d_exp
        m_net = m_sales - m_returns - m_exp

        return {
            'd_sales': d_sales, 'm_sales': m_sales,
            'd_returns': d_returns, 'm_returns': m_returns,
            'd_net': d_net, 'm_net': m_net,
            'd_exp': d_exp, 'm_exp': m_exp
        }

    # ==========================================
    # 2. İYZİCO ÖDEME SİSTEMİ ENTEGRASYONU
    # ==========================================
    def create_checkout_form(self, product_id, product_name, price, customer_id, full_name, phone, address,
                             sunucu_adresi):
        """İyzico Checkout Form scriptini (HTML kodunu) üretir"""
        import time
        zaman = int(time.time())

        api_data = self.db.get_api_key('iyzico')
        if not api_data: return None

        options = {
            'api_key': api_data['api_key'],
            'secret_key': api_data['secret_key'],
            'base_url': api_data['base_url']
        }

        isim_parcalari = full_name.split()
        isim = isim_parcalari[0]
        soyisim = isim_parcalari[-1] if len(isim_parcalari) > 1 else 'Müşteri'

        request_data = {
            'locale': 'tr',
            'conversationId': f"{customer_id}-{product_id}-{zaman}",
            'price': str(price),
            'paidPrice': str(price),
            'currency': 'TRY',
            'basketId': f"BSK-{product_id}-{zaman}",
            'paymentGroup': 'PRODUCT',
            'callbackUrl': f"{sunucu_adresi.replace('https://', 'https://')}/odeme-sonuc",
            'enabledInstallments': ['2', '3', '6', '9'],
            'buyer': {
                'id': str(customer_id),
                'name': isim, 'surname': soyisim, 'gsmNumber': phone,
                'email': 'musteri@sistem.com', 'identityNumber': '11111111111',
                'registrationAddress': address, 'ip': '85.34.78.112',
                'city': 'Sanliurfa', 'country': 'Turkey',
            },
            'shippingAddress': {
                'contactName': full_name, 'city': 'Sanliurfa', 'country': 'Turkey', 'address': address
            },
            'billingAddress': {
                'contactName': full_name, 'city': 'Sanliurfa', 'country': 'Turkey', 'address': address
            },
            'basketItems': [
                {'id': str(product_id), 'name': product_name, 'category1': 'Genel', 'itemType': 'PHYSICAL',
                 'price': str(price)}
            ]
        }

        checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request_data, options)
        response_json = json.loads(checkout_form_initialize.read().decode('utf-8'))

        if response_json.get('status') == 'success':
            return response_json.get('checkoutFormContent')
        else:
            print(f"❌ İyzico Link Hatası: {response_json.get('errorMessage')}")
            return None

    def check_payment_result(self, token):
        """İyzico'dan dönen token ile ödemenin sonucunu sorgular"""
        api_data = self.db.get_api_key('iyzico')
        if not api_data: return None

        options = {
            'api_key': api_data['api_key'],
            'secret_key': api_data['secret_key'],
            'base_url': api_data['base_url']
        }

        request_data = {'locale': 'tr', 'token': token}

        checkout_form_result = iyzipay.CheckoutForm().retrieve(request_data, options)
        return json.loads(checkout_form_result.read().decode('utf-8'))