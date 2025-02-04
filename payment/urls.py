from django.urls import path, include

from payment.views import (
    PaymentRequestView,
    KhaltiPaymentVerificationView,
    EsewaPaymentVerificationView,
    ConnectIPSPaymentVerificationView,
    IMEPayPaymentVerificationView,
)

urlpatterns = [
    # path("payment-partners/", PaymentPartnersView.as_view(), name="payment_partners"),
    path("initiate-payment/", PaymentRequestView.as_view(), name="initiate_payment"),
    path(
        "verify/esewa/",
        EsewaPaymentVerificationView.as_view(),
        name="esewa_payment_verification",
    ),
    path(
        "verify/khalti/",
        KhaltiPaymentVerificationView.as_view(),
        name="khalti_payment_verification",
    ),
    path(
        "verify/cips/",
        ConnectIPSPaymentVerificationView.as_view(),
        name="cips_payment_verification",
    ),
    path(
        "verify/imepay/",
        IMEPayPaymentVerificationView.as_view(),
        name="imepay_payment_verification",
    ),
    # if some other payment partners are added in future, we may need to add the success url for those partners
]
