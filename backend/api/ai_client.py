from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_key = getenv('OPENAI_API_KEY')
organization = getenv('ORGANIZATION')
project = getenv('PROJECT')

client = OpenAI(
  api_key = api_key,
  organization = organization,
  project = project,
)

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello world"}]
)

print(chat_completion.choices[0].message)