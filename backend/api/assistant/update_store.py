import boto3
import pickle
import numpy as np
import openai
from sklearn.neighbors import NearestNeighbors

def list_files(bucket_name, prefix='', max_keys=1000):
    """
    List files in an S3 bucket with pagination.
    
    :param bucket_name: Name of the S3 bucket (string)
    :param prefix: Optional prefix to filter objects (string)
    :param max_keys: Maximum number of keys to retrieve per request (int default=1000)
    :return: Generator that yields lists of keys (file names) in the bucket (list of strings)
    """
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix, PaginationConfig={'PageSize': max_keys})
    
    for page in pages:
        keys = [content['Key'] for content in page.get('Contents', [])]
        yield keys

def retrieve_vector(bucket_name, key):
    """
    Retrieve a vector from an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket (string)
    :param key: The key under which the vector is stored (string)
    :return: The retrieved vector (numpy array)
    """
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=key)
    serialized_vector = response['Body'].read()
    vector = pickle.loads(serialized_vector)
    return vector

def process_vectors_in_batches(bucket_name, prefix='', batch_size=100):
    """
    Process vectors in batches from an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket (string)
    :param prefix: Optional prefix to filter objects (string)
    :param batch_size: Number of vectors to process per batch (int)
    """
    vector_generator = list_files(bucket_name, prefix, max_keys=batch_size)
    
    for keys in vector_generator:
        vectors = []
        for key in keys:
            vector = retrieve_vector(bucket_name, key)
            vectors.append(vector)
        yield vectors

def update_vector_store(existing_vector_store, new_vectors):
    """
    Update the existing vector store with new vectors.
    
    :param existing_vector_store: Existing vector store (numpy array)
    :param new_vectors: List of new vectors to add (list of numpy arrays)
    :return: Updated vector store (numpy array)
    """
    if len(existing_vector_store) == 0:
        updated_vector_store = np.array(new_vectors)
    else:
        updated_vector_store = np.concatenate((existing_vector_store, new_vectors), axis=0)
    return updated_vector_store

def add_vectors_to_assistant(bucket_name, folder_name, existing_vector_store, nn_model, openai_api_key, batch_size=100):
    """
    Add vectors from an S3 bucket folder to an existing vector store and update the assistant.
    
    :param bucket_name: Name of the S3 bucket (string)
    :param folder_name: Folder name inside the S3 bucket containing the vectors (string)
    :param existing_vector_store: Existing vector store (numpy array)
    :param nn_model: Existing Nearest Neighbors model (sklearn.neighbors.NearestNeighbors)
    :param openai_api_key: OpenAI API key (string)
    :param batch_size: Number of vectors to process per batch (int default=100)
    :return: Updated vector store and a function to generate responses based on user input (tuple)
    """
    # Process and add vectors in batches
    for vectors in process_vectors_in_batches(bucket_name, folder_name, batch_size):
        existing_vector_store = update_vector_store(existing_vector_store, vectors)
    
    # Refit the Nearest Neighbors model with the updated vector store
    nn_model.fit(existing_vector_store)
    
    # Set OpenAI API key
    openai.api_key = openai_api_key

    def get_openai_response(prompt):
        """
        Get a response from the OpenAI API given a prompt.
        
        :param prompt: The prompt to generate a response (string)
        :return: The generated response (string)
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def get_similar_vectors(query_vector, vector_store, nn_model, top_n=5):
        """
        Get the top N most similar vectors to a query vector from a vector store.
        
        :param query_vector: The query vector (numpy array)
        :param vector_store: The vector store to search (numpy array)
        :param nn_model: Nearest Neighbors model (sklearn.neighbors.NearestNeighbors)
        :param top_n: Number of most similar vectors to return (int default=5)
        :return: Tuple of similar vectors and their distances (tuple of numpy arrays)
        """
        distances, indices = nn_model.kneighbors([query_vector], n_neighbors=top_n)
        similar_vectors = vector_store[indices[0]]
        return similar_vectors, distances[0]

    def generate_assistant_response(user_input_vector):
        """
        Generate a response from the assistant based on the user's input vector.
        
        :param user_input_vector: The user's input vector (numpy array)
        :return: The assistant's response (string)
        """
        similar_vectors, distances = get_similar_vectors(user_input_vector, existing_vector_store, nn_model)
        
        prompt = "The user asked about something similar to these topics: "
        for vec in similar_vectors:
            prompt += f"\n- {vec}"
        
        prompt += "\nBased on the above topics, respond to the user's query in a helpful manner."
        
        response = get_openai_response(prompt)
        return response
    
    # Return the updated vector store and a function to generate responses
    return existing_vector_store, generate_assistant_response

# Example usage
bucket_name = 'your-s3-bucket-name'
folder_name = 'your-folder-name'
openai_api_key = 'your-openai-api-key'
existing_vector_store = np.random.rand(10, 300)  # Example existing vector store (replace with actual data)
nn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
nn_model.fit(existing_vector_store)

# Update the vector store and get the response generator function
updated_vector_store, generate_response = add_vectors_to_assistant(bucket_name, folder_name, existing_vector_store, nn_model, openai_api_key)

# Example user input vector (replace with actual user input processing)
user_input_vector = np.random.rand(300)

# Generate the assistant's response
response = generate_response(user_input_vector)
print(response)