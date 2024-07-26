from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.profile, name= "profile"),
    path('register-user/', views.registerUser, name="register-user"),
    path('login-user/', views.loginUser, name="login-user"),
    path('logout-user/', views.logoutUser, name="logout-user"),
    path('edit-account/', views.editAccount, name="edit-account"),
    path('delete-account/', views.deleteAccount, name="delete-account"),
]