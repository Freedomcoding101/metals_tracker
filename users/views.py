from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, CustomProfileForm

# Create your views here.

def profiles(request):
    return render(request, 'users/profiles.html')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('edit-account')


    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method =="POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            User.objects.get(username=username)
            
        except:
            messages.error(request, 'Username does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'homepage')

        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {'page': page}
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User successfully logged out')
    return redirect('homepage')

@login_required(login_url='login-user')
def editAccount(request):
    profile = request.user.profile
    print("Profile retrieved:", profile)
    form = CustomProfileForm(instance = profile)
    print("Form data:", form)

    if request.method == 'POST':
        form = CustomProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('homepage')

    context = {'form': form, 'profile': profile}
    return render (request, 'users/profile_form.html', context)