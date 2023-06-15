from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from accounts.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, get_user_model
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .forms import UserRegistrationForm, AunthenicationForm
from django.contrib.auth.views import PasswordResetView, LoginView
from django.contrib.auth.tokens import default_token_generator as token_generator
from .utils import send_email_for_verify

User = get_user_model()


class MyLoginView(LoginView):
    form_class = AunthenicationForm


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')


    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'


def register(request):
    if request.method == 'GET':
        form = UserRegistrationForm
    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify()
            return redirect('confirm_email')
    else:
        return HttpResponse('Неверный запрос')
    return render(request, 'register.html', {'form': form})


