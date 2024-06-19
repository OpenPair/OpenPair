# Import statements
from openai import OpenAI, AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override
import os
import boto3
import numpy as np

# Load .env file for keys
load_dotenv()

# Create a session with S3 bucket
S3_API_KEY = os.getenv("S3_API_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
session = boto3.Session( aws_access_key_id=S3_API_KEY, aws_secret_access_key=S3_SECRET_KEY)
s3 = session.resource('s3')
my_bucket = s3.Bucket('openpair')

# Create a list of files in the bucket
bucket_objects = []
for bucket_object in my_bucket.objects.all():
    bucket_objects.append(bucket_object.key)

# Create variables for OpenAI access
OpenAI_api_key = os.getenv('OPENAI_API_KEY')
organization = 'OpenPair'
project = 'OpenPair'

# Create assistant variables
assistant_name = "OpenPair"
assistant_instructions = "You help programmers understand tech documents at their level"
assistant_model = "gpt-4-turbo"
assistant_tools = [{"type": "file_search"}]

# Create vector store variables
store_name = "tech_docs"

# Put file names here in tech docs list
tech_docs = []

# Create client connection from OpenAI variables
client = OpenAI(
  api_key = OpenAI_api_key,
  organization= organization,
  project = project,
)

# Create assistant
assistant = client.beta.assistants.create(
  name = assistant_name,
  instructions = assistant_instructions,
  model = assistant_model,
  tools = assistant_tools,
)

# Create vector store
vector_store = client.beta.vector_stores.create(name = store_name)

# Open the files in read binary mode
file_paths = tech_docs
file_streams = [open(path, "rb") for path in file_paths]

# Upload the files to the vector store
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id = vector_store.id, files=file_streams
)

# Confirm upload
print(file_batch.status)
print(file_batch.file_counts)
print(f"All files uploaded: ${str(file_batch.file_counts) == str(tech_docs.length)}")

# Update the assistant with the vector store
assistant = client.beta.assistants.update(
  assistant_id = assistant.id,
  tool_resources = {"file_search": {"vector_store_ids": [vector_store.id]}},
)

# Function to create a thread using user file
def upload_user_file(user_file):
  message_file = client.files.create(
    file = open(user_file, "rb"), purpose = "assistants"
  )

  # Create a thread and attach the file to the message
  thread = client.beta.threads.create(
    messages = [
      {
        "role": "user",
        "content": "How many shares of AAPL were outstanding at the end of of October 2023?",
        # Attach the new file to the message.
        "attachments": [
          { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
      }
    ]
  )

  # The thread now has a vector store with that file in its tool resources.
  print(thread.tool_resources.file_search)

  client = OpenAI()

  class EventHandler(AssistantEventHandler):
      @override
      def on_text_created(self, text) -> None:
          print(f"\nassistant > ", end = "", flush = True)

      @override
      def on_tool_call_created(self, tool_call):
          print(f"\nassistant > {tool_call.type}\n", flush=True)

      @override
      def on_message_done(self, message) -> None:
          # print a citation to the file searched
          message_content = message.content[0].text
          annotations = message_content.annotations
          citations = []
          for index, annotation in enumerate(annotations):
              message_content.value = message_content.value.replace(
                  annotation.text, f"[{index}]"
              )
              if file_citation := getattr(annotation, "file_citation", None):
                  cited_file = client.files.retrieve(file_citation.file_id)
                  citations.append(f"[{index}] {cited_file.filename}")

          print(message_content.value)
          print("\n".join(citations))


  # Then, we use the stream SDK helper
  # with the EventHandler class to create the Run
  # and stream the response.

  with client.beta.threads.runs.stream(
      thread_id = thread.id,
      assistant_id = assistant.id,
      instructions = assistant_instructions,
      event_handler = EventHandler(),
  ) as stream:
      stream.until_done()