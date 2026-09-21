from database.db_connection import DBConnection

class DBManager:
    def __init__(self):
        self.db = DBConnection()

    def _execute(self, query, params=(), fetch=False, fetch_one=False):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if fetch: return cursor.fetchone() if fetch_one else cursor.fetchall()
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    # ==========================================
    # API VE BOT SORGULARI
    # ==========================================
    def get_api_key(self, service_name):
        return self._execute("SELECT api_key, secret_key, base_url FROM api_keys WHERE service_name=%s", (service_name,), True, True)

    def get_bot_settings(self):
        return self._execute("SELECT page_token, verify_token FROM bot_settings ORDER BY id DESC LIMIT 1", fetch=True, fetch_one=True)

    # ==========================================
    # ENVANTER (INVENTORY) SORGULARI
    # ==========================================
    def get_all_inventory(self):
        return self._execute("SELECT * FROM vw_inventory_details ORDER BY id DESC", fetch=True)

    def insert_inventory(self, name, price, stock, barcode):
        return self._execute("INSERT INTO inventory (product_name, price, stock, barcode) VALUES (%s, %s, %s, %s)", (name, price, stock, barcode))

    def update_inventory(self, p_id, name, price, barcode):
        self._execute("UPDATE inventory SET product_name=%s, price=%s, barcode=%s WHERE id=%s", (name, price, barcode, p_id))

    def delete_inventory(self, p_id):
        self._execute("DELETE FROM inventory WHERE id=%s", (p_id,))

    def get_product_by_barcode(self, barcode):
        query = "SELECT id, stock FROM inventory WHERE barcode = %s"
        return self._execute(query, (barcode,), fetch=True, fetch_one=True)

    def update_inventory_stock(self, product_id, stock_to_add, new_price):
        query = "UPDATE inventory SET stock = stock + %s, price = %s WHERE id = %s"
        self._execute(query, (stock_to_add, new_price, product_id))

    def insert_inventory_product(self, barcode, product_name, price, stock):
        query = "INSERT INTO inventory (barcode, product_name, price, stock) VALUES (%s, %s, %s, %s)"
        self._execute(query, (barcode, product_name, price, stock))
        id_query = "SELECT id FROM inventory WHERE barcode = %s"
        return self._execute(id_query, (barcode,), fetch=True, fetch_one=True)['id']

    def update_inventory_product(self, product_id, product_name, price, barcode):
        query = "UPDATE inventory SET product_name = %s, price = %s, barcode = %s WHERE id = %s"
        self._execute(query, (product_name, price, barcode, product_id))

    def delete_inventory_product(self, product_id):
        query = "DELETE FROM inventory WHERE id = %s"
        self._execute(query, (product_id,))

    # ==========================================
    # SERİ NUMARASI SORGULARI
    # ==========================================
    def get_serial_numbers(self, p_id):
        return self._execute("SELECT serial_no, status FROM product_serials WHERE product_id=%s ORDER BY id DESC", (p_id,), fetch=True)

    def get_serials_by_product_id(self, product_id):
        query = "SELECT serial_no, status FROM product_serials WHERE product_id = %s"
        return self._execute(query, (product_id,), fetch=True)

    def insert_product_serial(self, serial_no, product_id):
        query = "INSERT INTO product_serials (serial_no, product_id, status) VALUES (%s, %s, 'Mevcut')"
        self._execute(query, (serial_no, product_id))

    def get_serial_number(self, serial_no):
        query = "SELECT serial_no FROM product_serials WHERE serial_no = %s"
        return self._execute(query, (serial_no,), fetch=True, fetch_one=True)

    def get_available_serial(self, p_id):
        return self._execute("SELECT serial_no FROM product_serials WHERE product_id=%s AND status='Mevcut' LIMIT 1", (p_id,), True, True)

    # ==========================================
    # PERSONEL VE KULLANICI (AUTH) SORGULARI
    # ==========================================
    def get_all_personnel(self):
        return self._execute("SELECT * FROM vw_personnel_details ORDER BY id DESC", fetch=True)

    def insert_personnel(self, full_name, email, password_hash, role, salary, bank_iban):
        query = "INSERT INTO users (full_name, email, password_hash, role, salary, bank_iban) VALUES (%s, %s, %s, %s, %s, %s)"
        self._execute(query, (full_name, email, password_hash, role, salary, bank_iban))

    def update_personnel(self, p_id, n, e, r, s, b):
        self._execute("UPDATE users SET full_name=%s, email=%s, role=%s, salary=%s, bank_iban=%s WHERE id=%s", (n, e, r, s, b, p_id))

    def delete_personnel(self, p_id):
        self._execute("DELETE FROM users WHERE id=%s", (p_id,))

    def get_user_by_email(self, email):
        query = "SELECT password_hash, role FROM users WHERE email = %s"
        return self._execute(query, (email,), fetch=True, fetch_one=True)

    def update_user_password(self, email, new_password_hash):
        query = "UPDATE users SET password_hash = %s WHERE email = %s"
        self._execute(query, (new_password_hash, email))

    # ==========================================
    # SİPARİŞ VE FİNANS SORGULARI
    # ==========================================
    def get_all_orders(self):
        return self._execute("SELECT * FROM vw_order_details ORDER BY id DESC", fetch=True)

    def insert_order(self, c_id, p_id, b_info, price, inv, serial):
        self._execute("INSERT INTO orders (customer_id, product_id, billing_info, price, invoice_no, serial_number) VALUES (%s, %s, %s, %s, %s, %s)", (c_id, p_id, b_info, price, inv, serial))

    def update_order_invoice(self, o_id, inv):
        self._execute("UPDATE orders SET invoice_no=%s WHERE id=%s", (inv, o_id))

    def update_order_tracking(self, o_id, tk):
        self._execute("UPDATE orders SET tracking_code=%s, status='Kargoya Verildi' WHERE id=%s", (tk, o_id))

    def get_order_for_refund(self, o_id):
        return self._execute("SELECT id, product_id, invoice_no, price, serial_number FROM orders WHERE id=%s", (o_id,), True, True)

    def update_order_status(self, o_id, st):
        self._execute("UPDATE orders SET status=%s WHERE id=%s", (st, o_id))

    def get_all_expenses(self):
        return self._execute("SELECT * FROM vw_expense_details ORDER BY id DESC", fetch=True)

    def insert_expense(self, name, amount):
        self._execute("INSERT INTO expenses (expense_name, amount) VALUES (%s, %s)", (name, amount))

    # ==========================================
    # İADE VE MÜŞTERİ SORGULARI
    # ==========================================
    def get_all_returns(self):
        return self._execute("SELECT * FROM vw_return_details ORDER BY return_id DESC", fetch=True)

    def insert_return(self, o_id, code):
        self._execute("INSERT INTO returns (order_id, return_code, status) VALUES (%s, %s, 'Kargo Bekleniyor')", (o_id, code))
        self._execute("UPDATE orders SET status='İade Talebi Alındı' WHERE id=%s", (o_id,))

    def get_return_by_id(self, r_id):
        return self._execute("SELECT order_id, status FROM returns WHERE id=%s", (r_id,), True, True)

    def update_return_status(self, r_id, st):
        self._execute("UPDATE returns SET status=%s WHERE id=%s", (st, r_id))

    def get_customer_orders_for_bot(self, c_id):
        return self._execute("SELECT o.id, i.product_name, o.price, o.status FROM orders o JOIN inventory i ON o.product_id = i.id WHERE o.customer_id=%s ORDER BY o.id DESC", (c_id,), True)

    def get_customer(self, f_id):
        return self._execute("SELECT full_name, phone, address FROM customers WHERE facebook_id=%s", (f_id,), True, True)

    def upsert_customer(self, f_id, fn, ph, ad):
        self._execute("INSERT INTO customers (facebook_id, full_name, phone, address) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE full_name=%s, phone=%s, address=%s", (f_id, fn, ph, ad, fn, ph, ad))

    def get_order_by_invoice(self, invoice_no):
        """Fatura numarasına göre sipariş, müşteri ve ürün detaylarını getirir"""
        query = """
            SELECT o.invoice_no, o.order_date, o.price, o.billing_info, o.serial_number,
                   c.full_name, c.phone, 
                   i.product_name 
            FROM orders o
            JOIN customers c ON o.customer_id = c.facebook_id
            JOIN inventory i ON o.product_id = i.id
            WHERE o.invoice_no = %s
        """
        return self._execute(query, (invoice_no,), fetch=True, fetch_one=True)
