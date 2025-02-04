from django_socio_grpc import generics
from grpc import RpcError, StatusCode

from enums import PaymentStatus
from payment.models import PaymentRequest, Payment
from payment.serializers import PaymentRequestProtoSerializer, PaymentProtoSerializer
from utils import generate_transaction_id


class PaymentRequestService(generics.AsyncModelService):
    queryset = PaymentRequest.objects.all()
    serializer_class = PaymentRequestProtoSerializer

    async def Create(self, request, context):
        print("PAYMENT REQUEST IS HIT FROM OTHER SERVICE")
        serializer = self.get_serializer(message=request)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.message
        # generate transaction_id for the request
        transaction_id = generate_transaction_id()
        user_id = validated_data['user_id']
        amount = validated_data['amount']
        # in python if decimal is multiplied by int, the result is Decimal => on need to typecast again
        amount_in_paisa = amount * 100
        purpose = validated_data['purpose']
        remarks = validated_data['remarks']
        status = PaymentStatus.choices()[0][0]
        # we request the admin to select one payment_partner, but allow user to change the payment partner according to
        # his wish
        payment_partner = validated_data['payment_partner']
        try:
            instance, created = PaymentRequest.objects.create(
                transaction_id=transaction_id,
                amount=amount,
                user_id=user_id,
                amount_in_paisa=amount_in_paisa,
                purpose=purpose,
                remarks=remarks,
                status=status,
                payment_partner=payment_partner
            )
        except PaymentRequest.AlreadyExists:
            return RpcError(StatusCode.ALREADY_EXISTS, "Payment request already exists")

        return serializer.to_message(instance)



class PaymentService(generics.AsyncModelService):
    queryset = Payment.objects.all()
    serializer_class = PaymentProtoSerializer