from rest_framework import status
from rest_framework.response import Response

from core.views import NavyaAuthView, NavyaAuthLessView
from payment.models import PaymentRequest
from payment.serializers import PaymentRequestSerializer
from payment.strategies.connect_ips import ConnectIPSPayment
from payment.strategies.esewa import EsewaPayment
from payment.strategies.ime_pay import IMEPayPayment
from payment.strategies.khalti import KhaltiPayment


class PaymentRequestView(NavyaAuthLessView):
    serializer_class = PaymentRequestSerializer

    # post request
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_partner = serializer.validated_data["payment_partner"]
        amount = serializer.validated_data["amount"]
        user_id = serializer.validated_data["user_id"]
        transaction_id = serializer.validated_data["transaction_id"]
        # check the record in our db first
        transaction_request = PaymentRequest.objects.filter(
            amount=amount,
            user_id=user_id,
            transaction_id=transaction_id,
        )
        if not transaction_request:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data=None
            )

        # check the user chosen strategy and set strategy accordingly
        if payment_partner== "esewa":
            strategy = EsewaPayment()
            body = strategy.initiate_payment(amount=amount)
        elif payment_partner== "khalti":
            strategy = KhaltiPayment()
            body = strategy.initiate_payment(amount=amount)
        elif payment_partner== "connectips":
            strategy = ConnectIPSPayment()
            body = strategy.initiate_payment(amount=amount)
        elif payment_partner== "imepay":
            strategy = IMEPayPayment()
            body = strategy.initiate_payment(amount=amount)

        else:
            raise NotImplementedError

        # now save the payment request object here and return response to user, shall be atomic transaction
        payment_request_obj, created = PaymentRequest.object.create(
            amount=amount,
            amount_in_paisa=amount * 100,
            # purpose=purpose,
            remarks=body["remarks"],
            transaction_id=body["transaction_id"],
            user_id=user_id,
            payment_partner=payment_partner,
        )
        response_body = self.serializer_class(payment_request_obj).data
        return Response(data=response_body, status=status.HTTP_200_OK)


class EsewaPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        request_content = self.request.get.GET()
        # decode the content
        # decoding is done on EsewaPayment Strategy
        strategy = EsewaPayment()
        payment_verified = strategy.verify_payment(request_content)
        # check the amount, transaction id matches here with the payment request
        # if yes then do grpc
        # else nothing
        pass


class KhaltiPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        # similar flow, creating separate views for separate handling of requests
        # call the verify_payment method from paymentStrategy, verify the payment and do the grpc
        pass


class IMEPayPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        """
        If merchant specified the Method parameter as GET then transaction response is routed to
        the merchant’s portal (RespUrl) in a Base64 query string by IME pay. The response url
        will be like:
        http://abc.com/result.aspx?data=M3xPcGVyYXRpb24gQ2FuY2VsbGVkIEJ5IFVzZXJ8MDAwfDAwM
        HxDaGl5YVBlckN1cF8xMC4xNXwxMC4xNXwyMDIwMDQwNDE5MzEzOTgzOTI%3d
        """

        data = request.GET.get("data")
        # here I want this strategy to handle the write and grpc calls
        strategy = IMEPayPayment()
        verified = strategy.verify_payment(data=data)
        # maybe return redirect
        if verified:
            # maybe redirect
            return Response(success=True, data={}, status=status.HTTP_200_OK)
        else:
            # maybe redirect to payment failed url or sth like that
            return ...



class ConnectIPSPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        pass


# we may need to provide both APIs for checking the payment request and the payment success db table when requested by
# the staff users (need to discuss later). So we will be open to 2 db calls from other services, these services will be
# added to allowed hosts (IMO)
# PaymentRequestView -> get, auth= isStaffUser, isAdmin, isSuperUser, table = PaymentRequest
# PaymentView -> get, auth= same as above, table = Payment


def handle_grpc_write():
    # do something here like writing the payment status
    pass
