from django.urls import path
from . import views

urlpatterns = [  # Each path corrisponds to a function in the views.py file.
    path('query-client/', views.query_openai, name='query_client'),
    # path('definition/<str:word>/', views.definition, name='definition'),
]