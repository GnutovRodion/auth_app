from django.urls import path

from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-email/', views.change_email, name='change_email')
]
