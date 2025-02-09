import json

from payment.views import handle_grpc_write
from utils.config import PaymentConfig
from payment.models import PaymentRequest, Payment
from payment.strategies.strategy import PaymentStrategy
from utils.utils import encode_esewa_message, decode_esewa_message


class EsewaPayment(PaymentStrategy):
    def __init__(self):
        self.service = "esewa"
        self.config = PaymentConfig()
        self.configs = self.config.get_credentials(self.service)

    def initiate_payment(self, obj, **kwargs):
        """
        Esewa provides some creds to the business (Mutual Fund) in our case, we encode our message with that key and
        send the end-user to Esewa platform with that message.
        End-User completes/cancels/gets-rejected for that payment, Esewa hits our success or failure url respectively
        with an encoded message which we decode and check on our end.
        """
        product_code = self.configs.get("product_code")
        secret_key = self.configs.get("secret_key")
        backend_url = self.configs.get("backend_url")
        success_url = backend_url + self.configs.get("success_url")
        failure_url = backend_url + self.configs.get("failure_url")
        # set payment method as esewa here
        obj.payment_partner = "eSewa"
        amount = obj.amount
        transaction_id = obj.transaction_id
        signed_field_names = f"total_amount,transaction_uuid,product_code"
        message = f"total_amount={amount},transaction_uuid={transaction_id},product_code={product_code}"
        signature = encode_esewa_message(message=message, secret=secret_key)
        body = {
            "amount": amount,
            "tax_amount": 0,
            "total_amount": amount,
            "transaction_uuid": transaction_id,
            "product_code": product_code,
            "product_service_charge":0,
            "product_delivery_charge": 0,
            "success_url": success_url,
            "failure_url": failure_url,
            "signed_field_names": signed_field_names,
            "signature": signature
        }
        obj.signature = signature
        obj.save()
        return body

    def verify_payment(self, **kwargs) -> bool:
        # decode the message
        message = kwargs.get("message")
        decoded_token = decode_esewa_message(message)
        body = json.loads(decoded_token)
        print(body)
        if not body["status"] == "COMPLETE":
            return False
        # get the transaction id and amount
        transaction_id = body["transaction_uuid"]
        amount = float(body["total_amount"].replace(",", ""))
        signature = body["signature"]
        # cross check with payment request
        payment_request = PaymentRequest.objects.filter(
            payment_partner="eSewa",
            transaction_id=transaction_id,
            amount=amount,
            signature=signature
        )
        if not payment_request:
            return False
        payment_request = payment_request.first()
        handle_grpc_write(payment_request_obj=payment_request)
        return True
