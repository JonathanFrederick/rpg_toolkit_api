import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication


# Create your views here.

@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        user_info = json.loads(request.body)
        user = User.objects.create_user(user_info['username'],
                                        user_info['email'],
                                        user_info['password'])
        user.save()

        return HttpResponse('', status=201)
