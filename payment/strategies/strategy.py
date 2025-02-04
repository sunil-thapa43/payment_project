from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def initiate_payment(self, amount, **kwargs):
        pass

    @abstractmethod
    def verify_payment(self, amount, **kwargs):
        pass
