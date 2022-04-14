import datetime

from django.contrib.auth.mixins import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.utils import timezone
from django.db.models import Q
from user.forms import RegistrationForm
from .forms import AttendanceForm, NewEmployeeForm
from .models import Department, Employee, Attendance, HOD
from user.models import Account
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages, auth
import requests
from django.contrib.auth.decorators import login_required, permission_required


def allDepartments(request):
    departments = Department.objects.all().order_by('-date_created')

    context = {
        'departments': departments
    }
    return render(request, 'department.html', context)


def allHods(request):
    hods = HOD.objects.all().order_by('-date_added')

    context = {
        'hods': hods
    }
    return render(request, 'hod.html', context)


def singleDepartment(request, slug):
    department = Department.objects.get(slug=slug)
    employees = Employee.objects.filter(department=department).order_by('-staff__date_joined')

    context = {
        'department': department,
        'employees': employees
    }

    return render(request, 'single_department.html', context)


def allEmployees(request):
     if request.user.has_perm('is_admin'):
        employees = Employee.objects.all().order_by('-staff__date_joined')
        if request.method == 'POST':
            form = RegistrationForm(request.POST, request.FILES)
            employee_form = NewEmployeeForm(request.POST)
            if form.is_valid() and employee_form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                profile_picture = form.cleaned_data['profile_picture']
                gender = employee_form.cleaned_data['gender']
                emergency = employee_form.cleaned_data['emergency']
                role = employee_form.cleaned_data['role']
                department = employee_form.cleaned_data['department']
                language = employee_form.cleaned_data['language']
                nuban = employee_form.cleaned_data['nuban']
                bank = employee_form.cleaned_data['bank']
                salary = employee_form.cleaned_data['salary']
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    profile_picture=profile_picture,
                    password=password
                )
                user.phone_number = phone_number
                user.save()

                employee = Employee()
                employee.staff = user
                employee.gender = gender
                employee.emergency = emergency
                employee. role = role
                employee.department = department
                employee.language = language
                employee.nuban = nuban
                employee.bank = bank
                employee.salary = salary
                employee.save()

                # user activation mail
                current_site = get_current_site(request)
                mail_subject = 'Please Activate Your Account'
                message = render_to_string('department/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'password': password,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, 'Employee successfully registered, waiting for employee to confirm account ')
                return redirect('employees')
            else:
                messages.error(request, 'Failed to add new employee, please check all fields and try again')
                form = RegistrationForm()
                employee_form = NewEmployeeForm()
                return redirect('employees')
        else:
            form = RegistrationForm()
            employee_form = NewEmployeeForm()

        context = {
            'employees': employees,
            'form': form,
            'employee_form': employee_form
        }
        return render(request, 'employees.html', context)


def employeeProfile(request, id):
    employee = Employee.objects.get(emp_id=id)
    context = {
        'employee': employee
    }
    return render(request, 'employee_profile.html', context)


# remember to later add LoginRequiredMixin
class Attendance_New(CreateView):
    model = Attendance
    form_class = AttendanceForm
    # login_url = 'hrms:login'
    template_name = 'attendance.html'
    success_url = reverse_lazy('attendance')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.localdate()
        pstaff = Attendance.objects.filter(Q(status='PRESENT') & Q(date=timezone.localdate()))
        context['present_staffers'] = pstaff
        return context

def attendance(request):
    form = AttendanceForm(request.POST)
    staff = Employee.objects.get(staff=request.user)
    if request.method == 'POST':
        if form.is_valid():
            data = Attendance()
            data.staff = staff
            data.first_in = datetime.datetime.now()
            data.status = "PRESENT"
            data.save()
            return render(request, 'attendance.html')
    if Attendance.objects.filter(staff=staff, date=timezone.localdate()).exists():
        context = {
            'signed_in': True
        }
        return render(request, 'attendance.html', context)
    else:
        return render(request, 'attendance.html', {'form':AttendanceForm()})



# remember to add LoginRequiredMixin
class Attendance_Out(View):
    # login_url = 'login'
    def get(self, request,*args, **kwargs):
        user = Attendance.objects.get(Q(staff__id=self.kwargs['pk']) & Q(status='PRESENT')& Q(date=timezone.localdate()))
        user.last_out = timezone.localtime()
        user.save()
        return redirect('attendance')



