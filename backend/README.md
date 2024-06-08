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
Right now, this is just a simple query to the AI. This will have to be changed to include our RAG set up.

## Models
If we choose to have user authentication and store user data in the database, we will have to create a model to store that information. Django includes model classes that will create and update tables in our Postgres database. Right now I have test model that isn't being used, but should have a table in the database.

## Serializers
For every model, there must be a serializer. This takes care of transforming Django's model data into something that can be sent with the API that we are creating. See DjangoRESTframework's documentation for more information.

## URLs
This file (not to be confused with the `urls.py` file in the /backend folder) contains all the endpoint urls.

For example:
```python
path('test-get/', views.test_get, name='test_get'),
```

The HTTP request must be sent to /api/test-get/ (NOTE: YOU MUST INCLUDE THE FINAL '/'), which will activated the second argument, `views.test_get`. This runs the function called `test_get` that is in our `views.py` file. See below. 

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