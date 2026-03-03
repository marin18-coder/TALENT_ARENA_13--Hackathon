from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(min_length=8, max_length=20)

    def validate_phoneNumber(self, value):
        # Keep digits and +
        normalized = "".join(ch for ch in value if ch.isdigit() or ch == "+")
        digits = [c for c in normalized if c.isdigit()]

        if len(digits) < 8:
            raise serializers.ValidationError("Invalid phone number.")

        return normalized