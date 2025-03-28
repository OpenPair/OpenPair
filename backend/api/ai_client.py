from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from dotenv import load_dotenv
from os import getenv
import pprint
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
            "created_at": current_time,
            "timestamp": current_time
        }]
        
    except Exception as e:
        print(f"Error in Langchain processing: {e}")
        raise

# Clean up unused functions and keep only what we need
def format_message_for_storage(message, role):
    """Format a message for storage and API response"""
    current_time = int(time.time())
    return {
        'id': str(uuid.uuid4()),
        'role': role,
        'content': message.content if hasattr(message, 'content') else str(message),
        'created_at': current_time,
        'timestamp': current_time
    }

# def get_chat_history(thread_id):
#     return session_raw_messages.get(thread_id, [])

# def add_to_chat_history(request, role, content):
#     history = request.session.get("chat_history", [])
#     history.append({
#         "id": str(uuid.uuid4()),
#         "role": role,
#         "content": [{"text": {"value": content}}],
#         "created_at": int(time.time())
#     })
#     request.session["chat_history"] = history
#     request.session.modified = True

# def get_or_create_workflow(session_id: str): # Do I need to create new or different workflows?
#     """Get existing workflow or create a new one for the session"""
#     if session_id not in session_workflows:
#         workflow = StateGraph(state_schema=MessagesState)
        
#         # Add nodes
#         workflow.add_node("start", lambda x: x)
#         workflow.add_node("model", call_model)
        
#         # Add edges
#         workflow.set_entry_point("start")
#         workflow.add_edge('start', 'model')
#         workflow.set_finish_point("model")

#         # Initialize memory
#         memory = MemorySaver(
#             thread_id=session_id,
#             checkpoint_id="chat_checkpoint"
#         )
#         session_workflows[session_id] = workflow.compile(checkpointer=memory)
#         session_messages[session_id] = []

#     return session_workflows[session_id]

# def rerun(thread_id, assistant_id, message_id, regen_message):
#   # delete the message from the thread, and have it return a new message that is restated.
#   #// 1 Delete message
#   #// 2 Create a new message asking for a rephrased response
#   #// 3 Create a run with new instructions of the assistant
#   #// 4 Delete the user's message that we crafted
#   #// 5 Return list of messages

#   deleted = client.beta.threads.messages.delete(
#       thread_id=thread_id,
#       message_id=message_id,
#     )

#   prompt = f"Please rephrase this response using simpler language and analogies: {regen_message}"
#   message = client.beta.threads.messages.create(
#     thread_id=thread_id,
#     role='user',
#     content=prompt,
#   )

#   run = client.beta.threads.runs.create_and_poll(
#     thread_id=thread_id,
#     assistant_id=assistant_id,
#     instructions='You are to simplify coding and development topics so it is understandable to beginners.'
#   )

#   if run.status == 'completed': 
#     client.beta.threads.messages.delete(
#       message_id=message.id,
#       thread_id=thread_id,
#     )

#     messages = client.beta.threads.messages.list(
#     thread_id=thread_id
#     )

#     return messages
#   else:
#     print(run.status)

# def get_conversation(thread_id):
#   messages = client.beta.threads.messages.list(
#     thread_id=thread_id
#   )
#   return messages


# ! A function to comprehend the data from AI assistant better. 
# def extract_messages(array):
#   # *Looping method
#   # list_of_messages = []
#   # for message in array:
#   #   message_keys = dict()

#   #   for m_key in message:
#   #     message_keys[m_key[0]] = m_key[1]

#   #   list_of_messages.append(message_keys)
#   # print(list_of_messages)

#   # *Dictionary comprehension method:
#   list_of_messages = []
#   for message in array:
#     message_keys = {item[0]: item[1] for item in message}
#     # print(message_keys)
#     list_of_messages.append(message_keys)
#   # print(list_of_messages)
#   return list_of_messages


# ! TESTING
# assistant = create_asst_thrd()
# # print(assistant["thread"].id)

# run(
#   thread_id=assistant["thread"].id, 
#   assistant_id=assistant["assistant"].id, 
#   user_message='Say hello!',
#   )

# run(  
#   thread_id=assistant["thread"].id, 
#   assistant_id=assistant["assistant"].id, 
#   user_message='Did I already ask you to say hello?',
#   )


# ! This is for Chat Completion API
# chat_completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "Hello world"}]
# )

# print(chat_completion.choices[0].message)


# ? When a user pings the server for the first time, if they don't have a thread id, it should be added to the session. 
#  If there is a thread_id already, we add it to the session to be referenced later.
#  The server will send back all the messages that pertain to that thread.