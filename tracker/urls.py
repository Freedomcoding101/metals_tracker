from django.urls import path
from . import views

urlpatterns = [
path('', views.homepage, name="homepage"),
# path('gold/', views.goldpage, name="goldpage"),
# path('platinum/', views.platinumpage, name="platinumpage"),
# path('silver/', views.silverpage, name="silverpage"),
path('update/', views.updatePage, name = "updatePage"),
path('<str:metal_type>/', views.metalPage, name='metal_page'),
path('edit/<str:metal_type>/<uuid:pk>/', views.editPage, name='editPage')
]