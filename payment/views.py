from rest_framework import status
from rest_framework.response import Response

from core.views import NavyaAuthView, NavyaAuthLessView
from payment.models import PaymentRequest
from payment.serializers import PaymentRequestSerializer
from payment.strategies.connect_ips import ConnectIPSPayment
from payment.strategies.esewa import EsewaPayment
from payment.strategies.ime_pay import IMEPayPayment
from payment.strategies.khalti import KhaltiPayment



# class PaymentPartnersView(NavyaAuthLessView):
#     queryset = PaymentPartners.objects.filter(active=True)
#     serializer_class = PaymentPartnersSerializer


    # def get(self, request):
    #     response = self.queryset
    #     return Response(data=response, status=status.HTTP_200_OK)


class PaymentRequestView(NavyaAuthLessView):
    serializer_class = PaymentRequestSerializer
    # post request
    def post(self, request, *args, **kwargs):
        serializer = PaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_partner = serializer.validated_data['payment_partner']
        amount = serializer.validated_data['amount']
        purpose = serializer.validated_data['purpose']
        # check the user chosen strategy and set strategy accordingly
        if payment_partner.name == "esewa":
            strategy = EsewaPayment()
            body = strategy.initiate_payment(amount=amount, purpose=purpose)
        elif payment_partner.name == "khalti":
            strategy = KhaltiPayment()
            body = strategy.initiate_payment(amount=amount, purpose=purpose)
        elif payment_partner.name == "connectips":
            strategy = ConnectIPSPayment()
            body = strategy.initiate_payment(amount=amount, purpose=purpose)
        elif payment_partner.name == "imepay":
            strategy = IMEPayPayment()
            body = strategy.initiate_payment(amount=amount, purpose=purpose)

        else:
            raise NotImplementedError

        # now save the payment request object here and return response to user, shall be atomic transaction
        payment_request_obj, created = PaymentRequest.object.create(
            amount=amount,
            amount_in_paisa=amount*100,
            purpose=purpose,
            remarks=body['remarks'],
            transaction_id=body['transaction_id'],
            user_id=user_id,
            payment_partner=payment_partner,
        )
        return Response(data=body, status=status.HTTP_200_OK)


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
        # ref_id from the response is transaction_id in our payment request table
        pass


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