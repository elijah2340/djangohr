from django.shortcuts import render
from department.models import Employee, Department, HOD
from django.views.generic import *
from django.contrib.auth.decorators import login_required, permission_required


# remember to come back an include login reqired mixin
@login_required(login_url='login')
def adminDashboard(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    hod = HOD.objects.all()

    employees_count = employees.count()
    departments_count = departments.count()
    hod_count = hod.count()
    context = {
        'employees_count': employees_count,
        'departments_count': departments_count,
        'hod_count': hod_count
    }
    if request.user.has_perm("is_admin"):
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'employee_dashboard.html')


