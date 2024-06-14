from django.urls import path
from . import views

urlpatterns = [
    path('query-client/', views.query_openai, name='query_client'),
    path('regen/', views.regenerate_response, name='regenerate_response'),
    path('definition/<str:word>/', views.definition, name='definition')
]