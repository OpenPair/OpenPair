import asyncio
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from . import ai_client

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

"""
Route: 'api/query-client/'
Expects: An object like: 
{
    "message": "Here is what the user was asking the AI assistant."
}
Response: 200, with list of entire conversation.

! NOTE: sessions expire when browser closes.
"""
@api_view(['GET'])
def query_openai(request):
    if ('thread_id' not in request.session):  # If the thread_id does not exist in a current session:
        created_assistant = ai_client.create_asst_thrd()  # creates a new assistant and thread
        request.session['thread_id'] = created_assistant["thread"].id  # Creates new session key for thread_id and assistant_id
        request.session['assistant_id'] = created_assistant['assistant'].id
        thread_id = request.session['thread_id']
        assistant_id = request.session['assistant_id']
        messages = ai_client.run(  # Creates a run with the first message.
            thread_id=thread_id, 
            assistant_id=assistant_id,
            user_message=request.data['message']
        )
        ex_messages = ai_client.extract_messages(messages)
        return Response(ex_messages, status=status.HTTP_200_OK)
    else:
        print(f"This is the thread_id: {request.session['thread_id']} \nThis is the message: {request.data['message']}")
        thread_id = request.session['thread_id']
        assistant_id = request.session['assistant_id']
        messages = ai_client.run(
            thread_id=thread_id, 
            assistant_id=assistant_id,
            user_message=request.data['message']
            )
        ex_messages = ai_client.extract_messages(messages)
        return Response(ex_messages, status=status.HTTP_200_OK)
