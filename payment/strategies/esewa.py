import base64
import json

from core.config import PaymentConfig
from payment.models import PaymentRequest
from payment.strategies.strategy import PaymentStrategy
from utils import generate_transaction_id


class EsewaPayment(PaymentStrategy):
    def __init__(self):
        self.service = "esewa"
        self.config = PaymentConfig()
        self.configs = self.config.get_credentials(self.service)

    def initiate_payment(self, amount, **kwargs):
        """
        Esewa provides some creds to the business (Mutual Fund) in our case, we encode our message with that key and
        send the end-user to Esewa platform with that message.
        End-User completes/cancels/gets-rejected for that payment, Esewa hits our success or failure url respectively
        with an encoded message which we decode and check on our end.
        """
        product_code = kwargs.get("product_code")
        transaction_id = generate_transaction_id()
        secret_key = self.configs["secret_key"]
        success_url = self.configs["success_url"]
        failure_url = self.configs["failure_url"]
        body = {
            "transaction_id": transaction_id,
            "product_code": product_code,
            "amount": amount,
            "secret_key": secret_key,
            "success_url": success_url,
            "failure_url": failure_url,
        }
        return body

    def verify_payment(self, amount, **kwargs) -> bool:
        # decode the token
        token = kwargs.get("token")
        decoded_token = base64.b64decode(token).decode()
        # convert to readable format
        body = json.loads(decoded_token)
        if not body["status"] == "COMPLETE":
            return False
        # get the transaction id and amount
        transaction_id = body["transaction_id"]
        amount = float(body["amount"])
        # cross check with payment request
        payment_request = PaymentRequest.objects.filter(
            payment_partner__name="esewa", transaction_id=transaction_id, amount=amount
        )
        if not payment_request:
            return False
        # double check for transaction:
        # url: https://epay.esewa.com.np/api/epay/transaction/status/?product_code=EPAYTEST&total_amount=100&transaction_uuid=123
        # method = get
        # if status = complete, then return true
        else:
            # maybe we should return the payment request if the payment request is success
            return True
