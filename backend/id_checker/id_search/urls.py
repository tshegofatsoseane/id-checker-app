from django.urls import path
from .views import id_search

urlpatterns = [
    path('search', id_search, name='id-search'),
]