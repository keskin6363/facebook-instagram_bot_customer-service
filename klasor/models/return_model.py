from database.db_manager import DBManager
import json
class ReturnModel:
    def __init__(self): self.db = DBManager()
    def get_returns(self): return self.db.get_all_returns()
    def add_return_request(self, order_id, return_code): self.db.insert_return(order_id, return_code)
    def update_return_status(self, return_id, new_status):
        ret_data = self.db.get_return_by_id(return_id)
        if ret_data and ret_data['status'] != new_status:
            self.db.update_return_status(return_id, new_status)
            if new_status == "Kargo Alındı / Depoya Yolda":
                order = self.db.get_order_for_refund(ret_data['order_id'])
                if order and order['invoice_no']:
                    import iyzipay, uuid
                    iyz_conf = self.db.get_api_key('iyzico')
                    options = {'api_key': iyz_conf['api_key'], 'secret_key': iyz_conf['secret_key'], 'base_url': iyz_conf['base_url']}
                    req = {'locale': 'tr', 'conversationId': str(uuid.uuid4()), 'paymentTransactionId': order['invoice_no'], 'price': str(order['price']), 'currency': 'TRY', 'ip': '85.34.78.112'}
                    refund = iyzipay.Refund().create(req, options)
                    res = json.loads(refund.read().decode('utf-8'))
                    if res.get('status') == 'success': self.db.update_order_status(order['id'], 'İade Tamamlandı (Para İade Edildi)')
    def get_customer_orders(self, customer_id): return self.db.get_customer_orders_for_bot(customer_id)