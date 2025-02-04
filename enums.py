from enum import Enum


class BaseEnum(Enum):
    """
    Base Enum class with a reusable `choices` method.
    """

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PaymentVendor(BaseEnum):
    ESEWA = "eSewa"
    IME_PAY = "IME Pay"
    KHALTI = "Khalti"
    CONNECT_IPS = "Connect IPS"


class PaymentStatus(BaseEnum):
    INITIATED = "Initiated"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    ERROR = "Error"
