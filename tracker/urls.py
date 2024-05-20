from django.urls import path
from . import views

urlpatterns = [
path('', views.homepage, name="homepage"),
path('update/', views.updatePage, name = "updatePage"),
path('<str:metal_type>/<str:pk>/', views.metalPage, name='metal_page'),
path('edit/<str:metal_type>/<uuid:pk>/', views.editPage, name='editPage'),
path('delete/<str:metal_type>/<uuid:pk>/', views.deletePage, name='deletePage'),

]