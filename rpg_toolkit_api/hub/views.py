import json

# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, \
                                      authentication_classes


# Create your views here.

@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        user_info = json.loads(request.body)
        if not user_info['username'] or not user_info['password']:
            return HttpResponse('Missing input(s)', status=400)
        user = User.objects.create_user(user_info['username'],
                                        user_info['email'],
                                        user_info['password'])
        user.save()

        return HttpResponse('', status=201)


@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def logout(request):
    Token.objects.get(user=request.user).delete()
    return HttpResponse('', status=200)