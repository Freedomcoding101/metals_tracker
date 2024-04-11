from django.urls import path
from . import views

urlpatterns = [
path('', views.homepage, name="homepage"),
path('gold/', views.goldpage, name="goldpage"),
path('platinum/', views.platinumpage, name="platinumpage"),
path('silver/', views.silverpage, name="silverpage")

]