import logging

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from .forms import CustomerChangeForm, ProfileForm, EmailChangeForm
from .models import Customer, Profile


# Настройка логирования
log_file_path = 'auth_app.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def home(request):
    """
    Отображает главную страницу сайта.
    Если пользователь авторизован, перенаправляет его
    на страницу списка пользователей.
    """
    if request.user.is_authenticated:
        return redirect('user_list')
    else:
        return render(request, 'home.html')


def user_list(request):
    """
    Отображает список всех зарегистрированных пользователей.
    """
    users = Customer.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def profile(request):
    """
    Отображает информацию о профиле текущего пользователя.
    Создает профиль, если его еще нет.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """
    Позволяет пользователю редактировать свои данные и информацию профиля.
    Обрабатывает формы и сохраняет изменения.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = CustomerChangeForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            try:
                user_form.save()
                profile_form.save()
                messages.success(
                    request, 'Профиль успешно обновлен.'
                )
                logger.info(
                    'Профиль успешно обновлен. '
                    f'Request: {request.POST.dict()}'
                )
                return redirect('profile')
            except Exception as e:
                messages.error(
                    request, f'Ошибка при сохранении профиля: {e}'
                )
                logger.error(
                    f'Ошибка при сохранении профиля: {e}. '
                    f'Request: {request.POST.dict()}'
                )

        else:
            messages.error(
                request, 'В форме есть ошибки, проверьте введенные данные.'
            )
            logger.error(
                f'В форме есть ошибки, проверьте введенные данные. '
                f'Request: {request.POST.dict()}'
            )

    else:
        user_form = CustomerChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        'users/edit_profile.html',
        {'user_form': user_form, 'profile_form': profile_form}
    )


@login_required
def change_password(request):
    """
    Позволяет пользователю изменить свой пароль.
    После успешного изменения обновляет сессию и отображает сообщение.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():

            try:
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(
                    request, 'Пароль успешно изменен.'
                )
                logger.info(
                    'Пароль успешно изменен. '
                    f'Request: {request.POST.dict()}'
                )
            except Exception as e:
                messages.error(
                    request, f'Ошибка при смене пароля: {e}'
                )
                logger.error(
                    f'Ошибка при смене пароля: {e}. '
                    f'Request: {request.POST.dict()}'
                )

        else:
            messages.error(
                request, 'В форме есть ошибки, проверьте введенные данные.'
            )
            logger.error(
                'В форме есть ошибки, проверьте введенные данные. '
                f'Request: {request.POST.dict()}'
            )

    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'users/change_password.html',
        {'form': form}
    )


@login_required
def change_email(request):
    """
    Позволяет пользователю изменить свой email.
    Проверяет уникальность нового email.
    """
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)

        if form.is_valid():

            try:
                new_email = form.cleaned_data['new_email']
                request.user.email = new_email
                request.user.save()
                messages.success(
                    request, 'Email успешно изменен.'
                )
                logger.info(
                    'Email успешно изменен. '
                    f'Request: {request.POST.dict()}.'
                )
                return redirect('profile')
            except Exception as e:
                messages.error(
                    request, f'Ошибка при изменении email: {e}'
                )
                logger.error(
                    f'Ошибка при изменении email: {e}. '
                    f'Request: {request.POST.dict()}'
                )

        else:
            messages.error(
                request, 'В форме есть ошибки, проверьте введенные данные.'
            )
            logger.error(
                'В форме есть ошибки, проверьте введенные данные. '
                f'Request: {request.POST.dict()}'
            )

    else:
        form = EmailChangeForm()

    return render(
        request,
        'users/change_email.html',
        {'form': form}
    )
