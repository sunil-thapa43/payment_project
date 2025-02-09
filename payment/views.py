from django.views.generic.base import RedirectView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from core.views import NavyaAuthLessView
from payment.grpc.grpc_client import grpc_update_payment
from payment.models import PaymentRequest, Payment
from payment.serializers import PaymentRequestSerializer
from payment.strategies.connect_ips import ConnectIPSPayment
from payment.strategies.esewa import EsewaPayment
from payment.strategies.ime_pay import IMEPayPayment
from payment.strategies.khalti import KhaltiPayment


def handle_grpc_write(payment_request_obj:PaymentRequest)->None:
    with transaction.atomic:
        payment_request_obj.status = "Completed"
        payment_request_obj.save()
        # create an entry into Payment table
        payment_obj, created =Payment.objects.create(
            request=payment_request_obj,
            transaction_id=payment_request_obj.transaction_id,
            amount=payment_request_obj.amount,
            amount_in_paisa=payment_request_obj.amount_in_paisa,
            user_id=payment_request_obj.user_id,
        )
        # now handle grpc write
        grpc_update_payment(payment_obj=payment_obj)

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
        transaction_request_object = transaction_request.first()
        # check the user chosen strategy and set strategy accordingly
        if payment_partner== "eSewa":
            strategy = EsewaPayment()
            body= strategy.initiate_payment(obj=transaction_request_object)
        elif payment_partner== "Khalti":
            strategy = KhaltiPayment()
            body= strategy.initiate_payment(obj=transaction_request_object)
        elif payment_partner== "Connect IPS":
            strategy = ConnectIPSPayment()
            body= strategy.initiate_payment(obj=transaction_request_object)
        elif payment_partner== "IME Pay":
            strategy = IMEPayPayment()
            body = strategy.initiate_payment(obj=transaction_request_object)

        else:
            raise NotImplementedError

        if not body:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=body, status=status.HTTP_200_OK)


class EsewaPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        data = request.query_params.get("data")
        # this data should be decoded first. Decoding is done on EsewaPayment Strategy
        strategy = EsewaPayment()
        payment_verified = strategy.verify_payment(message=data)
        if payment_verified:
            # redirect to success url
            return Response(data={}, status=status.HTTP_200_OK)
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


class KhaltiPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        # similar flow, creating separate views for separate handling of requests
        # call the verify_payment method from paymentStrategy, verify the payment and do the grpc
        data = request.query_params.get("data")
        strategy = KhaltiPayment()
        payment_verified = strategy.verify_payment(message=data)
        # maybe redirect
        return Response(data={}, status=status.HTTP_200_OK)


class IMEPayPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        """
        If merchant specified the Method parameter as GET then transaction response is routed to
        the merchant’s portal (RespUrl) in a Base64 query string by IME pay. The response url
        will be like:
        http://abc.com/result.aspx?data=M3xPcGVyYXRpb24gQ2FuY2VsbGVkIEJ5IFVzZXJ8MDAwfDAwM
        HxDaGl5YVBlckN1cF8xMC4xNXwxMC4xNXwyMDIwMDQwNDE5MzEzOTgzOTI%3d
        """

        data = request.query_params.get("data")
        print("the query_param is: ", data)
        # here I want this strategy to handle the write and grpc calls
        strategy = IMEPayPayment()
        verified = strategy.verify_payment(data=data)
        # maybe return redirect
        if verified:
            # maybe redirect
            return Response(data={}, status=status.HTTP_200_OK)
        # maybe redirect to payment failed url or sth like that
        return ...



class ConnectIPSPaymentVerificationView(NavyaAuthLessView):
    def get(self, request):
        """
        FROM CIPS DOCS:
        In each instance of redirection, connectIPS will append only TXNID parameter at the end of the URL;
        referring to which, payment validation URL has to be called to validate payment from merchant’s end.
        """
        data = request.query_params.get("TXNID")
        strategy = ConnectIPSPayment()
        verified = strategy.verify_payment(txn_id=data)
        # Redirection to be done
        if verified:
            return Response(data={}, status=status.HTTP_200_OK)
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


class PaymentFailureView(NavyaAuthLessView, RedirectView):
    permanent = False
    query_string = True
    url = "https://navya_payment_fail_page"

# We can redirect to this PaymentFailureView for all failed payments, but maybe we should update the payment request
# Just considering this issue, I have made separate views.

class EsewaPaymentFailureView(PaymentFailureView):
    ...

class KhaltiPaymentFailureView(PaymentFailureView):
    ...

class IMEPayPayFailureView(PaymentFailureView):
    ...

class ConnectIPSPayFailureView(PaymentFailureView):
    # set status to failed
    def get(self, request, *args, **kwargs):
        txn_id = request.query_params.get("TXNID")
        payment_request = PaymentRequest.objects.filter(transaction_id=txn_id)
        if not payment_request:
            # redirect
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        payment_request = payment_request.first()
        payment_request.status = "Failed"
        payment_request.save()
        # redirect
        return Response(data={}, status=status.HTTP_200_OK)