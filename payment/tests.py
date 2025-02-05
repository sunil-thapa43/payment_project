# import requests
#
# from core.config import PaymentConfig
# import base64, json
#
# from utils import generate_transaction_id
#
# print("IM HERE")
# configs = PaymentConfig()
# creds = configs.get_credentials("imepay")
# print(type(creds))
#
# token_url = creds.get("token_url")
# username = creds.get("merchant_username")
# password = creds.get("merchant_password")
# merchant_module = creds.get("merchant_module")
# merchant_code = creds.get("merchant_code")
# amount = 13.52
# transaction_id = generate_transaction_id()
# success_url = creds.get("success_url")
# failure_url = creds.get("failure_url")
# checkout_url = creds.get("checkout_url")
# payload = {
#             "MerchantCode": merchant_code,
#             "Amount": amount,
#             "RefId": transaction_id,
#         }
# auth = f"{username}:{password}"
# auth_encoded = base64.b64encode(auth.encode()).decode()
# module_encoded = base64.b64encode(merchant_module.encode()).decode()
# headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Basic {auth_encoded}",
#             "Module": module_encoded,
#         }
#
# response = requests.post(
#     url=token_url,
#     headers=headers,
#     data=json.dumps(payload),
# )
# print("RESPONSE IS:", response)
# print("RESPONSE JSON:", response.json())
# response_json = response.json()
# print("response code: ", response_json["ResponseCode"])
# if response_json["ResponseCode"] == 0:
#     token_id = response_json["TokenId"]
#     ref_id = response_json["RefId"]
#     amount = response_json["Amount"]
#     payload_composition = f"{token_id}|{merchant_code}|{ref_id}|{amount}|GET|{success_url}|{failure_url}"
#     payload_encoded = base64.b64encode(payload_composition.encode()).decode()
#     print(f"{checkout_url}?data={payload_encoded}")
# else:
#     ...
#
#
# """ RESPONSE FROM IMEPAY
#     RESPONSE IS: <Response [200]>
#     RESPONSE JSON: {'ResponseCode': 0, 'TokenId': '202502041421246622', 'Amount': '13.5200', 'RefId': '100295eb29ef46e6a5be', 'ResponseDescription': None}
#
#     AFTER GETTING THIS RESPONSE FROM THE IMEPAY, WE NEED TO:
#     Prepare a payload string comprising data parameters and encode those data into Base64
#     string and redirect to our Url as below:
#     Payload data composition: TokenId|MerchantCode|RefId|TranAmount|Method|RespUrl|CancelUrl
#
# """
#
# # on our success url the imepay hits with param as: our_succes_url/?data=M3xPcGVyYXRpb24gQ2FuY2VsbGVkIEJ5IFVzZXJ8MDAwfDAwM
# # HxDaGl5YVBlckN1cF8xMC4xNXwxMC4xNXwyMDIwMDQwNDE5MzEzOTgzOTI%3d
#
# message = "M3xPcGVyYXRpb24gQ2FuY2VsbGVkIEJ5IFVzZXJ8MDAwfDAwMHxDaGl5YVBlckN1cF8xMC4xNXwxMC4xNXwyMDIwMDQwNDE5MzEzOTgzOTI3d"
# decoded_message = base64.b64decode(message).decode()
# print(decoded_message)
#
# client.py
import grpc
from payment.grpc import payment_pb2_grpc, payment_pb2
from payment.grpc.payment_pb2_grpc import PaymentControllerStub


class PaymentClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = payment_pb2_grpc.PaymentRequestControllerStub(self.channel)
        self.request_stub = payment_pb2_grpc.PaymentRequestControllerStub(self.channel)

    # PaymentController Methods
    def create_payment(self, payment_data):
        return self.stub.Create(payment_data)

    def get_payment(self, payment_id):
        return self.stub.Retrieve(
            payment_pb2.PaymentRetrieveRequest(id=payment_id)
        )

    # PaymentRequestController Methods
    def create_payment_request(self, request_data):
        return self.request_stub.Create(request_data)



client = PaymentClient(host='localhost', port=50051)
try:
    response = client.create_payment(
        payment_pb2.PaymentRequest(
            amount=100.22,
            user_id=122534,
        )
    )
    print(response)
except grpc.RpcError as e:
    print("HIT EXCEPTION")
    print(e)