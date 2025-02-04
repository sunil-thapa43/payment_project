from django.contrib import admin

from payment.models import ImePayDetails, Payment, PaymentRequest

# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentRequest)
admin.site.register(ImePayDetails)