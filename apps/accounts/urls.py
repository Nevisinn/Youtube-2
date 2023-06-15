from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from django.views.generic import TemplateView

from .views import register, MyPasswordResetView, EmailVerify, MyLoginView, personal_account, subscribe_toggle, \
    MyLogoutView, PasswordResetDoneView, MyPasswordResetCompleteView, edit_profile, subscribed_channels

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm_email', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),
    path('register', register, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('verify_email/<uidb64>/<token>', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify', TemplateView.as_view(template_name='registration/invalid_verify.html')),
    path('account/', personal_account, name='personal_account'),
    path('subscribe_toggle/<str:channel_username>/', subscribe_toggle, name='subscribe_toggle'),
    path('subscribed_channels/', subscribed_channels, name='subscribed_channels'),
    ]
