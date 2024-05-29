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

# ? Test GET/POST the current count
@api_view(['GET', 'POST'])
def count(request):
    # ! GET
    if request.method == 'GET':
        print('GETTING SESSION:', f'\n\tSession key: {request.session.session_key}', '\n\tUser:', request.user)
        return Response(request.session['MyCount'], status=status.HTTP_200_OK)
    # ! POST
    if request.method == 'POST':
        print('REQUEST.DATA:', request.data, 'user:', request.user)
        print('POSTING SESSION:', request.session)
        request.session['MyCount'] = request.data
        print(request.session['MyCount'], request.session.keys())
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def query_openai(request):
    return Response('You are querying the OpenAi genie', status=status.HTTP_200_OK)
