"""
This module contains the models for the CropDoc API, including custom user model,
disease model, and scan history model."""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    This allows for future extensibility if needed.
    """

    phone_number = models.CharField(max_length=15, blank=True, null=True)


class Disease(models.Model):
    """
    Model to represent a disease.
    """

    name = models.CharField(max_length=100, unique=True)
    twi_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    treatment_advice = models.TextField(blank=True, null=True)
    twi_treatment_advice = models.TextField(blank=True, null=True)




class ScanHistory(models.Model):
    """
    Model to represent a scan history entry.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="scans/")
    predicted_disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    confidence_score = models.FloatField()
    user_text_description = models.TextField(blank=True, null=True)
    user_audio_path = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for ScanHistory model."""
        ordering = ["-created_at"]
