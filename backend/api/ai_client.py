from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from dotenv import load_dotenv
from os import getenv

load_dotenv()


# ! Sets up the AI Client with the correct keys.
api_key = getenv('OPENAI_API_KEY')
organization = getenv('ORGANIZATION')
project = getenv('PROJECT')
vector_store_id = getenv('VECTOR_STORE_ID')


# ! Setup OpenAI with api key, etc.
client = OpenAI(
  api_key = api_key,
  organization = organization,
  project = project,
)

def create_asst_thrd(instructions = 'You are tutor that simplifies coding documentation for beginning software developers'):
  """
  Creates the AI assistant with its applicable settings, 
  as well as the thread. Returns the created assistant and thread, 
  both with id properties.
  Args: instructions -- str, instructions for the assistant. Defaults to coding tutor.
  """
  # Creates a new Assistant
  assistant = client.beta.assistants.create(
      name='Tech Documentation Simplifier',
      instructions=instructions,
      model='gpt-3.5-turbo',
      tools=[{'type': 'file_search'}],
      tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
  )

  #  Creates a new Thread (series of messages)
  thread = client.beta.threads.create()

  return {"assistant": assistant, "thread": thread}


def run(thread_id, assistant_id, user_message):
  """
  Takes the current thread_id, assistant_id, and whatever message user has typed,
  appends it to the conversation, and returns the whole conversation.
  """

  # Creates the message that gets appended to the conversation.
  print('In the client run function')
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
  print("The Ai response is generated.")
  return messages

def rerun(thread_id, assistant_id, message_id, regen_message):
  """
  ! Not being used. 
  Regenerates a response from OpenAI, and returns whole conversation.
  """

  #  Deletes old AI message
  deleted = client.beta.threads.messages.delete(
      thread_id=thread_id,
      message_id=message_id,
    )

  # Creates a new user message instructing to rephrase.
  prompt = f"Please rephrase this response using simpler language and analogies: {regen_message}"
  message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role='user',
    content=prompt,
  )

  # Runs model with new user message
  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions='You are to simplify coding and development topics so it is understandable to beginners.'
  )

  if run.status == 'completed': 
    #  Deletes the user message from the thread
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
  """
  A function that simply returns all the messages in a given thread.
  """
  messages = client.beta.threads.messages.list(
    thread_id=thread_id
  )
  return messages

def create_vector_store(tech_docs):
  """
  Creates a vector store.
  Args: tech_docs -- a list of file paths.
  Returns a vector store object (not the actual vector store).
  """

  #  Creates the empty store
  vector_store = client.beta.vector_stores.create(
    name = 'tech_docs'
  )

  # Opening files
  file_streams = [open(path, 'rb') for path in tech_docs]

  # Uploading files to store.
  file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=file_streams
  )

  print(file_batch.status)
  print(file_batch.file_counts)
  print(f"All files uploaded: {file_batch.file_counts} == {len(tech_docs)}")

  return vector_store

def update_asst(assistant_id, vector_store_id):
  """
  A function to add a vector store to an assistant. 
  Returns assistant object.
  """
  #  Adds the vector store as a tool resource to an assistant.
  assistant = client.beta.assistants.update(
  assistant_id=assistant_id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
)
  return assistant


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