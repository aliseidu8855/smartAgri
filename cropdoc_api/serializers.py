from rest_framework import serializers
from .models import User, Disease, ScanHistory


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    This serializer includes all fields from the User model.
    """

    class Meta:
        model = User
        fields = ["id", "username", "phone_number"]


class DiseaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Disease model.
    This serializer includes all fields from the Disease model.
    """

    class Meta:
        model = Disease
        fields = "__all__"


class ScanHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ScanHistory model.
    This serializer includes all fields from the ScanHistory model.
    """

    predicted_disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = ScanHistory
        fields = [
            "id",
            "image",
            "predicted_disease",
            "confidence_score",
            "created_at",
            "user_text_description",
        ]
        read_only_fields = ["predicted_disease", "confidence_score", "created_at"]
