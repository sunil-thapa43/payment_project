from django_socio_grpc import generics
from grpc import RpcError, StatusCode
from enums import PaymentStatus
from payment.grpc import payment_pb2
from payment.models import PaymentRequest, Payment
from payment.serializers import PaymentRequestProtoSerializer, PaymentProtoSerializer
from utils import generate_transaction_id


class PaymentRequestService(generics.AsyncModelService):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestProtoSerializer

    async def Create(self, request, context):
        print("PAYMENT REQUEST IS HIT FROM OTHER SERVICE")
        print("Payment request context is:", context)
        print("GRPC Context: ", context.grpc_context)
        print("Trailing metadata: ", context.grpc_context.trailing_metadata())
        try:
            serializer = self.get_serializer(message=request)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.message
            transaction_id = generate_transaction_id()
            user_id = validated_data.user_id
            amount = validated_data.amount
            amount_in_paisa = amount * 100
            purpose = validated_data.purpose
            remarks = validated_data.remarks
            status = PaymentStatus.choices()[0][0]

            # Create instance using async ORM methods directly
            instance = await PaymentRequest.objects.acreate(
                transaction_id=transaction_id,
                amount=amount,
                amount_in_paisa=amount_in_paisa,
                user_id=user_id,
                purpose=purpose,
                remarks=remarks,
                status=status
            )
            try:
                context.set_code(StatusCode.OK)
                context.set_details("Payment Request created successfully.")
                # I encountered this error when trying to return the response without having any trailing_meta_data
                # while sending the response, so below line is added for now until the package is updated.
                # TypeError : PaymentRequest/Create
                # Traceback (most recent call last):
                #   File "/usr/local/lib/python3.12/site-packages/django_socio_grpc/services/servicer_proxy.py", line 238, in handler
                #     response = self._middleware_chain(request_container)
                #                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                #   File "/usr/local/lib/python3.12/site-packages/django_socio_grpc/middlewares.py", line 92, in middleware
                #     return get_response(request)
                #            ^^^^^^^^^^^^^^^^^^^^^
                #   File "/usr/local/lib/python3.12/site-packages/django_socio_grpc/middlewares.py", line 59, in middleware
                #     return get_response(request)
                #            ^^^^^^^^^^^^^^^^^^^^^
                #   File "/usr/local/lib/python3.12/site-packages/django_socio_grpc/services/servicer_proxy.py", line 154, in _get_response
                #     socio_response = GRPCInternalProxyResponse(response, request_container.context)
                #                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                #   File "<string>", line 7, in __init__
                #   File "/usr/local/lib/python3.12/site-packages/django_socio_grpc/request_transformer/grpc_internal_proxy.py", line 57, in __post_init__
                #     self.headers = ResponseHeadersProxy(self.grpc_context, self.http_response)
                #                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                #   File "<string>", line 6, in __init__
                #   File "/usr/local/lib/python3.12/site-packages/django_socio_grpc/request_transformer/grpc_internal_proxy.py", line 182, in __post_init__
                #     metadata_as_dict = dict(self.grpc_context.trailing_metadata())
                context.set_trailing_metadata(
                    [
                        ("service-name", "Payment-Module"),
                        ("service-version", "1.0")
                    ]
                )
                return payment_pb2.PaymentRequestResponse(
                    id=instance.id,
                    amount=instance.amount,
                    amount_in_paisa=instance.amount_in_paisa,
                    status=instance.status,
                    remarks=instance.remarks,
                    payment_partner=instance.payment_partner,
                    transaction_id=instance.transaction_id,
                    purpose=instance.purpose,
                    user_id=instance.user_id,
                )
            except Exception as e:
                print("Could not convert to proto message", e)

        except Exception as e:
            # Proper error handling
            context.set_code(StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return payment_pb2.PaymentRequestResponse()


class PaymentService(generics.AsyncModelService):
    queryset = Payment.objects.all()
    serializer_class = PaymentProtoSerializer