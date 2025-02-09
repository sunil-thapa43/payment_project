from payment.views import handle_grpc_write
from utils.config import PaymentConfig
from payment.models import PaymentRequest
from payment.strategies.strategy import PaymentStrategy
import json
import requests

from utils.utils import generate_transaction_id, payment_request_with_retry


class KhaltiPayment(PaymentStrategy):
    def __init__(self):
        self.service = "khalti"
        self.config = PaymentConfig()
        self.configs = self.config.get_credentials(self.service)

    def initiate_payment(self, obj, **kwargs):
        """
        For Khalti payment, once the user chooses the Khalti payment option from all available options,
        the frontend requests for a khalti payment initiation.
        Upon that request: backend hits khalti payment url "https://dev.khalti.com/api/v2/epayment/initiate/" with
        headers = {
        #     'Authorization': 'key LIVE_SECRET_KEY',
        #     'Content-Type': 'application/json',
        # }

        khalti resonse is like:
        {
        "pidx": "bZQLD9wRVWo4CdESSfuSsB",
        "payment_url": "https://test-pay.khalti.com/?pidx=bZQLD9wRVWo4CdESSfuSsB",
        "expires_at": "2023-05-25T16:26:16.471649+05:45",
        "expires_in": 1800
        }
        Now frontend redirects the user to this payment url which is sent back by the backend. Khalti
        processes the payment of the end-user on their own end, hits our success or failure url respectively.
        """
        success_url = self.configs["success_url"]
        initiate_url = self.configs["initiate_url"]
        secret_key = self.configs["secret_key"]
        wesite_url = kwargs.get("wesite_url")

        payload = json.dumps(
            {
                "return_url": success_url,
                "website_url": wesite_url,
                # amount should be in paisa
                "amount": obj.amount * 100,
                "purchase_order_id": obj.transaction_id,
                "purchase_order_name": obj.purpose,
                # This module does not have access to the customer details, so if required this info is filled from the
                # frontend at the time of making the request to the merchant

                # "customer_info": {
                #     "name": kwargs.get("customer_name"),
                #     "email": kwargs.get("customer_email"),
                #     "phone": kwargs.get("customer_phone"),
                # },

            }
        )
        headers = {
            "Authorization": f"key {secret_key}",
            "Content-Type": "application/json",
        }
        response, status = payment_request_with_retry(
            "POST", initiate_url, headers=headers, data=payload
        )
        if response.status_code != 200:
            return None
        # lets save the pidx as signature so that we can verify later.
        obj.signature = response["pidx"]
        obj.payment_partner = "Khalti"
        obj.save()
        body = response.json()
        return body

    def verify_payment(self, **kwargs) -> bool:
        secret_key = self.configs["secret_key"]
        body = json.dumps({"pidx": kwargs.get("pidx")})
        verify_url = self.configs["verify_url"]

        headers = {
            "Authorization": f"key {secret_key}",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", verify_url, headers=headers, data=body)
        body = response.json()
        if not (response.status_code == 200 or body["status"].lower() == "completed"):
            return False
        # cross check with payment request
        payment_request = PaymentRequest.objects.filter(
            transaction_id=body["tranasaction_id"], amount=body["amount"]/100
        )
        if not payment_request:
            # add some logs here, because it is already success on Khalti's end, but might be some infiltration as well
            # add logs
            return False
        handle_grpc_write(payment_request_obj=payment_request.first())
        return True
