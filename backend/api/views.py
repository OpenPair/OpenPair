from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import ai_client
from api.serializers import MessageSerializer
import uuid
import time

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
        
        # Create user message for response
        current_time = int(time.time())
        print(f"\n=== Timestamp Debug ===")
        print(f"Current Unix timestamp: {current_time}")
        print(f"As readable date: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}")
        
        user_message = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": request.data['message'],
            "timestamp": current_time  # Single source of truth for timing
        }
        print(f"User message with timestamp: {user_message}")
            
        # Get AI response
        ai_response = ai_client.run(
            thread_id=thread_id,
            user_message=request.data['message'],
            request=request
        )
        
        # Return just the new messages
        new_messages = [user_message] + ai_response
        print("\n=== Message Debug ===")
        print("Messages before serialization:", new_messages)
        print("Timestamps in messages:", [(msg["role"], msg["timestamp"], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg["timestamp"]))) for msg in new_messages])
        serialized_messages = MessageSerializer(new_messages, many=True)
        print("Serialized messages:", serialized_messages.data)
        return Response(serialized_messages.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error: {e}")
        return Response(
            {"error": "An error occurred processing your request"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
