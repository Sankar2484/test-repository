from django.contrib import admin
from django.urls import path
from Hospital import views
from Hospital.views import patient_search




urlpatterns = [

    path('admin/', admin.site.urls),

    path('',views.home, name='home'),

    # Ward URLs
    path('wards/', views.ward_list, name='ward_list'),
    path('wards/new/', views.ward_create, name='ward_create'),
    path('wards/<int:pk>/edit/', views.ward_update, name='ward_update'),
    path('wards/<int:pk>/delete/', views.ward_delete, name='ward_delete'),

    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/new/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),

    # Bed URLs
    path('beds/', views.bed_list, name='bed_list'),
    path('beds/new/', views.bed_create, name='bed_create'),
    path('beds/<int:pk>/edit/', views.bed_update, name='bed_update'),
    path('beds/<int:pk>/delete/', views.bed_delete, name='bed_delete'),

    # Patient URLs
    path('patient_list/', views.patient_list, name='patient_list'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Search URLs
    path('search/', patient_search, name='patient_search'),
]
