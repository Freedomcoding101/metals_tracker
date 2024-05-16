from django.shortcuts import render
from .forms import CustomUserCreationForm

# Create your views here.

def profiles(request):
    return render(request, 'users/profiles.html')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)