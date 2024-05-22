from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

# Create your views here.
# POST, works with Postman, not with React yet
def add_to_sess(request):
    print('You are adding to the session, supposedly.', request.body)
    return HttpResponse(status=200)

# GET
def test_get(request):
    print('You are GETTING')
    return HttpResponse('You have gotten some text.')

# GET
def get_csrf_token(request):
    token = get_token(request)
    response = JsonResponse({'csrfToken': token})
    print('Getting the valuable token', token)
    # response['X-CSRFToken'] = get_token(request)
    response.set_cookie('csrftoken', token)
    return response
