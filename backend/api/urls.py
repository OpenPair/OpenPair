from django.urls import path
from . import views

urlpatterns = [  # Each path corresponds to a function in the views.py file.
    path('query-client/', views.query_openai, name='query_client'),
    # path('chat-history/', views.get_chat_history, name='chat_history'),

    # path('definition/<str:word>/', views.definition, name='definition'),
]