from django.contrib.auth.models import Group

def hasGroup(user, groupName):
    try:
        group = Group.objects.get(name=groupName)
        return True if group in user.groups.all() else False
    except:
        return False

def menu_processor(request):
    menu = {}
    user = request.user
    if hasGroup(user, 'doctor'):
        #menu['Appointments'] = '/appointments'
        menu['Cases'] = '/case'
        menu['New Patient'] = '/register'
        menu['Manage Patient'] = '/manage_patient'
    elif hasGroup(user, 'patient'):
        menu['Reports'] = '/reports'
        menu['Appointments'] = '/appointments'
        menu['Medication'] = '/medicines'
        menu['Bills'] = '/bill'
        menu['Cases'] = '/case'
    elif hasGroup(user, 'receptionist'):
        menu['New Patient'] = '/register'
        #menu['Manage Appointments'] = '/appointments'
        #menu['New Appointment'] = '/book'
        #menu['Bills'] = '/bill'
        menu['Cases'] = '/case'
        menu['Generate Case'] = '/generate'
    elif hasGroup(user, 'lab_attendant'):
        menu['Reports'] = '/reports'
        menu['Generate Report'] = '/reports/generate'
    elif hasGroup(user, 'inventory_manager'):
        menu['All Stock'] = ''
        menu['Stock Details'] = ''

    return {'menu': menu}
