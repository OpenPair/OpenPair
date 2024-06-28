# Django Rest Framework Backend

## Setup
1. Make sure your virtual environment is activated.
2. Run `python -m pip install -r requirements.txt` to ensure all Python dependencies are downloaded.
3. Set up .env file in root directory. This should look like this:
```
OPENAI_API_KEY=<YOUR-API-KEY>
ORGANIZATION=<YOUR-ORGANIZATION-CODE>
PROJECT=<YOUR-PROJECT-CODE>
DATABASE_NAME=<NAME-OF-YOUR-DATABASE>
DATABASE_USER=<YOUR-DB-USERNAME>
VECTOR_STORE_ID=<AN-ID-FOR-AN-EXISTING-OPENAI-VECTOR-STORE>
```
4. Run `python manage.py migrate`. In Postico, you should see your database populated with Django's tables. If you encounter an error, ensure that you can run `psql --version` in the terminal. If you can't, you need to set up the terminal path for Postgres.
5. _I have changed the terminal commands to run the client and server_
```
npm run server # this now runs the Django server.
npm run client # this runs the Vite React frontend.
```

## Lay of the Land
```
└── 📁 backend
    └── README.md <-- YOU ARE HERE 
    └── 📁 api
        └── __init__.py
        └── admin.py
        └── ai_client.py            <--- SEE AI CLIENT BELOW
        └── apps.py
        └── 📁 middleware
            └── middleware_logger.py
        └── 📁 migrations
            └── 0001_initial.py
            └── __init__.py
        └── models.py               <--- SEE MODELS BELOW
        └── serializers.py          <--- SEE SERIALIZERS BELOW
        └── tests.py
        └── urls.py                 <--- SEE URLS BELOW
        └── views.py                <--- SEE VIEWS BELOW
    └── 📁 backend
        └── __init__.py
        └── asgi.py
        └── settings.py             <--- SEE SETTINGS BELOW
        └── urls.py
        └── wsgi.py
    └── manage.py
```


Most of the files in these folders you can ignore, but I have marked the most important ones. Below are their descriptions. 

*Note: that there is a `urls.py` file in both the /backend folder and the /api folder. `backend/urls.py` is the root URLs folder, which includes the URLs from the `api/urls.py` file. You should only add URLs to the `api/urls.py` file.*


## AI Client
I've set up a very basic RAG AI in `ai_client.py`, which will eventually be replaced by a more robust vector storage system. Right now, there is a function to create an assistant and a thread. The assistant is created to have an existing vector store attached.

To set up your vector store: 

*Prequisites: you must have an OpenAi account with all the keys in your `.env`.*

1. Open a terminal in the root directory. Ensure virtual environment is active.
2. Run `python backend/manage.py shell`. This opens a space in the terminal that you can run code.
3. Run 
```python
>>> doc_list = ['path-for-a-doc', 'path-for-another-doc',]
```
4. Run
```python
>>> from api.ai_client import create_vector_store
```
This imports the helper function from `ai_client.py` into this workspace in the terminal.
5. Run 
```python
>>> vector_store = create_vector_store(doc_list)
```
6. Run 
```python
>>> vector_store.id
```
Should return the `id` of the vector store that you just created. Copy this and paste it into your `.env` file. 
7. Run `quit()`. This will exit the terminal workspace. 

This vector store can be seen in you OpenAI dashboard on their website if you need to access the `id` again, at more files to the vector store, etc. 

## Models
If we choose to have user authentication and store user data in the database, we will have to create a model to store that information. Django includes model classes that will create and update tables in our Postgres database. 

There is a model there for a Vocab word. The class defines 'word' and 'definition' as columns in the database. Django automatically includes a primary key as a column. 

If you make changes to the Vocab model, or add other model classes for other Postgres tables, you have to make and run migragations. 

From your root directory, virtual env active:

```
python backend/manage.py makemigrations
python backend/manage.py migrate
```

## Serializers
**For every model, there must be a serializer**. This takes care of transforming Django's model data into something that can be sent with the API that we are creating. See DjangoRESTframework's documentation for more information.

Right now, I have four serializers. The serializers are necessary for converting the complex object classes of OpenAi response objects and database objects into something that is easily parsed into JSON to be sent as an HTTP response. 

Each variable declared in the serializer classes is an expected key from the data that it is supposed to be serializing. For example, in the `TextSerializer`, there is a variable called `value` and a variable called `annotations`. That means that whatever object it is going to serialize should have a key of value and annotations. 

These serializers are used in the `views.py` file. See below.

## URLs
This file (not to be confused with the `urls.py` file in the /backend folder) contains all the endpoint urls.

For example:
```python
path('test-get/', views.test_get, name='test_get'),
```

The HTTP request must be sent to /api/test-get/ **(NOTE: YOU MUST INCLUDE THE FINAL '/')**, which will activated the second argument, `views.test_get`. This runs the function called `test_get` that is in our `views.py` file. See below. 

## Views
Views are the functions that get called when an HTTP request is made. Here's an example: 

```python
@api_view(['POST']) # Decorator indicating the expected HTTP method(s).
def add_to(request):
    print('This is a test', request.data) # request.data accesses the body of data sent by frontend
    return Response(status=status.HTTP_201_CREATED) # Response with at status of 201 Created
```




## Settings
Settings for backend server at root level. Things will need to be changed here for deployment. Notable sections include Database settings, middleware, and apps. 