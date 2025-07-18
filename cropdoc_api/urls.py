from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("auth/send-otp/", views.SendOTPView.as_view(), name="send-otp"),
    path("auth/verify-otp/", views.VerifyOTPView.as_view(), name="verify-otp"),
    # Core Features
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("scans/", views.ScanHistoryListCreateView.as_view(), name="scan-history"),
]
