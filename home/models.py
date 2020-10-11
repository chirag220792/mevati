from django.db import models
from django.contrib.auth.models import User


class PastHistory(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_patient')
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_doctor')
	history_type = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	description = models.CharField(max_length=500, default=None)
	created_at=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.patient.username + ' having ' + self.history_type

class ComplaintList(models.Model):
	complaintname = models.CharField(max_length = 250)
	
	def __str__(self):
		return self.complaintname

	class Meta:
		db_table = "newcomplaints"

		
class PatientCheckUp(models.Model):
	patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patientcheckup_patient')
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patientcheckup_doctor')
	lmpdob = models.DateField(blank=True, null = True)
	weight = models.DecimalField(blank=True, null = True, decimal_places = 2, max_digits=500)
	height = models.DecimalField(blank=True, null = True, decimal_places = 2, max_digits=300)
	generalcondition = models.CharField(max_length=50)
	temperature = models.DecimalField(blank=True, null = True, decimal_places = 2, max_digits=110)
	pulse = models.IntegerField()
	systolicpressure = models.IntegerField()
	dystolicpressure = models.IntegerField()
	respiratoryrate = models.IntegerField()
	spo2 = models.IntegerField()
	checkupremake = models.CharField(max_length = 250, blank=True, null = True)
	respiratorysystem = models.CharField(max_length = 50, blank=True, null = True)
	cardiovascularsystem = models.CharField(max_length = 50, blank=True, null = True)
	centralnervoussystem = models.CharField(max_length = 50, blank=True, null = True)
	palpitation1 = models.CharField(max_length = 20, blank=True, null = True)
	palpitation2 = models.CharField(max_length = 20, blank=True, null = True)
	palpitation3 = models.TextField()
	provisionaldiagnosis = models.CharField(max_length = 20, blank=True, null = True)
	followup = models.CharField(max_length=200, blank = True, null = True)
	filed_date=models.DateTimeField(auto_now= True)

	def __str__(self):
		return self.patient.username + ' having ' + self.provisionaldiagnosis

class PatientComplaint(models.Model):
	patientcheckup = models.ForeignKey(PatientCheckUp, on_delete=models.CASCADE)
	complaint1 = models.CharField(max_length = 50, blank=True, null = True)
	since1 = models.CharField(max_length = 20, blank=True, null = True)
	complaint2 = models.CharField(max_length = 50, blank=True, null = True)
	since2 = models.CharField(max_length = 20, blank=True, null = True)
	complaint3 = models.CharField(max_length = 50, blank=True, null = True)
	since3 = models.CharField(max_length = 20, blank=True, null = True)

class Medicines(models.Model):
	medicinesname = models.CharField(max_length = 250)
	
	def __str__(self):
		return self.medicinesname

	class Meta:
		db_table = "newmedicines"

class PrescriptionMedicine(models.Model):
	patientcheckup = models.ForeignKey(PatientCheckUp, on_delete=models.CASCADE)
	doctor = models.ForeignKey(User, on_delete=models.CASCADE)
	name1 = models.CharField(max_length=200)
	time1 = models.CharField(max_length=10)
	when1 = models.CharField(max_length=10)
	numberofdays1 = models.IntegerField()
	name2 = models.CharField(max_length=200)
	time2 = models.CharField(max_length=10)
	when2 = models.CharField(max_length=10)
	numberofdays2 = models.IntegerField()
	name3 = models.CharField(max_length=200)
	time3 = models.CharField(max_length=10)
	when3 = models.CharField(max_length=10)
	numberofdays3 = models.IntegerField()
	name4 = models.CharField(max_length=200)
	time4 = models.CharField(max_length=10)
	when4 = models.CharField(max_length=10)
	numberofdays4 = models.IntegerField()
	specialinstruction = models.CharField(max_length=200)
	created_at=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name1

class Bill(models.Model):
	patientcomplaint = models.ForeignKey(PatientComplaint, on_delete=models.CASCADE, related_name='bill_patientcomplaint')
	patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bill_patient')
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bill_doctor')
	amount = models.IntegerField()
	bill_date = models.DateField(auto_now_add=True)
	paid_date = models.DateField()
	is_paid = models.BooleanField(default=False)