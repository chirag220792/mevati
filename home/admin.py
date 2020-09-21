from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PastHistory)
admin.site.register(ComplaintList)
admin.site.register(PatientCheckUp)
admin.site.register(PatientComplaint)
admin.site.register(Medicines)
admin.site.register(PrescriptionMedicine)
admin.site.register(Bill)