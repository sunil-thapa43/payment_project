import base64
import requests
from core.config import PaymentConfig
from payment.strategies.strategy import PaymentStrategy
from utils import base_64_encoder


class IMEPayPayment(PaymentStrategy):
    def __init__(self, **kwargs):
        self.service = "imepay"
        configs_class = PaymentConfig()
        self.configs = configs_class.get_credentials(self.service)

    def initiate_payment(self, amount, **kwargs):
        token_url = self.configs.get("token_url")
        username = self.configs.get("merchant_username")
        password = self.configs.get("merchant_password")
        merchant_module = self.configs.get("merchant_module")
        merchant_code = self.configs.get("merchant_code")
        transaction_id = kwargs.get("transaction_id")
        success_url = self.configs.get("success_url")
        failure_url = self.configs.get("failure_url")
        checkout_url = self.configs.get("checkout_url")
        auth = f"{username}:{password}"
        auth_encoded = base_64_encoder(auth)
        module_encoded = base_64_encoder(merchant_module)

        payload = {
            "MerchantCode": merchant_code,
            "Amount": amount,
            "RefId": transaction_id,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_encoded}",
            "Module": module_encoded,
        }
        response = requests.request(
            method="POST", url=token_url, data=payload, headers=headers
        )
        if response.status_code == 200:
            response_json = response.json()
            if response_json["ResponseCode"] == 0:
                token_id = response_json["TokenId"]
                ref_id = response_json["RefId"]
                amount = response_json["Amount"]
                payload_composition = f"{token_id}|{merchant_code}|{ref_id}|{amount}|GET|{success_url}|{failure_url}"
                payload_encoded = base_64_encoder(payload_composition)
                return ...


    def verify_payment(self, **kwargs):
        pass
