from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from dotenv import load_dotenv
from os import getenv
import pprint

load_dotenv()

api_key = getenv('OPENAI_API_KEY')
organization = getenv('ORGANIZATION')
project = getenv('PROJECT')

client = OpenAI(
  api_key = api_key,
  organization = organization,
  project = project,
)

def create_asst_thrd():
  assistant = client.beta.assistants.create(
      name = 'Tech Documentation Simplifier',
      instructions= 'You are tutor that simplifies coding documentation for beginning software developers',
      model='gpt-3.5-turbo',
      tools=[{'type': 'file_search'}],
  )

  thread = client.beta.threads.create()

  return {"assistant": assistant, "thread": thread}

def run(thread_id, assistant_id, user_message):
  message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role='user',
    content=user_message
  )

  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions='The user is a beginning developer.'
  )

  if run.status == 'completed': 
    messages = client.beta.threads.messages.list(
    thread_id=thread_id
    )
    pprint.pformat(messages)
  else:
    print(run.status)

  return messages



# ! TESTING
assistant = create_asst_thrd()
# print(assistant["thread"].id)

run(
  thread_id=assistant["thread"].id, 
  assistant_id=assistant["assistant"].id, 
  user_message='Say hello!',
  )

run(  
  thread_id=assistant["thread"].id, 
  assistant_id=assistant["assistant"].id, 
  user_message='Did I already ask you to say hello?',
  )


# ! This is for Chat Completion API
# chat_completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": "Hello world"}]
# )

# print(chat_completion.choices[0].message)


# ? When a user pings the server for the first time, if they don't have a thread id, it should be added to the session. 
#  If there is a thread_id already, we add it to the session to be referenced later.
#  The server will send back all the messages that pertain to that thread.