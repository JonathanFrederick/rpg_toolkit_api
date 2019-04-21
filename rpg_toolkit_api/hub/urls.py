from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user/', views.user_create),
    path('login/', obtain_auth_token),
    path('logout/', views.logout),
]
