from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def add_to_sess(request):
    print('You are adding to the session, supposedly.', request.body)
    return HttpResponse(status=200)