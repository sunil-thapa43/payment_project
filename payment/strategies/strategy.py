from abc import ABC, abstractmethod

from payment.models import PaymentRequest


class PaymentStrategy(ABC):
    @abstractmethod
    def initiate_payment(self, obj:PaymentRequest, **kwargs):
        """
        Initiate Payment is not basically initiate payment in our case, because the payment is
        already initiated by the Admin service.
        This method is only called when the frontend requests for the payment payloads so that the
        user will be taken to the Payment Partners' portal and make the payment.
        So, generation of a transaction id will be taken care by Create method on gRPC call when the
        admin service initiates the payment.
        """
        ...

    @abstractmethod
    def verify_payment(self, message, **kwargs):
        """
        Verify payment is just a class method that helps to verify the payments made from various
        merchants. For each payment partner, separate implementation of verify payment is adopted.
        """
        ...
