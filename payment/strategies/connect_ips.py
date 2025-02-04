from datetime import datetime

from requests.auth import HTTPBasicAuth

from core.config import PaymentConfig
from payment.strategies.strategy import PaymentStrategy
from utils import get_encoded_token_cips, generate_transaction_id
import requests


class ConnectIPSPayment(PaymentStrategy):
    def __init__(self, **kwargs):
        self.service = "connect_ips"
        self.configs = PaymentConfig(self.service)

    def initiate_payment(self, amount, **kwargs):
        """
        ConnectIPS provides credentials files to each of businesses that request ConnectIPS payment partnership.

        """
        merchant_id = self.configs.merchant_id
        client_id = self.configs.client_id
        client_secret = self.configs.client_secret
        app_id = self.configs.app_id
        app_name = self.configs.app_name
        transaction_id = generate_transaction_id()
        transaction_date = datetime.now().strftime("%d-%m-%Y")
        reference_id = transaction_id
        remarks = kwargs.get("remarks")
        particulars = "PAR-" + transaction_id[:4]
        token = "some_random_token_for_now"
        token_string = f"MERCHANT_ID={merchant_id},APP_ID={app_id},APP_NAME={app_name},TXNID={transaction_id},TXNDATE={transaction_date},TXNCRNCY=NPR,TXNAMT={amount},REFERENCEID={reference_id}, REMARKS={remarks},PARTICULARS={particulars},TOKEN={token}"

    def verify_payment(self, **kwargs):
        cert_path = self.configs.cert_path
        password = self.configs.password
        verify_url = self.configs.verify_url
        reference_id = kwargs.get("reference_id")
        total_amount = kwargs.get("total_amount")

        merchant_id = self.configs.merchant_id
        app_id = self.configs.app_id

        # transaction amount is in paisa initially
        transaction_amount = float(total_amount) * 100
        token = f"MERCHANT_ID={merchant_id},APPID={app_id},REFERENCE_ID={reference_id},TXNAMT={transaction_amount}"
        encoded_token = get_encoded_token_cips(token, cert_path)
        payload = {
            "merchantId": merchant_id,
            "appId": app_id,
            "referenceId": reference_id,
            "txnAmt": transaction_amount,
            "token": encoded_token,
        }
        # response = requests.get(
        #     "https://api.example.com/data",
        #     auth=HTTPBasicAuth(username, password)
        # )
        #
        # print(response.status_code)
        # print(response.json())
        response = requests.post(url=verify_url, data=payload, auth=HTTPBasicAuth(merchant_id, password))
        if response.status_code != 200:
            # maybe retry once or twice
            return False
        else:
            status = response.json()
            if status["status"] == "SUCCESS":
                return True
            return False


