from django.urls import path
from . import views

urlpatterns = [
    path('session/', views.add_to_sess, name='add_to_sess'),  #POST
    path('test_get/', views.test_get, name='test_get'),  #GET
]