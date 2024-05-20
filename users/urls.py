from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profiles, name= "profiles"),
    path('register-user/', views.registerUser, name="register-user"),
    path('login-user/', views.loginUser, name="login-user"),
    path('logout-user/', views.logoutUser, name="logout-user"),
    path('edit-account/', views.editAccount, name="edit-account"),
]