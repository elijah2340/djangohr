from django.shortcuts import render, redirect
from department.models import Employee, Department, NextOfKin, Leave, Director
from django.views.generic import *
from django.contrib.auth.decorators import login_required, permission_required
from department.forms import NextOfKinForm
from django.contrib import messages
from django.db.models import Q
import datetime


# remember to come back an include login reqired mixin
@login_required(login_url='login')
def adminDashboard(request):
    if request.user.has_perm("is_admin"):
        employees = Employee.objects.all()
        departments = Department.objects.all()
        employees_count = employees.count()
        departments_count = departments.count()
        directors = Director.objects.all
        context = {
            'employees_count': employees_count,
            'departments_count': departments_count,
            'directors': directors
        }

        return render(request, 'dashboard.html', context)
    elif request.user.is_staff:
        director = Director.objects.get(staff=request.user)
        department = Department.objects.get(name=director.department)
        staffs = Employee.objects.filter(department=department)
        try:
            leave = Leave.objects.filter(status='PENDING', applicant__department=department)
        except Leave.DoesNotExist:
            leave = None
        today = datetime.datetime.today()
        day = 0
        to_retire = None
        for i in range(31):
            if day < 30:
                day += 1
                retirering_staff = Employee.objects.filter(department=department, actual_retirement=datetime.datetime(today.year, today.month, day))
                if retirering_staff:
                    to_retire = retirering_staff


        context = {
            'department': department,
            'director': director,
            'staffs': staffs,
            'leave': leave,
            'retirering_staff': to_retire
        }
        return render(request, 'director_dashboard.html', context)
    else:
        employee = Employee.objects.get(staff=request.user)
        family = NextOfKin.objects.filter(employee=employee)
        try:
            director = Director.objects.get(department=employee.department)
        except Director.DoesNotExist:
            director = None
        try:
            leave = Leave.objects.get((~Q(status='DECLINED')), applicant=employee, completed=False)
            if datetime.date.today() >= leave.end_time:
                leave.completed = True
                leave.save()
        except Leave.DoesNotExist:
            leave = None
        try:
            previous_applications = Leave.objects.filter((~Q(status='PENDING')), applicant=employee).order_by('-date_applied')
        except Leave.DoesNotExist:
            previous_applications = None
        previous = previous_applications.count()
        if request.method == 'POST':
            form = NextOfKinForm(request.POST)
            if form.is_valid():
                name1 = form.cleaned_data['name1']
                relationship1 = form.cleaned_data['relationship1']
                phone_number1 = form.cleaned_data['phone_number1']
                name2 = form.cleaned_data['name1']
                relationship2 = form.cleaned_data['relationship1']
                phone_number2 = form.cleaned_data['phone_number1']

                kin = NextOfKin()
                kin.employee = employee
                kin.name1 = name1
                kin.relationship1 = relationship1
                kin.phone_number1 = phone_number1
                kin.name2 = name2
                kin.relationship2 = relationship2
                kin.phone_number2 = phone_number2
                kin.save()
                messages.success(request, 'Next of Kin added successfully')
                return redirect('dashboard')
            else:
                messages.error(request, 'Failed to add next of kin, please check all fields and try again')
                context = {
                    'form': form,
                    'family': family,
                    'leave': leave,
                    'previous_applications': previous_applications,
                    'previous': previous,
                    'director': director,
                }
                return render(request, 'employee_dashboard.html', context)
        else:
            form = NextOfKinForm()
            context = {
                'employee': employee,
                'form': form,
                'family': family,
                'leave': leave,
                'previous_applications': previous_applications,
                'previous': previous,
                'director': director,
            }
            return render(request, 'employee_dashboard.html', context)


