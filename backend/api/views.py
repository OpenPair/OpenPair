import asyncio
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from . import ai_client
from .models import Vocab
from .serializers import VocabSerializer
# from api.serializers import MessageSerializer

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

"""
Route: 'api/regen/'
Expects: An object like: 
{
    "message": "Here is what the user was asking the AI assistant.",
    "message_id": "msg_abc12",
}
Response: 200, with list of entire conversation. 400 if there is no current thread/assistant.
"""   
@api_view(['GET'])
def regenerate_response(request):
    print(f"Old answer: {request.data['message']}\nMessage ID: {request.data['message_id']}")
    if 'assistant_id' not in request.session:
        return Response('This is not allowed.', status=status.HTTP_400_BAD_REQUEST)
    
    messages = ai_client.rerun(
        thread_id=request.session['thread_id'],
        assistant_id=request.session['assistant_id'],
        message_id=request.data['message_id'],
        regen_message=request.data['message']
    )
    ex_messages = ai_client.extract_messages(messages)
    return Response(ex_messages, status=status.HTTP_200_OK)

"""
Route: 'api/definition/:word'
"""
@api_view(["GET"])
def definition(request, word):
    word = get_object_or_404(Vocab, word__iexact=word)
    print(f"Word: {word}")
    serialized_word = VocabSerializer(word)
    print(f"Serialized: {serialized_word.data}")
    return Response(serialized_word.data, status=status.HTTP_200_OK)

    
# Create your views here.
# ? Test POST
# @api_view(['POST'])
# def add_to_sess(request):
#     print('You are adding to the session, supposedly.', request.body)
#     return Response(status=status.HTTP_201_CREATED)

# # ? TEST GET
# def test_get(request):
#     print('You are GETTING')
#     return HttpResponse('You have gotten some text.')

# # ? TEST GET
# def get_csrf_token(request):
#     token = get_token(request)
#     response = JsonResponse({'csrfToken': token})
#     print('Getting the valuable token', token)
#     # response['X-CSRFToken'] = get_token(request)
#     response.set_cookie('csrftoken', token)
#     return response

# # ? Test GET/POST the current count
# @api_view(['GET', 'POST'])
# def count(request):
#     # ! GET
#     if request.method == 'GET':
#         print('GETTING SESSION:', f'\n\tSession key: {request.session.session_key}', '\n\tUser:', request.user)
#         return Response(request.session['MyCount'], status=status.HTTP_200_OK)
#     # ! POST
#     if request.method == 'POST':
#         print('REQUEST.DATA:', request.data, 'user:', request.user)
#         print('POSTING SESSION:', request.session)
#         request.session['MyCount'] = request.data
#         print(request.session['MyCount'], request.session.keys())
#         return Response(status=status.HTTP_201_CREATED)