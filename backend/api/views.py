from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import ai_client
# from .models import Vocab
# from .serializers import VocabSerializer
from api.serializers import MessageSerializer

"""
Route: 'api/query-client/'
Expects: An object like: 
{
    "message": "Here is what the user was asking the AI assistant."
}
Response: 200, with list of entire conversation.
"""
@api_view(['POST'])
def query_openai(request):
    print(f"request.data: {request.data}")
    
    try:
        # Make sure we have a session
        thread_id = ai_client.get_or_create_chat_session(request)
            
        messages = ai_client.run(
            thread_id=thread_id,  # Use session key for memory
            user_message=request.data['message'],
            request=request
        )
        
        # Get full chat history
        chat_history = request.session.get("chat_history", [])
        
        # Add vocab to all messages
        # for message in chat_history:
        #     if 'vocab' not in message:  # Only process if vocab hasn't been added yet
        #         message['vocab'] = extract_vocab(message['content'][0]['text']['value'])
            
        serialized_messages = MessageSerializer(chat_history, many=True)
        return Response(serialized_messages.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error: {e}")
        return Response(
            {"error": "An error occurred processing your request"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

"""
Route: 'api/chat-history/'
Response: 200, with list of all messages in the current session.
"""
@api_view(['GET'])
def get_chat_history(request):
    """Get the chat history for the current session"""
    if not request.session.session_key:
        return Response([], status=status.HTTP_200_OK)
        
    chat_history = ai_client.get_chat_history(request.session.session_key)
    
    # Add vocab to all messages
    # for message in chat_history:
    #     if 'vocab' not in message:
    #         message['vocab'] = extract_vocab(message['content'][0]['text']['value'])
            
    serialized_messages = MessageSerializer(chat_history, many=True)
    return Response(serialized_messages.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def clear_chat(request):
    """Clear the chat history for the current session"""
    if not request.session.session_key:
        request.session.create()
    
    ai_client.clear_chat_history(request.session.session_key)
    return Response(status=status.HTTP_200_OK)

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
# @api_view(["GET"])
# def definition(request, word):
#     word = get_object_or_404(Vocab, word__iexact=word)
#     print(f"Word: {word}")
#     serialized_word = VocabSerializer(word)
#     print(f"Serialized: {serialized_word.data}")
#     return Response(serialized_word.data, status=status.HTTP_200_OK)

# def extract_vocab(res):
#     word_list = Vocab.objects.all()
#     words_in_res = []
#     for word in word_list:
#         if not res.lower().find(f" {word.word.lower()}") == -1:
#             words_in_res.append(word)
#     return words_in_res