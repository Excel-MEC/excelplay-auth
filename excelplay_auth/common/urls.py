from django.urls import path

from .views import sign_in, sign_out, set_token, get_user_detail, get_all_users

urlpatterns = [
        path('signin', sign_in, name='sign_in'),
        path('signout', sign_out, name='sign_out'),
        path('token', set_token, name='set_token'),
        path('user/detail', get_user_detail, name='get_user_detail'),
        path('users', get_all_users, name='get_all_users')
]
