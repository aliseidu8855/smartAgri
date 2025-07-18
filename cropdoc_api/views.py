from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Disease, ScanHistory
from .serializers import UserSerializer, DiseaseSerializer, ScanHistorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
import random


otp_storage = {}


class SendOTPView(APIView):
    """
    View to send OTP to the user's phone number.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response(
                {"error": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = random.randint(1000, 9999)
        otp_storage[phone_number] = otp
        print(f"OTP for {phone_number}: {otp}")
        return Response(
            {"message": "OTP sent successfully."},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    """
    View to verify the OTP sent to the user's phone number.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        if not phone_number or not otp:
            return Response(
                {"error": "Phone number and OTP are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp_storage.get(phone_number) != otp:
            return Response(
                {"error": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            username=phone_number, defaults={"phone_number": phone_number}
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveAPIView):
    """_summary_

    Args:
        generics (_type_): _description_
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.request.user


class ScanHistoryListCreateView(generics.ListCreateAPIView):
    """
    View to list and create scan history entries.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScanHistorySerializer

    def get_queryset(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return ScanHistory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        image = self.request.data.get("image")
        text_description = self.request.data.get("text_description")

        predicted_disease_name = "Cassava Mosaic"  # Placeholder
        confidence = 0.95  # Placeholder

        disease_obj = Disease.objects.filter(name=predicted_disease_name).first()
        serializer.save(
            user=self.request.user,
            predicted_disease=disease_obj,
            confidence_score=confidence,
            user_text_description=text_description,
        )
