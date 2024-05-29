from django.urls import path
from . import views

urlpatterns = [
    path('terms_of_service/', views.tos_view, name='terms_of_service'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('about_us/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]