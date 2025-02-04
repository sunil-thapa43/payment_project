from rest_framework import serializers
from .models import PaymentRequest, Payment


# class PaymentPartnersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentPartners
#         fields = '__all__'



class PaymentRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentRequest
        fields = [
            'payment_partner', 'user_id', 'purpose', 'remarks', 'amount',
            'amount_in_paisa', 'transaction_id'
        ]
        extra_kwargs = {
            'user_id': {'read_only': True},  # user_id is read-only (set from request)
            'remarks': {'required': False},  # remarks is optional
            'amount_in_paisa': {'required': False},  # amount_in_paisa is optional
            'transaction_id': {'required': False},  # transaction_id is optional
        }

    def validate(self, data):
        """
        Custom validation logic.
        """
        # Ensure merchant is provided
        if 'payment_partner' not in data:
            raise serializers.ValidationError("Payment Partner is required.")

        # Ensure purpose is one of the allowed choices
        if data['purpose'] not in self.PURPOSE_CHOICES:
            raise serializers.ValidationError("Invalid purpose.")

        # Ensure amount is provided and positive
        if 'amount' not in data or data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be a positive value.")

        return data

    def create(self, validated_data):
        """
        Custom create logic to:
        1. Set user_id from the request.
        2. Convert amount to amount_in_paisa if not provided.
        """
        # Get user_id from the request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user_id'] = request.user.id

        # Convert amount to amount_in_paisa if not provided
        if 'amount_in_paisa' not in validated_data:
            validated_data['amount_in_paisa'] = validated_data['amount'] * 100

        # Create and return the PaymentRequest instance
        return PaymentRequest.objects.create(**validated_data)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ("created_at", "updated_at")