# NEEDS (user_file, assistant, assistant_instructions, client) as parameters in order to function!!!

# function upload_user_file() adds the user file to the assistant's vector store 
# and creates a thread with the user file attached to the message. 
# The function then prints the tool resources of the thread. The function then creates an instance 
# of the OpenAI class and defines an EventHandler class that extends the AssistantEventHandler class.
# This allows for citation of the uploaded file in the assistant's response.


# Import statements
from openai import OpenAI, AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override

# Function to create a thread using user file
def upload_user_file(user_file, assistant, assistant_instructions, client):
    """
    Upload a user file to the assistant's vector store and create a thread with the file attached.

    :param user_file: Path to the user file (string)
    :param assistant: Assistant object (openai.Assistant)
    :param assistant_instructions: Instructions for the assistant (string)
    :param client: OpenAI client object (openai.OpenAI)
    :return: None
    """
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

   # Creating an event handler to handle the assistant's response
    class EventHandler(AssistantEventHandler):
        @override
        def on_text_created(self, text) -> None:
            """
            Print the assistant's response to the console.

            :param text: The assistant's response (string)
            :return: None
            """
            print(f"\nassistant > ", end = "", flush = True)

        @override
        def on_tool_call_created(self, tool_call):
            """
            Print the tool call type to the console.

            :param tool_call: The tool call object (openai.ToolCall)
            :return: None
            """
            print(f"\nassistant > {tool_call.type}\n", flush=True)

        @override
        def on_message_done(self, message) -> None:
            """
            Print the assistant's response to the console.
            
            :param message: The assistant's message (openai.Message)
            :return: None
            """
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