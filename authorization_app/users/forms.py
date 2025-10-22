from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from .models import Customer, Profile


User = get_user_model()


class CustomerChangeForm(UserChangeForm):
    """
    Форма для редактирования профиля пользователя.
    """

    class Meta:
        model = Customer
        fields = ['email', 'username']


class ProfileForm(forms.ModelForm):
    """
    Форма для обновления дополнительной информации профиля.
    """
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio']


class EmailChangeForm(forms.Form):
    """
    Форма для смены email-адреса пользователя.
    """
    new_email = forms.EmailField(
        label='Новый email',
        help_text='Введите новый email-адресс.'
    )

    def check_unique_email(self):
        new_email = self.cleaned_data['new_email']
        if User.objects.filter(
            email=new_email
        ).exclude(pk=self.user.pk).exists():
            raise ValidationError(
                f'Почта {new_email} уже используется другим пользователем.'
            )
        return new_email
