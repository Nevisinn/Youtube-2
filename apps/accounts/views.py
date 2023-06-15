from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView

from .forms import UserRegistrationForm, AunthenicationForm, CustomUserChangeForm
from django.contrib.auth.views import PasswordResetView, LoginView, LogoutView, PasswordContextMixin, \
    PasswordResetCompleteView
from django.contrib.auth.tokens import default_token_generator as token_generator

from .models import Subscription
from .utils import send_email_for_verify

User = get_user_model()


class MyLoginView(LoginView):
    form_class = AunthenicationForm


class MyLogoutView(LogoutView):
    next_page = 'video_list'


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('video_list')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
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
    email_template_name = 'registration/password_reset_email.html'

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Переопределенный метод для отправки письма с инструкциями по сбросу пароля.
        """
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        email = render_to_string(email_template_name, context)

        send_mail(subject, email, from_email, [to_email], html_message=html_email_template_name)


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "password_reset_done.html"
    title = "Password reset sent"


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('personal_account')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


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
            send_email_for_verify(request, user)
            return redirect('confirm_email')
    else:
        return HttpResponse('Неверный запрос')
    return render(request, 'register.html', {'form': form})


@login_required
def personal_account(request):
    context = {
        'user': request.user,
    }
    return render(request, 'account.html', context)


@login_required
def subscribe_toggle(request, channel_username):
    channel_user = get_object_or_404(User, username=channel_username)
    subscriber = request.user

    if Subscription.objects.filter(subscriber=subscriber, channel_user=channel_user).exists():
        # Пользователь уже подписан, отписываем его
        Subscription.objects.filter(subscriber=subscriber, channel_user=channel_user).delete()
        subscribed = False
        channel_user.subscribers_count -= 1
    else:
        # Пользователь не подписан, подписываем его
        Subscription.objects.create(subscriber=subscriber, channel_user=channel_user)
        subscribed = True
        channel_user.subscribers_count += 1

    channel_user.save()

    subscribers_count = channel_user.subscribers.count()

    return JsonResponse({'subscribed': subscribed, 'subscribers_count': subscribers_count})


def subscribed_channels(request):
    subscriptions = Subscription.objects.filter(subscriber_id=request.user.id)
    channel_users = User.objects.filter(id__in=subscriptions.values_list('channel_user_id', flat=True))
    return render(request, 'subscribed_channels.html', {'channel_users': channel_users})
