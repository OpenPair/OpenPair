from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from dotenv import load_dotenv
from os import getenv
import pprint

load_dotenv()


# ! Sets up the AI Client with the correct keys.
api_key = getenv('OPENAI_API_KEY')
organization = getenv('ORGANIZATION')
project = getenv('PROJECT')

client = OpenAI(
  api_key = api_key,
  organization = organization,
  project = project,
)

"""
! Creates the AI assistant with its applicable settings, 
! as well as the thread. Returns the created assistant and thread, 
! both with id properties.
! Args: instructions -- str, instructions for the assistant. Defaults to coding tutor.
"""
def create_asst_thrd(
    instructions = 'You are tutor that simplifies coding documentation for beginning software developers'
    ):
  assistant = client.beta.assistants.create(
      name = 'Tech Documentation Simplifier',
      instructions= instructions,
      model='gpt-3.5-turbo',
      tools=[{'type': 'file_search'}],
  )

  thread = client.beta.threads.create()

  return {"assistant": assistant, "thread": thread}

"""
! Takes the current thread_id, assistant_id, and whatever message user has typed,
! appends it to the conversation, and returns the whole conversation.
"""
def run(thread_id, assistant_id, user_message):
  # Creates the message that gets appended to the conversation.
  message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role='user',
    content=user_message
  )

  # Runs the assistant with the new message
  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
  )

  # Once the run is complete, a list of messages from the current thread is created
  # and returned.
  if run.status == 'completed': 
    messages = client.beta.threads.messages.list(
    thread_id=thread_id
    )
    # pprint.pformat(messages)
  else:
    print(run.status)

  return messages

def rerun(thread_id, assistant_id, message_id, regen_message):
  # delete the message from the thread, and have it return a new message that is restated.
  #// 1 Delete message
  #// 2 Create a new message asking for a rephrased response
  #// 3 Create a run with new instructions of the assistant
  #// 4 Delete the user's message that we crafted
  #// 5 Return list of messages

  deleted = client.beta.threads.messages.delete(
      thread_id=thread_id,
      message_id=message_id,
    )

  prompt = f"Please rephrase this response using simpler language and analogies: {regen_message}"
  message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role='user',
    content=prompt,
  )

  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions='You are to simplify coding and development topics so it is understandable to beginners.'
  )

  if run.status == 'completed': 
    client.beta.threads.messages.delete(
      message_id=message.id,
      thread_id=thread_id,
    )

    messages = client.beta.threads.messages.list(
    thread_id=thread_id
    )

    return messages
  else:
    print(run.status)

def get_conversation(thread_id):
  messages = client.beta.threads.messages.list(
    thread_id=thread_id
  )
  return messages


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