import datetime

from django.contrib.auth.mixins import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.utils import timezone
from django.db.models import Q
from user.forms import RegistrationForm
from .forms import AttendanceForm, NewEmployeeForm, NewDepartmentForm, LeaveForm
from .models import Department, Employee, Attendance, Leave
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
    if request.method == 'POST':
        form = NewDepartmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            department = Department()
            department.name = name
            department.description = description
            department.save()
        else:
            messages.error(request, 'Failed to add new department, please check all fields and try again')
            form = NewDepartmentForm()
            return redirect('all_departments')
    else:
        form = NewDepartmentForm()

    context = {
        'departments': departments,
        'form': form,
    }
    return render(request, 'department.html', context)


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
                local_government = employee_form.cleaned_data['local_government']
                state_of_origin = employee_form.cleaned_data['state_of_origin']
                date_of_first_appointment = employee_form.cleaned_data['date_of_first_appointment']
                date_of_present_appointment = employee_form.cleaned_data['date_of_present_appointment']
                date_of_birth = employee_form.cleaned_data['date_of_birth']
                grade_level = employee_form.cleaned_data['grade_level']
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

                retirement_by_birth = date_of_birth.replace(year=date_of_birth.year + 60)
                retirement_by_service = date_of_first_appointment.replace(year=date_of_first_appointment.year + 35)
                employee = Employee()
                employee.retirement_date_by_age = retirement_by_birth
                employee.retirement_date_by_years_of_service = retirement_by_service
                employee.staff = user
                employee.gender = gender
                employee.date_of_birth = date_of_birth
                employee.emergency = emergency
                employee.local_government = local_government
                employee.state_of_origin = state_of_origin
                employee.date_of_first_appointment = date_of_first_appointment
                employee.date_of_present_appointment = date_of_present_appointment
                employee.grade_level = grade_level
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
                context = {
                    'employees': employees,
                    'form': form,
                    'employee_form': employee_form
                }
                return render(request, 'employees.html', context)
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


def leave(request):
    if request.method == 'POST':
        employee = Employee.objects.get(staff=request.user)
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave_purpose = form.cleaned_data['leave_purpose']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['start_time']

            data = Leave()
            data.leave_purpose = leave_purpose
            data.start_time = start_time
            data.end_time = end_time
            data.applicant = employee
            data.save()
            messages.success(request, 'Your leave application has been received and is being reviewed, check the status'
                                      ' on your dashboard ')
            return redirect('dashboard')
        else:
            messages.error(request, 'Application Failed, please check all fields and try again')
            form = LeaveForm()
            context = {
                'form': form,
            }
            return render(request, 'leave.html', context)
    else:
        form = LeaveForm()
    context = {
        'form': form,
    }
    return render(request, 'leave.html', context)


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



