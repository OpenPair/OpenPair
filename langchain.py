import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
langchain_tracing = os.getenv("LANGCHAIN_TRACING_V2")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the environment variables in your code
print(f"LangChain Tracing: {langchain_tracing}")
print(f"LangChain API Key: {langchain_api_key}")
print(f"OpenAI API Key: {openai_api_key}")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's request only based on the given context."),
    ("user", "Question: {question}\nContext: {context}")
])
model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

question = "Can you summarize this morning's meetings?"
context = "During this morning's meeting, we solved all world conflict."
chain.invoke({"question": question, "context": context})