from datetime import datetime
from django.db import transaction
from requests.auth import HTTPBasicAuth

from payment.models import PaymentRequest
from payment.views import handle_grpc_write
from utils.config import PaymentConfig
from payment.strategies.strategy import PaymentStrategy
from utils.utils import sign_connect_ips_message, \
    payment_request_with_retry


class ConnectIPSPayment(PaymentStrategy):
    def __init__(self, **kwargs):
        self.service = "connect_ips"
        config_class = PaymentConfig()
        self.configs = config_class.get_credentials(self.service)

    def initiate_payment(self, obj, **kwargs):
        """
        ConnectIPS provides credentials files to each of businesses that request ConnectIPS payment partnership.
        """
        merchant_id = self.configs.get("merchant_id")
        cert_path = self.configs.get("cert_path")
        password = self.configs.get("password")
        app_id = self.configs.get("app_id")
        app_name = self.configs.get("app_name")
        transaction_id = obj.transaction_id
        amount = obj.amount
        transaction_date = datetime.now().strftime("%d-%m-%Y")
        reference_id = transaction_id
        remarks = kwargs.get("remarks")
        particulars = "PAR-" + transaction_id[:4]
        token = self.configs.get("token")
        message_to_be_signed = f"""
            MERCHANT_ID={merchant_id},
            APP_ID={app_id},APP_NAME={app_name},
            TXNID={transaction_id},
            TXNDATE={transaction_date},
            TXNCRNCY=NPR,
            TXNAMT={amount},
            REFERENCEID={reference_id}, 
            REMARKS={remarks},
            PARTICULARS={particulars},
            TOKEN={token}"""
        token = sign_connect_ips_message(
            cips_message=message_to_be_signed,
            certificate_path=cert_path,
            certificate_password=password
        )
        body = {
            "MERCHANT_ID": merchant_id,
            "APPID": app_id,
            "APPNAME": app_name,
            "TXNID": transaction_id,
            "TXNDATE": transaction_date,
            "TXNCRNCY": "NPR",
            "TXNAMT": obj.amount,
            "REFERENCEID": reference_id,
            "REMARKS": remarks,
            "PARTICULARS": particulars,
            "TOKEN": token,
        }
        return body

    def verify_payment(self, **kwargs):
        cert_path = self.configs.get("cert_path")
        password = self.configs.get("basic_auth_password")
        username = self.configs.get("basic_auth_username")
        verify_url = self.configs.get("verify_url")
        merchant_id = self.configs.get("merchant_id")
        app_id = self.configs.get("app_id")

        # we get TXNID from the success url
        transaction_ = kwargs.get("txn_id")
        transactions = PaymentRequest.objects.filter(transaction_id=transaction_)
        if not transactions:
            return False

        transaction_obj = transactions.first()
        total_amount = transaction_obj.amount
        reference_id = transaction_obj.transaction_id
        # transaction amount is in paisa initially
        transaction_amount = float(total_amount) * 100
        token = f"""
            MERCHANT_ID={merchant_id},
            APPID={app_id},
            REFERENCE_ID={reference_id},
            TXNAMT={transaction_amount}
            """
        encoded_token = sign_connect_ips_message(
            cips_message=token,
            certificate_path=cert_path,
            certificate_password=password
        )
        payload = {
            "merchantId": merchant_id,
            "appId": app_id,
            "referenceId": reference_id,
            "txnAmt": transaction_amount,
            "token": encoded_token,
        }
        response, status = payment_request_with_retry(
            method="POST",
            url=verify_url,
            data=payload,
            auth=HTTPBasicAuth(
                username=username,
                password=password
            )
        )
        if response.status_code != 200:
            return False
        status = response.json()
        if status["status"] != "SUCCESS":
            return False
        # the payment is success, now we need to:
        # a. Set Payment Request Status to Completed, save the obj
        # b. Create an entry to Payment Table
        # c. gRPC call to Admin Service to update their Payment Table -> we send them transaction id
        handle_grpc_write(payment_request_obj=transaction_obj)
        return True
