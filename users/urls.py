from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profiles, name= "profiles"),
    path('register-user/', views.registerUser, name="register-user"),
]