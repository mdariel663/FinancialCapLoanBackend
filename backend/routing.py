from django.urls import path
from controller.user_controller import create_user, login, get_users, register_user

Router = [
    path('auth/login', login, name='auth_login'),
    path('auth/register', register_user, name='auth_register'),
]