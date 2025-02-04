from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from payment.services import PaymentService, PaymentRequestService

def grpc_handlers(server):
    app_registry = AppHandlerRegistry("payment", server)
    app_registry.register(PaymentService)
    app_registry.register(PaymentRequestService)