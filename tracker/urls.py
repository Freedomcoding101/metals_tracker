from django.urls import path
from . import views

urlpatterns = [
path('', views.homepage, name="homepage"),
path('search-stack/', views.searchMetal, name='searchMetal'),
path('update/', views.updatePage, name = "updatePage"),
path('single_metal/<str:metal_type>/<uuid:pk>', views.singleMetal, name='singleMetal'),
path('<str:metal_type>/', views.metalPage, name='metal_page'),
path('edit/<str:metal_type>/<uuid:pk>/', views.editPage, name='editPage'),
path('sell/<str:metal_type>/<uuid:pk>/', views.sellPage, name='sellPage'),
path('delete/<str:metal_type>/<uuid:pk>/', views.deletePage, name='deletePage'),
path('sales/<str:metal_type>/<uuid:pk>/<str:name>', views.salesPage, name='salesPage'),
path('delete-sale/<str:metal_type>/<uuid:pk>/<str:name>', views.deleteSale, name='deleteSale'),


]