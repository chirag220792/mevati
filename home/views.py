from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User,Group
from account.models import Profile
from django.template.context_processors import csrf
from home.context_processors import hasGroup
from django.contrib.auth.models import User, Group
from .models import *
from datetime import datetime
from django.utils import timezone

# Create your views here.
@login_required()
def home(request):
    messages.add_message(request, messages.INFO, 'Welcome to The Clinic Portal.')
    return render(request, 'home/base.html')


# Create your views here.
@login_required
def myProfile(request):
    c={}
    if hasGroup(request.user, 'patient'):
        c['isPatient'] = True
    return render(request, 'profiles/my_profile.html', c)

@login_required
def register(request):
    if hasGroup(request.user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        return render(request, 'profiles/register.html')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

@login_required
def doRegister(request):
    if hasGroup(request.user, 'receptionist'):
        """ username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username Already Exists.')
            return HttpResponseRedirect('/register')
        password = request.POST.get('password1')
        cpassword = request.POST.get('password2')
        if not password == cpassword:
            messages.add_message(request, messages.ERROR, 'Passwords not matching.')
            return HttpResponseRedirect('/register') """
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = first_name+'.'+last_name
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username Already Exists.')
            return HttpResponseRedirect('/register')
        contact_no = request.POST.get('contact_no')
        if not contact_no.isdigit():
            messages.add_message(request, messages.ERROR, 'Wrong Contact no.')
            return HttpResponseRedirect('/register')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        sex_choices = request.POST.get('sex_choices')
        email = request.POST.get('email')
        patient = User.objects.create_user(username=username, password='123', first_name=first_name, last_name=last_name, email=email)
        patient.profile = Profile(contact_no=int(contact_no), address=address, dob=dob, age = age, blood_group=blood_group, sex=sex_choices)
        patient.profile.save()
        patient.save()

        group = Group.objects.get(name='patient')
        group.user_set.add(patient)
        group.save()

        messages.add_message(request, messages.WARNING, 'Successfully Registered '+username)
        return HttpResponseRedirect('/manage_patient')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

# All Users
@login_required
def userlist(request):
    users = User.objects.all()
    return render(request, "user/userlist.html", {"users": users})

#Manage Patient
@login_required
def manage_patient(request):
    if hasGroup(request.user, 'doctor'):
        c = {}
        c.update(csrf(request))
        c['patients'] = User.objects.filter(groups__name='patient')
        return render(request, 'case/manage_pateint.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def edit_patient(request, patient_id):
    patient = Profile.objects.get(user=patient_id)
    return render(request, 'profiles/edit_patient.html', {'patient':patient})

@login_required
def edit_patient_save(request):
    if hasGroup(request.user, 'doctor'):
        patient_id = request.POST.get("patient_id")
        #print("patinet ID"+patient_id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = first_name+'.'+last_name
        contact_no = request.POST.get('contact_no')
        if not contact_no.isdigit():
            messages.add_message(request, messages.ERROR, 'Wrong Contact no.')
            return HttpResponseRedirect('/register')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        sex_choices = request.POST.get('sex_choices')
        email = request.POST.get('email')
        

        profile = User.objects.get(id = patient_id)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.username = username
        profile.email = email
        profile.save()


        patient = Profile.objects.get(user = patient_id)
        patient.contact_no = contact_no
        patient.address = address
        patient.dob = dob
        patient.age = age
        patient.blood_group = blood_group
        patient.sex_choices = sex_choices

        patient.save()
        messages.add_message(request, messages.WARNING, 'Successfully Update '+username)
        return HttpResponseRedirect('/manage_pateint')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

@login_required
def generate(request, patient_id):
    patient = Profile.objects.get(user=patient_id)
    patientPastHistorys = PastHistory.objects.filter(patient=patient_id)
    medicinesnames = Medicines.objects.all
    results=ComplaintList.objects.all
    #patientcheckups = PatientCheckUp.objects.filter(patient=patient_id)
    patientcomplaints = PatientComplaint.objects.filter(patientcheckup__patient=patient_id)
    patientbills = Bill.objects.filter(patient=patient_id)
    
    #print(patientPastHistorys)
    return render(request, 'case/generate.html', {'patient':patient,'patientPastHistorys':patientPastHistorys, 'results':results, 'medicinesnames':medicinesnames, 'patientcomplaints':patientcomplaints, 'patientbills':patientbills})

@login_required
def history(request):
    if hasGroup(request.user, 'doctor'):
        patient_id=request.POST.get('patient_id')
        patient = User.objects.get(id = patient_id)
        #user_id = request.POST.get("user_id")
        history_type = request.POST.get('HistoryType')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        created_at = datetime.now()
        history = PastHistory(patient=patient, doctor=request.user, history_type = history_type, subject = subject, description=description, created_at=created_at)
        history.save()
        messages.add_message(request, messages.INFO, 'Successfully Patient History')
        return HttpResponseRedirect('/generate/'+patient_id)
    else:    
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')


@login_required
def patientcheckup_save(request):
    if hasGroup(request.user, 'doctor'):
        patient_id=request.POST.get('patient_id')
        patient = User.objects.get(id = patient_id)
        patient_weghit = request.POST.get('patient_weghit')
        patient_height = request.POST.get('patient_height')
        patient_lmpdate = request.POST.get('patient_lmpdate')
        patient_gerenalcondition = request.POST.get('patient_gerenalcondition')
        patient_temperature = request.POST.get('patient_temperature')
        patient_pulse = request.POST.get('patient_pulse')
        patient_systolicpressure = request.POST.get('patient_systolicpressure')
        patient_dystolicpressure = request.POST.get('patient_dystolicpressure')
        patient_respiratoryrate = request.POST.get('patient_respiratoryrate')
        patient_spo2 = request.POST.get('patient_spo2')
        patient_checkupremark = request.POST.get('patient_checkupremark')
        patient_respiratorysystem = request.POST.get('patient_respiratorysystem')
        patient_cardiovascularsystem = request.POST.get('patient_cardiovascularsystem')
        patient_centralnervoussystem = request.POST.get('patient_centralnervoussystem')
        patient_palpitation1 = request.POST.get('patient_palpitation1')
        patient_palpitation2 = request.POST.get('patient_palpitation2')
        patient_palpitation3 = request.POST.get('patient_palpitation3')
        patient_provisionaldiagnosis = request.POST.get('patient_provisionaldiagnosis')
        created_at = datetime.now()
        #insert into table
        patientcheckup = PatientCheckUp(patient=patient, doctor=request.user, lmpdob = patient_lmpdate, weight = patient_weghit, height = patient_height, generalcondition = patient_gerenalcondition, temperature = patient_temperature, pulse = patient_pulse, systolicpressure = patient_systolicpressure, dystolicpressure = patient_dystolicpressure, respiratoryrate =patient_respiratoryrate, spo2 = patient_spo2,checkupremake = patient_checkupremark, respiratorysystem = patient_respiratorysystem, cardiovascularsystem = patient_cardiovascularsystem, centralnervoussystem = patient_centralnervoussystem, palpitation1 = patient_palpitation1, palpitation2 = patient_palpitation2, palpitation3 = patient_palpitation3, provisionaldiagnosis = patient_provisionaldiagnosis, filed_date = created_at)
        patientcheckup.save()

        #Change PatientComplaint DataBase Table
        patient_complaint1 = request.POST.get('patient_complaint1')
        patient_since1 = request.POST.get('sincetime1')
        patient_complaint2 = request.POST.get('patient_complaint2')
        patient_since2 = request.POST.get('sincetime2')
        patient_complaint3 = request.POST.get('patient_complaint3')
        patient_since3 = request.POST.get('sincetime3')
        #insert into table PatientComplaint
        patientcomplaint = PatientComplaint(patientcheckup = patientcheckup, complaint1 = patient_complaint1, since1 = patient_since1, complaint2 = patient_complaint2, since2 = patient_since2, complaint3 = patient_complaint3, since3 = patient_since3)
        patientcomplaint.save()

        #Change PrescriptionMedicine DataBase Table
        patient_medicinesname = request.POST.get('patient_medicines')
        patient_medicinestime = request.POST.get('patient_medicinestime')
        patient_medicineswhen = request.POST.get('patient_medicineswhen')
        patient_medicinesnumberofdays = request.POST.get('patient_medicinesdays')
        patient_medicinesspecialinstruction = request.POST.get('patient_medicinesremark')
        created_at = datetime.now()

        #insert into table PrescriptionMedicine
        prescriptionedicine = PrescriptionMedicine(patientcheckup = patientcheckup, doctor=request.user, name = patient_medicinesname, time = patient_medicinestime, when = patient_medicineswhen, numberofdays = patient_medicinesnumberofdays, specialinstruction = patient_medicinesspecialinstruction, created_at= created_at)
        prescriptionedicine.save()

        #insert into table Bill
        bill = Bill(patientcomplaint = patientcomplaint, patient = patient, doctor = request.user, amount=0, paid_date = created_at)
        bill.save()

        messages.add_message(request, messages.INFO, 'Successfully Generated Case')
        return HttpResponseRedirect('/generate/'+patient_id)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def bill_save(request):
    if hasGroup(request.user, 'doctor'):
        patient_id=request.POST.get('patient_id')
        patient = User.objects.get(id = patient_id)
        patientcomplaint_id=request.POST.get('patientcheckup_id')
        patientcomplaint = PatientComplaint.objects.get(id = patientcomplaint_id)
        amount = request.POST.get('amount')
        created_at = datetime.now()
        patientbill_id=request.POST.get('patientbill_id')
        billpatient = Bill.objects.get(id = patientbill_id)
        billpatient.patientcomplaint = patientcomplaint
        billpatient.patient = patient
        billpatient.doctor = request.user
        billpatient.amount = amount
        billpatient.paid_date = created_at
        billpatient.is_paid = True
        
        billpatient.save()
        messages.add_message(request, messages.INFO, 'Successfully Bill Paid')
        return HttpResponseRedirect('/generate/'+patient_id)
    else:    
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

# All Bill
@login_required
def all_bill(request):
    bills = Bill.objects.all()
    return render(request, "bill/billlist.html", {"bills": bills})