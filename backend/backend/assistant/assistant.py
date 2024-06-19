# Creates base assistant with vector store for tech docs. By default, no tech docs are uploaded.

# Variables:
#   'tech_docs' is a list of file paths that will be uploaded to the vector store. Empty by default.
#   'store_name' is the name of the vector store. Set to 'tech_docs'
#   'assistant_name' is the name of the assistant. Set to 'OpenPair'
#   'assistant_instructions' are the instructions for the assistant.
#       Set to 'You help programmers understand tech documents at their level'
#   'assistant_model' is the model used by the assistant. Set to 'gpt-4-turbo'
#   'assistant_tools' are the tools used by the assistant. Set to 'file_search'
#   'organization' is the OpenAI organization name. Set to 'OpenPair'.
#   'project' is the OpenAI project name. Set to 'OpenPair'.
#   's3_bucket_name' is the name of the S3 bucket. Set to 'openpair'.
#   'bucket_objects' is a list of objects in the S3 bucket.
#       Empty by default. But populated by all objects in the defined S3 bucket.
#   'bucket_folders' is a list of folders in the S3 bucket.
#       Empty by default. But populated by all folders in the defined S3 bucket.

# Import statements
from openai import OpenAI, AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override
import os
import boto3
import numpy as np

# Put file names here in tech docs list
tech_docs = []

# Create vector store variables
store_name = "tech_docs"

# Create variables for OpenAI access
organization = 'OpenPair'
project = 'OpenPair'

# Create assistant variables
assistant_name = "OpenPair"
assistant_instructions = "You help programmers understand tech documents at their level"
assistant_model = "gpt-4-turbo"
assistant_tools = [{"type": "file_search"}]

# Define S3 bucket name
s3_bucket_name = "openpair"

# Load .env file for keys
load_dotenv()
S3_API_KEY = os.getenv("S3_API_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
OpenAI_api_key = os.getenv('OPENAI_API_KEY')

# Create a session with S3 bucket
session = boto3.Session(aws_access_key_id=S3_API_KEY, aws_secret_access_key=S3_SECRET_KEY)
s3 = session.resource('s3')
my_bucket = s3.Bucket(s3_bucket_name)

# Create a list of files in the bucket
bucket_objects = []
bucket_folders = []
for bucket_object in my_bucket.objects.all():
    bucket_objects.append(bucket_object.key)
    object_key = str(bucket_object.key)
    folder = object_key.split('/')[0].lower()
    if folder not in bucket_folders:
        bucket_folders.append(folder)

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