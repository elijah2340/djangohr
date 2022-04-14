from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from user.forms import RegistrationForm
from user.models import Account
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages, auth
import requests


def registerview(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            profile_picture = form.cleaned_data['profile_picture']
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_picture= profile_picture,
                password=password
            )
            user.phone_number = phone_number
            user.save()

            # # user profile creation
            # profile = UserProfile()
            # profile.user_id = user.id
            # profile.profile_picture = 'default/default.jpeg'
            # profile.save()

            # user activation mail
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('user/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/user/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


def loginview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You Are Now Logged In')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials, Please Try Again')
            return redirect('login')
    return render(request, 'user/login.html')

@login_required(login_url='login')
def logoutview(request):
    auth.logout(request)
    messages.success(request, 'You Have Been Logged Out, Please Come Back Soon')
    return redirect('login')


def activateview(request, uidb64, token):
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
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')

def forgotpasswordview(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('user/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'A mail with a password reset link has been sent to yur email address [' + email + ']' )
            return redirect('login')
        else:
            messages.error(request, 'Account with email ' + email + ' does not exist')
            return redirect('forgotpassword')
    return render(request, 'user/forgotpassword.html')


def resetpassword_validateview(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, OverflowError, Account.ObjectDoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Reset Your Password')
        return redirect('reset-password')
    else:
        messages.error(request, 'This link has expired please request another')
        return redirect('login')


def resetpasswordview(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'You have successfully reset your password , please login')
            return redirect('login')
        else:
            messages.error(request, 'passwords do not match')
            return redirect('reset-password')
    return render(request, 'user/reset-password.html')
