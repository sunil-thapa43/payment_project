from rest_framework import serializers

from .grpc import payment_pb2
from .models import PaymentRequest, Payment
from django_socio_grpc import proto_serializers


# class PaymentPartnersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentPartners
#         fields = '__all__'


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = [
            "payment_partner",
            "user_id",
            "purpose",
            "remarks",
            "amount",
            "amount_in_paisa",
            "transaction_id",
        ]
        extra_kwargs = {
            "payment_partner": {"required": True},
            "user_id": {"required": True},
            "remarks": {"required": False},  # remarks is optional
            "amount_in_paisa": {"required": False},  # amount_in_paisa is optional
            "purpose": {"required": False}
        }

    def validate(self, data):
        """
        Custom validation logic.
        """
        # Ensure merchant is provided
        if "payment_partner" not in data:
            raise serializers.ValidationError("Payment Partner is required.")

        # Ensure amount is provided and positive
        if "amount" not in data or data["amount"] <= 10:
            raise serializers.ValidationError("Amount must be greater than Rs. 10")

        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ("created_at", "updated_at")


""" Writing Proto Serializers from here on:"""

class PaymentRequestProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = PaymentRequest
        proto_class = payment_pb2.PaymentRequest
        fields = [
            "id",
            "payment_partner",
            "user_id",
            "purpose",
            "remarks",
            "amount",
            "amount_in_paisa",
            "transaction_id",
            "status"
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "payment_partner": {"required": False},
            "remarks": {"required": False},
            "amount_in_paisa": {"required": False},
            "transaction_id": {"required": False},
            "purpose": {"required": False},
            "status": {"required": False},
        }


class PaymentProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "request",
            "user_id",
            "amount",
            "transaction_id",
            "amount_in_paisa",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "amount_in_paisa": {"required": False},
        }
