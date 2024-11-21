from django.urls import path
from .views import search_id

urlpatterns = [
    path('search', search_id, name='search-id'),
]