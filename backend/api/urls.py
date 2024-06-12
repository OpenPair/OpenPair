from django.urls import path
from . import views

urlpatterns = [
    path('query-client/', views.query_openai, name='query_client')
]