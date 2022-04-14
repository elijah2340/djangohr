from django import forms
from .models import Account
from django.contrib.auth.password_validation import validate_password


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Your Password',
        'class': 'form-control'
    }), validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm Your Password',
        'class': 'form-control'
    }), validators=[validate_password])

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your Firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Lastname'
        self.fields['username'].widget.attrs['placeholder'] = 'Create a Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Input Your Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Submitted Passwords Don\'t match, please try again')