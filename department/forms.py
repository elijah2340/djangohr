from django import forms
from .models import Attendance, Employee
from django.utils import timezone
from django.db.models import Q


class AttendanceForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Attendance.STATUS,widget=forms.Select(attrs={'class':'form-control w-50'}))
    staff = forms.ModelChoiceField(Employee.objects.filter(Q(attendance__status=None) | ~Q(attendance__date = timezone.localdate())), widget=forms.Select(attrs={'class':'form-control w-50'}))
    class Meta:
        model = Attendance
        fields = ['status', 'staff']


class NewEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['gender', 'emergency', 'role', 'department', 'language', 'nuban', 'bank', 'salary']

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
