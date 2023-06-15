from django.urls import path, include
from django.views.generic import TemplateView

from .views import register, MyPasswordResetView, EmailVerify, MyLoginView

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html')),
    path('register/', register, name='register'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='registration/invalid_verify.html')),
    ]
