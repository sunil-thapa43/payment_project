import requests

from payment.views import handle_grpc_write
from utils.config import PaymentConfig
from payment.models import ImePayDetails, PaymentRequest
from payment.strategies.strategy import PaymentStrategy
from utils.utils import base_64_encoder, decode_imepay_message, prepare_imepay_header, prepare_imepay_initiate_payload, \
    payment_request_with_retry


class IMEPayPayment(PaymentStrategy):
    def __init__(self, **kwargs):
        self.service = "imepay"
        config_class = PaymentConfig()
        self.configs = config_class.get_credentials(self.service)


    def initiate_payment(self, obj, **kwargs):
        token_url = self.configs.get("token_url")
        username = self.configs.get("merchant_username")
        password = self.configs.get("merchant_password")
        merchant_module = self.configs.get("merchant_module")
        merchant_code = self.configs.get("merchant_code")
        success_url = self.configs.get("success_url")
        failure_url = self.configs.get("failure_url")
        checkout_url = self.configs.get("checkout_url")
        payload = prepare_imepay_initiate_payload(obj=obj, merchant_code=merchant_code)
        headers = prepare_imepay_header(username=username, password=password, merchant_module=merchant_module)
        # this function ime_pay_request_with_retry hits the end url 3 times consecutively, if it fails all attempts it
        # returns the status code
        response, status = payment_request_with_retry(
            method="POST", url=token_url, data=payload, headers=headers
        )
        print("IME PAY PAYMENT INITIATION FAILURE: ", status)
        if not response:
            return None
        response_json = response.json()
        if response_json["ResponseCode"] != 0:
            # return some status code, like 421 for now
            return None
        token_id = response_json["TokenId"]
        ref_id = response_json["RefId"]
        amount = response_json["Amount"]
        payload_composition = f"{token_id}|{merchant_code}|{ref_id}|{amount}|GET|{success_url}|{failure_url}"
        payload_encoded = base_64_encoder(payload_composition)
        # return this message as response to the frontend
        payload = f"{checkout_url}?data={payload_encoded}"
        # now write this to IME pay details
        ImePayDetails.objects.create(
            transaction_amount = amount,
            token_id = token_id,
            transaction_id = obj.transaction_id,
            ime_transaction_status = 0
        )
        body = {
            "payment_url": payload
        }
        return body


    def verify_payment(self, **kwargs):
        """
        The merchant (IMEPay) in this case sends an encoded message to our success url.
        Then the decoded message looks like this: Decoded data is:  3|Operation Cancelled By User|000|000|ChiyaPerCup_10.15|10.15|202004041931398392
        Order of the string is:
        a. [0]-> ResponseCode
        b. [1]-> ResponseDescription
        c. [2]-> Msisdn
        d. [3]-> TransactionId
        e. [4]-> RefId
        f. [5]-> TranAmount
        g. [6]-> TokenId
        """
        data = kwargs.get("data")
        decoded_data = decode_imepay_message(data)
        print("Decoded data is: ", decoded_data)
        data_splits = decoded_data.split("|")
        # decipher the message, if success then update the payment request table, imepay table, payment table, and
        # finally make a grpc call to the Admin that updates the payment request and payment table on their side.
        response_code = data_splits[0]
        response_description = data_splits[1]
        msisdn = data_splits[2]
        transaction_id = data_splits[3]
        ref_id = data_splits[4]
        transaction_amount = data_splits[5]
        token_id = data_splits[6]
        if not response_code == 0:
            return False, response_description
        validation_url = self.configs.get("validation_url")
        username = self.configs.get("merchant_username")
        password = self.configs.get("merchant_password")
        merchant_module = self.configs.get("merchant_module")
        merchant_code = self.configs.get("merchant_code")
        headers = prepare_imepay_header(username=username, password=password, merchant_module=merchant_module)
        payload = {
            "MerchantCode": merchant_code,
            "RefId": ref_id,
            "TokenId": token_id,
            "TransactionId": transaction_id,
            "Msisdn": msisdn,
        }
        response, status = payment_request_with_retry(
            method="POST", url=validation_url, data=payload, headers=headers
        )
        if response.status_code != 200:
            return False, response.status_code
        response_json = response.json()
        imepay_status_code = response_json["ResponseCode"]
        imepay_details = ImePayDetails.objects.filter(
            transaction_id=transaction_id,
            token_id=token_id,
            transaction_amount=transaction_amount,
        )
        if not imepay_details or imepay_status_code!=0:
            return False
        imepay_detail = imepay_details.first()
        # update the record
        imepay_detail.ime_transaction_status = imepay_status_code
        imepay_detail.save()
        payment_request = PaymentRequest.objects.filter(transaction_id=transaction_id)
        if not payment_request:
            return False
        payment_request =  payment_request.first()
        handle_grpc_write(payment_request_obj=payment_request)
        return True
