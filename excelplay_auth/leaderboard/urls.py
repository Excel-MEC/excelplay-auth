from django.urls import path

from .views import get_all_rank, kryptos_ranklist, dalalbull_ranklist

urlpatterns = [
        path('rank', get_all_rank, name='get_all_rank'),
        path('kranklist', kryptos_ranklist, name='kryptos_ranklist'),
        path('dbranklist', dalalbull_ranklist, name='dalalbull_ranklist')
]
