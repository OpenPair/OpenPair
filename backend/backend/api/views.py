from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token

# Create your views here.
# ? Test POST
@api_view(['POST'])
def add_to_sess(request):
    print('You are adding to the session, supposedly.', request.body)
    return Response(status=status.HTTP_201_CREATED)

# ? TEST GET
def test_get(request):
    print('You are GETTING')
    return HttpResponse('You have gotten some text.')

# ? TEST GET
def get_csrf_token(request):
    token = get_token(request)
    response = JsonResponse({'csrfToken': token})
    print('Getting the valuable token', token)
    # response['X-CSRFToken'] = get_token(request)
    response.set_cookie('csrftoken', token)
    return response

# GET the current count
@api_view(['POST', 'GET'])
def count(request):
    if request.session:
        print(request.session)
    if request.method == 'GET':
        return Response('You are GETting from count/')
    if request.method == 'POST':
        print(request.data)
        request.session['MyCount'] = request.data
        print(request.session['MyCount'])
        return Response(status=status.HTTP_201_CREATED)
