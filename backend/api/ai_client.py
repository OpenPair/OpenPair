from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from os import getenv
import time
import uuid

load_dotenv()

model = ChatOpenAI(
  api_key=getenv('OPENAI_API_KEY'),
  model="gpt-3.5-turbo"  
)

SYSTEM_PROMPT = "you are a tutor that simplifies coding documentation for beginning software developers"
MAX_MESSAGES = 10  # Keep last 10 messages for context

# Store messages for each session
session_raw_messages = {}

def get_or_create_session(thread_id):
    """Initialize or get a session's message history"""
    if thread_id not in session_raw_messages:
        session_raw_messages[thread_id] = [SystemMessage(content=SYSTEM_PROMPT)]
    return session_raw_messages[thread_id]

def get_or_create_chat_session(request):
    """Ensure we have a session key"""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def run(thread_id, user_message, request):
    try:
        # Get session messages
        messages = get_or_create_session(thread_id)
        
        # Add user message to context
        user_msg = HumanMessage(content=user_message)
        messages.append(user_msg)
        
        # Keep only the system message and last MAX_MESSAGES messages
        if len(messages) > MAX_MESSAGES + 1:  # +1 for system message
            messages = [messages[0]] + messages[-(MAX_MESSAGES):]
        
        # Update session messages
        session_raw_messages[thread_id] = messages
        
        # Get AI response
        response = model.invoke(messages)
        
        # Add AI response to context
        messages.append(response)
        
        # Format response for frontend
        current_time = int(time.time())
        return [{
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": response.content,  # Send plain text content
            "timestamp": current_time
        }]
        
    except Exception as e:
        print(f"Error in Langchain processing: {e}")
        raise
