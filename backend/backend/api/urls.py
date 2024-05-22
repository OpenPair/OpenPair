from django.urls import path
from . import views

urlpatterns = [
    path('session/', views.add_to_sess, name='add_to_sess'),  #POST
    path('test-get/', views.test_get, name='test_get'),  #GET
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf-token'), #To get the token
]