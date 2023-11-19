from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from account.forms import EmailValidationCheckForm, UserRegisterForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, HttpResponse, render
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .tokens import account_activation_token
from django.utils.html import format_html


class SignUp(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('signin')
    success_message ="Account created successfully"

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS, 'Please check your Mail to activate your account.')
            return redirect('signin')
        else:
            return render(request, "accounts/signup.html", {'form': form})


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Activate Your Account"
    email_body = render_to_string('accounts/activate.html', {
        'user':user,
        "domain":current_site,
        "username": urlsafe_base64_encode(force_bytes(user.username)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
    to=[user.email])
    email.send()   


def activate_user(request, username, token):
	try:
		users = force_str(urlsafe_base64_decode(username))
		user = User.objects.filter(username=users).first()
	except: user = None
	if user != None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.add_message(request, messages.SUCCESS, 'Your Account Successfully Activated')
		return redirect('signin')
	return HttpResponse('Failed not Allowed')


class LogIn(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy('signin')
    success_message = "Login success"


class PasswordReset(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/forgot.html'
    form_class = EmailValidationCheckForm
    success_message = "Your password reset request was sent"
    success_url = reverse_lazy('signin')


class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password-reset.html'
    success_url = reverse_lazy('signin')
    success_message = "Your password reset was done successfully"
