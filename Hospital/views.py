from django.shortcuts import render, get_object_or_404, redirect
from Hospital.models import BedDetails, RoomDetails, WardDetails, PatientDetails
from django.core.exceptions import ValidationError
import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db.models import Q



def home(request):
    return render(request, 'home.html')


# List views
def ward_list(request):
    wards = WardDetails.objects.all()
    return render(request, 'ward_list.html', {'wards': wards})

def room_list(request):
    rooms = RoomDetails.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

def bed_list(request):
    beds = BedDetails.objects.all()
    return render(request, 'bed_list.html', {'beds': beds})

def patient_list(request):
    patients = PatientDetails.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

# Create views
def ward_create(request):
    if request.method == 'POST':
        wardType = request.POST['wardType']
        WardDetails.objects.create(wardType=wardType)
        return redirect('ward_list')
    return render(request, 'ward_form.html')

def room_create(request):
    if request.method == 'POST':
        roomNumber = request.POST['roomNumber']
        floor = request.POST['floor']
        capacity = request.POST['capacity']
        RoomDetails.objects.create(roomNumber=roomNumber, floor=floor, capacity=capacity)
        return redirect('room_list')
    return render(request, 'room_form.html')

def bed_create(request):
    if request.method == 'POST':
        isAvailable = request.POST.get('isAvailable', 'off') == 'on'
        room_id = request.POST['room']
        ward_id = request.POST['ward']
        room = get_object_or_404(RoomDetails, pk=room_id)
        ward = get_object_or_404(WardDetails, pk=ward_id)
        BedDetails.objects.create(isAvailable=isAvailable, room=room, ward=ward)
        return redirect('bed_list')
    return render(request, 'bed_form.html', {'rooms': RoomDetails.objects.all(), 'wards': WardDetails.objects.all()})

def patient_create(request):
    if request.method == 'POST':
        room_id = request.POST['room']
        room = get_object_or_404(RoomDetails, pk=room_id)
        bed_count = BedDetails.objects.filter(room=room).count()
        if bed_count < room.capacity:
            admit_time = request.POST['admitTime']
            discharge_time = request.POST['dischargeTime']

            if not admit_time:
                admit_time = None
            else:
                try:
                    admit_time = datetime.datetime.strptime(admit_time, '%H:%M').time()
                except ValueError:
                    raise ValidationError('Invalid admit time format.')

            if not discharge_time:
                discharge_time = None
            else:
                try:
                    discharge_time = datetime.datetime.strptime(discharge_time, '%H:%M').time()
                except ValueError:
                    raise ValidationError('Invalid discharge time format.')

            patient = PatientDetails(
                patientName=request.POST['patientName'],
                patientMobile=request.POST['patientMobile'],
                checkInDate=request.POST['checkInDate'],
                checkOutDate=request.POST['checkOutDate'] or None,
                admitTime=admit_time,
                dischargeTime=discharge_time,
                patientAddress=request.POST['patientAddress'],
                patientEmail=request.POST['patientEmail'],
                emergencyContact=request.POST['emergencyContact'],
                dateOfBirth=request.POST['dateOfBirth'] or None,
                gender=request.POST['gender'],
                currentDiagnosis=request.POST['currentDiagnosis'],
                doctorAssigned=request.POST['doctorAssigned'],
                bed_id=request.POST['bed'],
                room_id=request.POST['room'],
                ward_id=request.POST['ward']
            )
            patient.save()
            return redirect('patient_list')
        else:
            return render(request, 'patient_form.html', {'error': 'Room capacity exceeded', 'beds': BedDetails.objects.filter(isAvailable=True), 'rooms': RoomDetails.objects.all(), 'wards': WardDetails.objects.all()})
    else:
        beds = BedDetails.objects.filter(isAvailable=True)
        rooms = RoomDetails.objects.all()
        wards = WardDetails.objects.all()
        return render(request, 'patient_form.html', {'beds': beds, 'rooms': rooms, 'wards': wards})

# Update views
def ward_update(request, pk):
    ward = get_object_or_404(WardDetails, pk=pk)
    if request.method == 'POST':
        ward.wardType = request.POST['wardType']
        ward.save()
        return redirect('ward_list')
    return render(request, 'ward_form.html', {'ward': ward})

def room_update(request, pk):
    room = get_object_or_404(RoomDetails, pk=pk)
    if request.method == 'POST':
        room.roomNumber = request.POST['roomNumber']
        room.floor = request.POST['floor']
        room.capacity = request.POST['capacity']
        room.save()
        return redirect('room_list')
    return render(request, 'room_form.html', {'room': room})

def bed_update(request, pk):
    bed = get_object_or_404(BedDetails, pk=pk)
    if request.method == 'POST':
        bed.isAvailable = request.POST.get('isAvailable', 'off') == 'on'
        bed.room_id = request.POST['room']
        bed.ward_id = request.POST['ward']
        bed.save()
        return redirect('bed_list')
    return render(request, 'bed_form.html', {'bed': bed, 'rooms': RoomDetails.objects.all(), 'wards': WardDetails.objects.all()})

def patient_update(request, pk):
    patient = get_object_or_404(PatientDetails, pk=pk)
    if request.method == 'POST':
        room_id = request.POST['room']
        room = get_object_or_404(RoomDetails, pk=room_id)
        bed_count = BedDetails.objects.filter(room=room).count()
        if bed_count < room.capacity or patient.room_id == room_id:
            admit_time = request.POST['admitTime']
            discharge_time = request.POST['dischargeTime']

            if not admit_time:
                admit_time = None
            else:
                try:
                    admit_time = datetime.datetime.strptime(admit_time, '%H:%M').time()
                except ValueError:
                    raise ValidationError('Invalid admit time format.')

            if not discharge_time:
                discharge_time = None
            else:
                try:
                    discharge_time = datetime.datetime.strptime(discharge_time, '%H:%M').time()
                except ValueError:
                    raise ValidationError('Invalid discharge time format.')

            patient.patientName = request.POST['patientName']
            patient.patientMobile = request.POST['patientMobile']
            patient.checkInDate = request.POST['checkInDate']
            patient.checkOutDate = request.POST['checkOutDate'] or None
            patient.admitTime = admit_time
            patient.dischargeTime = discharge_time
            patient.patientAddress = request.POST['patientAddress']
            patient.patientEmail = request.POST['patientEmail']
            patient.emergencyContact = request.POST['emergencyContact']
            patient.dateOfBirth = request.POST['dateOfBirth'] or None
            patient.gender = request.POST['gender']
            patient.currentDiagnosis = request.POST['currentDiagnosis']
            patient.doctorAssigned = request.POST['doctorAssigned']
            patient.bed_id = request.POST['bed']
            patient.room_id = request.POST['room']
            patient.ward_id = request.POST['ward']
            patient.save()
            return redirect('patient_list')
        else:
            return render(request, 'patient_form.html', {'patient': patient, 'error': 'Room capacity exceeded', 'beds': BedDetails.objects.filter(isAvailable=True), 'rooms': RoomDetails.objects.all(), 'wards': WardDetails.objects.all()})
    else:
        beds = BedDetails.objects.filter(isAvailable=True) | BedDetails.objects.filter(pk=patient.bed.pk)
        rooms = RoomDetails.objects.all()
        wards = WardDetails.objects.all()
        return render(request, 'patient_form.html', {'patient': patient, 'beds': beds, 'rooms': rooms, 'wards': wards})


# Delete views

def ward_delete(request, pk):
    ward = get_object_or_404(WardDetails, pk=pk)
    if request.method == 'POST':
        ward.delete()
        return redirect('ward_list')
    return render(request, 'ward_confirm_delete.html', {'ward': ward})

def room_delete(request, pk):
    room = get_object_or_404(RoomDetails, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'room_confirm_delete.html', {'room': room})

def bed_delete(request, pk):
    bed = get_object_or_404(BedDetails, pk=pk)
    if request.method == 'POST':
        bed.delete()
        return redirect('bed_list')
    return render(request, 'bed_confirm_delete.html', {'bed': bed})

def patient_delete(request, pk):
    patient = get_object_or_404(PatientDetails, pk=pk)
    patient.delete()
    return redirect('patient_list')


# Search Patient

def patient_search(request):
    query = request.GET.get('q')
    patients = PatientDetails.objects.filter(patientName__icontains=query)
    return render(request, 'search_results.html', {'patients': patients})