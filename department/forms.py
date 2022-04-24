from django import forms
from .models import Attendance, Employee, Department, NextOfKin, Leave
from django.utils import timezone
from django.db.models import Q
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class AttendanceForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Attendance.STATUS,widget=forms.Select(attrs={'class':'form-control w-50'}))
    staff = forms.ModelChoiceField(Employee.objects.filter(Q(attendance__status=None) | ~Q(attendance__date = timezone.localdate())), widget=forms.Select(attrs={'class':'form-control w-50'}))
    class Meta:
        model = Attendance
        fields = ['status', 'staff']


class NewEmployeeForm(forms.ModelForm):
    date_of_first_appointment = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': '1990-01-10',
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    date_of_present_appointment = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': '1990-01-10',
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': '1990-01-10',
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = Employee
        fields = ['gender', 'emergency', 'role', 'department', 'language', 'nuban', 'bank', 'salary', 'local_government'
                  , 'state_of_origin', 'date_of_first_appointment', 'date_of_birth', 'date_of_present_appointment', 'grade_level']

    def __init__(self, *args, **kwargs):
        super(NewEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['emergency'].widget.attrs['placeholder'] = 'Enter an emergency line'
        self.fields['nuban'].widget.attrs['placeholder'] = 'Input Bank Account Number'
        self.fields['bank'].widget.attrs['placeholder'] = 'Input Bank'
        self.fields['salary'].widget.attrs['placeholder'] = 'Input Salary'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(NewEmployeeForm, self).clean()


class NewDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(NewDepartmentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(NewDepartmentForm, self).clean()


class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = NextOfKin
        fields = ['name1', 'relationship1', 'phone_number1', 'name2', 'relationship2', 'phone_number2']

    def __init__(self, *args, **kwargs):
        super(NextOfKinForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(NextOfKinForm, self).clean()


class LeaveForm(forms.ModelForm):
    start_time = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': '1990-01-10',
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    end_time = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': '1990-01-10',
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    class Meta:
        model = Leave
        fields = ['leave_purpose', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(LeaveForm, self).clean()


