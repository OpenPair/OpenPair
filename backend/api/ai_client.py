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

load_dotenv()

model = ChatOpenAI(
  api_key=getenv('OPENAI_API_KEY'),
  model="gpt-3.5-turbo"  
)

SYSTEM_PROMPT = "you are a tutor that simplifies coding documentation for beginning software developers"

session_workflows = {}
session_messages = {}  # Store messages for each session

def call_model(state: MessagesState):
    """Process the current state and generate a response"""
    # Get all messages from the state
    messages = state["messages"]
    
    # Always include system message first
    all_messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    # Get response from the model
    response = model.invoke(all_messages)
    
    # Update the state with the new message
    state["messages"].append(response)
    
    return state

def format_message_for_storage(message, role):
    """Format a message for storage and API response"""
    return {
        'id': str(hash(str(message))),
        'role': role,
        'content': [{'text': {'value': message.content if hasattr(message, 'content') else str(message)}}],
        'created_at': int(time.time())
    }

def get_or_create_workflow(session_id: str):
    """Get existing workflow or create a new one for the session"""
    if session_id not in session_workflows:
        workflow = StateGraph(state_schema=MessagesState)
        
        # Add nodes
        workflow.add_node("start", lambda x: x)
        workflow.add_node("model", call_model)
        
        # Add edges
        workflow.set_entry_point("start")
        workflow.add_edge('start', 'model')
        workflow.set_finish_point("model")

        # Initialize memory
        memory = MemorySaver()
        session_workflows[session_id] = workflow.compile(checkpointer=memory)
        session_messages[session_id] = []

    return session_workflows[session_id]

def run(thread_id, assistant_id, user_message):
    """Process a user message and return the response"""
    try:
        # Get or create workflow
        workflow = get_or_create_workflow(thread_id)
        
        # Create the user message
        user_msg = HumanMessage(content=user_message)
        
        # Get current state or create new one
        current_messages = session_messages.get(thread_id, [])
        
        # Run the workflow
        result = workflow.invoke({
            "messages": current_messages + [user_msg]
        })
        
        # Get the last message (AI's response)
        ai_response = result["messages"][-1]
        
        # Format messages for storage
        formatted_user_msg = format_message_for_storage(user_msg, 'user')
        formatted_ai_msg = format_message_for_storage(ai_response, 'assistant')
        
        # Update session storage
        if thread_id not in session_messages:
            session_messages[thread_id] = []
        
        session_messages[thread_id].extend([formatted_user_msg, formatted_ai_msg])
        
        # Return just the AI response for immediate display
        return [formatted_ai_msg]

    except Exception as e:
        print(f"Error in Langchain processing: {e}")
        raise

def get_chat_history(thread_id):
    """Get all messages for a given session"""
    return session_messages.get(thread_id, [])

def clear_chat_history(thread_id):
    """Clear the chat history for a given session"""
    if thread_id in session_messages:
        session_messages[thread_id] = []
    if thread_id in session_workflows:
        del session_workflows[thread_id]  # Remove workflow to start fresh

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