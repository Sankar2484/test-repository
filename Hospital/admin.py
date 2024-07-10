from django.contrib import admin
from .models import WardDetails, RoomDetails, BedDetails, PatientDetails

admin.site.register(WardDetails)
admin.site.register(RoomDetails)
admin.site.register(BedDetails)
admin.site.register(PatientDetails)