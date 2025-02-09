# This client will be responsible for updating the payment db table of another service,
# i.e Admin. We will be updating the payment status whenever the payment is completed.

import grpc
from payment.grpc import payment_pb2_grpc, payment_pb2

class PaymentClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = payment_pb2_grpc.PaymentControllerStub(self.channel)

    # PaymentController Methods
    async def create_payment(self, payment_data):
        return self.stub.Create(payment_data)

    async def update_payment(self, payment_data):
        return self.stub.Update(payment_data)

    async def update_payment_request(self, payment_request):
        return self.stub.Update(payment_request)


def grpc_update_payment(payment_obj):
    client = PaymentClient(host='localhost', port=50051)
    try:
        response = client.create_payment(
            payment_pb2.PaymentRequest(
                amount=payment_obj.amount,
                user_id=payment_obj.request.user_id,
                transaction_id=payment_obj.transaction_id,
            )
        )
        print(response)
    except grpc.RpcError as e:
        print("HIT EXCEPTION")
        print(e)