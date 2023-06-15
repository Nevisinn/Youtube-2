from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as DjangoAuthenticationForm
from django.core.exceptions import ValidationError

from apps.accounts.utils import send_email_for_verify

User = get_user_model()


class AunthenicationForm(DjangoAuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                if not self.user_cache.email_verify:
                    send_email_for_verify(self.request, self.user_cache)
                    raise ValidationError(
                        'Почта не подтверждена, проверьте свою почту',
                        code="invalid_login",
                    )
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Почта', required=True, help_text='Обязательное поле')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email',)


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']
        exclude = ['password']
