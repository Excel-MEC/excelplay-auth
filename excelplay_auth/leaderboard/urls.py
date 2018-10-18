from django.urls import path

from .views import get_all_rank, kryptos_ranklist, test_ldb

urlpatterns = [
        path('rank', get_all_rank, name='get_all_rank'),
        path('kranklist', kryptos_ranklist, name='kryptos_ranklist'),
        path('test', test_ldb, name='test_ldb')
]
