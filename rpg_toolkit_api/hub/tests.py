import requests
import json
import re

from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


# Create your tests here.

class TestSmoke(TestCase):
    def test_truth(self):
        assert True

    def test_math(self):
        assert 1+1 == 2


class FunctionalTests_Users(LiveServerTestCase):
    body = {'username': 'my_user',
            'email': 'mail@example.com',
            'password': 'my_password'}

    def test_user_creation(self):
        response = requests.post(self.live_server_url + '/hub/user/',
                                 data=json.dumps(self.body))
        assert response.status_code == 201

    def test_login(self):
        User.objects.create_user(self.body['username'],
                                 self.body['email'],
                                 self.body['password'],)

        response = requests.post(self.live_server_url + '/hub/login/',
                                 data=self.body)

        assert response.status_code == 200
        resp = json.loads(response.text)
        assert 'token' in resp.keys()
        assert re.match(r'^[0-9a-f]*$', resp['token'])
        assert Token.objects.all()

    def test_logout(self):
        user = User.objects.create_user(self.body['username'],
                                        self.body['email'],
                                        self.body['password'],)

        token, created = Token.objects.get_or_create(user=user)

        response = requests.post(self.live_server_url + '/hub/logout/',
                                 headers={'Authorization':
                                          'Token {}'.format(token)})

        assert response.status_code == 200
        assert not Token.objects.all()
