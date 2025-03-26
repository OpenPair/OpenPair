from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import ai_client
from .models import Vocab
from .serializers import VocabSerializer
from api.serializers import MessageSerializer

"""
Route: 'api/query-client/'
Expects: An object like: 
{
    "message": "Here is what the user was asking the AI assistant."
}
Response: 200, with list of entire conversation.
"""
@api_view(['GET', 'POST'])
def query_openai(request):
    print(f"request.data: {request.data}")
    
    try:
        # We no longer need thread_id and assistant_id, but keeping them as None
        # to maintain the function signature
        messages = ai_client.run(
            thread_id=None,
            assistant_id=None,
            user_message=request.data['message']
        )
        
        for message in messages:
            message['vocab'] = extract_vocab(message['content'][0]['text']['value'])
            
        serialized_messages = MessageSerializer(messages, many=True)
        return Response(serialized_messages.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error: {e}")
        return Response(
            {"error": "An error occurred processing your request"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# You can remove these endpoints since we're not using them anymore:
# - regenerate_response
# - get_all_messages 
@api_view(["GET"])
def get_all_messages(request):
    if 'thread_id' not in request.session:
        return Response(status=status.HTTP_200_OK)
    messages = ai_client.get_conversation(thread_id=request.session['thread_id'])
    serialized_messages = MessageSerializer(messages, many=True)
    return Response(serialized_messages.data, status=status.HTTP_200_OK)

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
    for message in messages:
        message.vocab = extract_vocab(message.content[0].text.value)
    serialized_messages = MessageSerializer(messages, many=True)
    return Response(serialized_messages.data, status=status.HTTP_200_OK)

"""
Route: 'api/definition/:word/' expects a string that is the word being looked up. Case-insensitive
Response: 200 {
    "id": 5,
    "word": "Class",
    "definition": "In object-oriented programming, a blueprint for creating objects, providing initial values for state and implementations of behavior."
}
404 if the word isn't found with an object like this: 
{
    "detail": "No Vocab matches the given query."
}
"""
@api_view(["GET"])
def definition(request, word):
    word = get_object_or_404(Vocab, word__iexact=word) # Queries the DB for word that matches the work in the URL
    print(f"Word: {word}")
    serialized_word = VocabSerializer(word)
    print(f"Serialized: {serialized_word.data}")
    return Response(serialized_word.data, status=status.HTTP_200_OK)


# I need a function that will look through each of the AI's responses, and identify the words that match vocab words.
# 1. Get all the vocab words
# 2. For each word, check if responses contain any vocab word.
# 3. Append the word and definition to a dictionary.
# 4. Dictionary is attached to message object.
# 5. Message object is serialized and sent over.

def extract_vocab(res):
    word_list = Vocab.objects.all()
    # words_in_res = {}
    # for word in word_list:
    #     if not res.lower().find(f" {word.word.lower()}") == -1:
    #         print(f"Word: {word.word}\nDefinition: {word.definition}")
    #         words_in_res[word.word] = word.definition
    # return words_in_res
    words_in_res = []
    for word in word_list:
        if not res.lower().find(f" {word.word.lower()}") == -1:
            words_in_res.append(word)
    return words_in_res
 
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