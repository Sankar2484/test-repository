from django.db import models
from django.utils.timezone import now
import datetime


class WardDetails(models.Model):
    wardType = models.CharField(max_length=50)

class RoomDetails(models.Model):
    roomNumber = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    capacity = models.IntegerField()

class BedDetails(models.Model):
    isAvailable = models.BooleanField(default=True)
    room = models.ForeignKey(RoomDetails, on_delete=models.CASCADE)
    ward = models.ForeignKey(WardDetails, on_delete=models.CASCADE, null=True)

class PatientDetails(models.Model):
    patientName = models.CharField(max_length=100)
    patientMobile = models.CharField(max_length=15)
    checkInDate = models.DateField()
    checkOutDate = models.DateField(null=True, blank=True)
    admitTime = models.TimeField(null=True, blank=True)
    dischargeTime = models.TimeField(null=True, blank=True)
    patientAddress = models.CharField(max_length=255, null=True, blank=True)
    patientEmail = models.EmailField(null=True, blank=True)
    emergencyContact = models.CharField(max_length=15, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    currentDiagnosis = models.TextField(null=True, blank=True)
    doctorAssigned = models.CharField(max_length=100, null=True, blank=True)
    bed = models.OneToOneField(BedDetails, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(RoomDetails, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(WardDetails, on_delete=models.SET_NULL, null=True)