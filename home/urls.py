from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('profile/', myProfile, name = 'profile'),
    path('register/', register, name = 'register'),
    path('do_register/', doRegister, name = 'do_register'),
    path('userlist/', userlist, name = 'userlist'),
    path('manage_patient/', manage_patient, name = 'manage_patient'),
    path('edit_patient/<str:patient_id>', edit_patient, name = 'edit_patient'),
    path('edit_patient_save/', edit_patient_save, name = 'edit_patient_save'),
    path('generate/<str:patient_id>', generate, name = 'generate'),
    path('history/', history, name = 'history'),
    path('patientcheckup_save/', patientcheckup_save, name = 'patientcheckup_save'),
    path('bill_save/', bill_save, name = 'bill_save'),
    path('all_bill/', all_bill, name = 'all_bill'),
]