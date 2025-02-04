import base64

import requests
from core.config import PaymentConfig
from payment.strategies.strategy import PaymentStrategy
from utils import generate_transaction_id


class IMEPayPayment(PaymentStrategy):
    def __init__(self, **kwargs):
        self.service = "ime_pay"
        self.configs = PaymentConfig(self.service)

    def initiate_payment(self, amount, **kwargs):
        initiate_url = self.configs.initiate_url
        transaction_id = generate_transaction_id()
        merchant_code = self.configs.merchant_code
        username = self.configs.username
        password = self.configs.password
        ime_merchant_module = self.configs.ime_merchant_module
        payload = {
            "MerchantCode": merchant_code,
            "Amount": amount,
            "RefId": transaction_id,
        }
        auth = f"{username}:{password}"
        auth_encoded = base64.b64encode(auth.encode()).decode()
        module_encoded = base64.b64encode(ime_merchant_module.encode()).decode()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}",
            "Module": module_encoded,
        }
        response = requests.request(
            method="POST", url=initiate_url, data=payload, headers=headers
        )
        pass

    def verify_payment(self, **kwargs):
        pass
