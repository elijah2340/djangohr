import datetime
from django.contrib.auth.mixins import *
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.utils import timezone
from django.db.models import Q
from user.forms import RegistrationForm
from .forms import AttendanceForm, NewEmployeeForm, NewDepartmentForm, LeaveForm, DirectorForm, DirectorNextOfKinForm
from .models import Department, Employee, Attendance, Leave, Director, NextOfKin, DirectorNextOfKin
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
                if retirement_by_birth < retirement_by_service:
                    employee.actual_retirement = retirement_by_birth
                else:
                    employee.actual_retirement = retirement_by_service
                employee.name = user.first_name + user.last_name
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


def allDirectors(request):
     if request.user.has_perm('is_admin'):
        directors = Director.objects.all().order_by('-staff__date_joined')
        if request.method == 'POST':
            form = RegistrationForm(request.POST, request.FILES)
            director_form = DirectorForm(request.POST)
            if form.is_valid() and director_form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                profile_picture = form.cleaned_data['profile_picture']
                gender = director_form.cleaned_data['gender']
                emergency = director_form.cleaned_data['emergency']
                local_government = director_form.cleaned_data['local_government']
                state_of_origin = director_form.cleaned_data['state_of_origin']
                date_of_first_appointment = director_form.cleaned_data['date_of_first_appointment']
                date_of_present_appointment = director_form.cleaned_data['date_of_present_appointment']
                date_of_birth = director_form.cleaned_data['date_of_birth']
                grade_level = director_form.cleaned_data['grade_level']
                department = director_form.cleaned_data['department']
                language = director_form.cleaned_data['language']
                nuban = director_form.cleaned_data['nuban']
                bank = director_form.cleaned_data['bank']
                salary = director_form.cleaned_data['salary']
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
                director = Director()
                if retirement_by_birth < retirement_by_service:
                    director.actual_retirement = retirement_by_birth
                else:
                    director.actual_retirement = retirement_by_service

                director.retirement_date_by_age = retirement_by_birth
                director.retirement_date_by_years_of_service = retirement_by_service
                director.staff = user
                director.gender = gender
                director.date_of_birth = date_of_birth
                director.emergency = emergency
                director.local_government = local_government
                director.state_of_origin = state_of_origin
                director.date_of_first_appointment = date_of_first_appointment
                director.date_of_present_appointment = date_of_present_appointment
                director.grade_level = grade_level
                director.department = department
                director.language = language
                director.nuban = nuban
                director.bank = bank
                director.salary = salary
                director.save()

                # user activation mail
                current_site = get_current_site(request)
                mail_subject = 'Please Activate Your Account'
                message = render_to_string('department/director_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'password': password,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, 'Director successfully registered, waiting for Director to confirm account through mail ')
                return redirect('directors')
            else:
                messages.error(request, 'Failed to add new employee, please check all fields and try again')
                context = {
                    'directors': directors,
                    'form': form,
                    'director_form': director_form
                }
                return render(request, 'directors.html', context)
        else:
            form = RegistrationForm()
            director_form = DirectorForm()

        context = {
            'directors': directors,
            'form': form,
            'director_form': director_form
        }
        return render(request, 'directors.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, OverflowError, Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        messages.success(request, 'Your Account Has Been Successfully Activated, Please Login')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link, Please Contact The Management.')
        return redirect('login')

def employeeactivate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, OverflowError, Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your Account Has Been Successfully Activated, Please Login')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link, Please Contact The Management.')
        return redirect('login')


def employeeProfile(request, id):
    employee = Employee.objects.get(emp_id=id)
    try:
        family = NextOfKin.objects.get(employee=employee)
    except NextOfKin.DoesNotExist:
        family = None
    try:
        director = Director.objects.get(department=employee.department)
    except Director.DoesNotExist:
        director = None
    context = {
        'employee': employee,
        'director': director,
        'family': family
    }
    return render(request, 'employee_profile.html', context)


def singleDirectorProfile(request, id):
    director = Director.objects.get(id=id)
    try:
        family = DirectorNextOfKin.objects.get(staff=director)
    except NextOfKin.DoesNotExist:
        family = None
    context = {
        'director': director,
        'family': family
    }
    return render(request, 'single_director_profile.html', context)


def directorProfile(request):
    director = Director.objects.get(staff=request.user)
    try:
        family = DirectorNextOfKin.objects.get(staff=director)
    except DirectorNextOfKin.DoesNotExist:
        family = None
    if request.method == 'POST':
        form = DirectorNextOfKinForm(request.POST)
        if form.is_valid():
            name1 = form.cleaned_data['name1']
            relationship1 = form.cleaned_data['relationship1']
            phone_number1 = form.cleaned_data['phone_number1']
            name2 = form.cleaned_data['name1']
            relationship2 = form.cleaned_data['relationship1']
            phone_number2 = form.cleaned_data['phone_number1']

            kin = DirectorNextOfKin()
            kin.staff = director
            kin.name1 = name1
            kin.relationship1 = relationship1
            kin.phone_number1 = phone_number1
            kin.name2 = name2
            kin.relationship2 = relationship2
            kin.phone_number2 = phone_number2
            kin.save()
            messages.success(request, 'Next of Kin added successfully')
            return redirect('director_profile')
        else:
            messages.error(request, 'Failed to add next of kin, please check all fields and try again')
            context = {
                'form': form,
                'family': family,
                'director': director,
            }
            return render(request, 'director_profile.html', context)
    else:
        form = DirectorNextOfKinForm()
        context = {
            'form': form,
            'family': family,
            'director': director,
        }
        return render(request, 'director_profile.html', context)


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

def department_leave(request):
    director = Director.objects.get(staff=request.user)
    department = Department.objects.get(name=director.department)
    pending_leave = Leave.objects.filter(status='PENDING', applicant__department=department)
    approved_leave = Leave.objects.filter(status='APPROVED', applicant__department=department)
    declined_leave = Leave.objects.filter(status='DECLINED', applicant__department=department)
    all_leave = Leave.objects.filter(applicant__department=department).order_by('-date_applied')
    for leave in all_leave:
        if datetime.date.today() >= leave.end_time:
            leave.completed = True
            leave.save()
    context = {
        'pending_leave': pending_leave,
        'approved_leave': approved_leave,
        'declined_leave': declined_leave,
        'all_leave': all_leave
    }

    return render(request, 'department_leave.html', context)


def retiring_staff(request):
    director = Director.objects.get(staff=request.user)
    department = Department.objects.get(name=director.department)
    today = datetime.datetime.today()
    day = 0
    to_retire = None
    for i in range(31):
        if day < 30:
            day += 1
            retirering_staff = Employee.objects.filter(department=department,
                                                       actual_retirement=datetime.datetime(today.year, today.month,
                                                                                           day))
            if retirering_staff:
                to_retire = retirering_staff
    context = {
        'retirering_staff': to_retire
    }
    return render(request, 'retirering_staff.html', context)

def approve_leave(request, id):
    try:
        applicant_leave = Leave.objects.get(applicant__id=id, status='PENDING')
    except Leave.DoesNotExist:
        applicant_leave = None
    applicant_leave.status = 'APPROVED'
    applicant_leave.save()
    messages.success(request, 'Leave Status Successfully Updated')
    return redirect('department_leave')


def decline_leave(request, id):
    try:
        leave_to_decline = Leave.objects.get(applicant__id=id, status='PENDING')
    except Leave.DoesNotExist:
        leave_to_decline = None
    leave_to_decline.status = 'DECLINED'
    leave_to_decline.save()
    messages.success(request, 'Leave Status Successfully Updated')
    return redirect('department_leave')


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
    all_attendance = Attendance.objects.all()

    context = {
        'attendance': all_attendance
    }
    return render(request, 'attendance.html', context)

def departmentattendance(request):
    director = Director.objects.get(staff=request.user)
    all_attendance = Attendance.objects.filter(staff__department=director.department)

    context = {
        'attendance': all_attendance
    }
    return render(request, 'departmentattendance.html', context)


def searchview(request):
    employees = None
    if 'query' in request.GET:
        query = request.GET['query']
        if query:
            employees = Employee.objects.order_by('-staff__date_joined').filter(Q(name__icontains=query) | Q(role__icontains=query))
            employee_count = employees.count()
            if employees.count() == 0:
                messages.warning(request, f'No staff with \'{query}\' found.')
            else:
                messages.success(request, f'{employee_count} staff found.')
    context = {
        'employees': employees,
    }
    return render(request, 'search.html', context)