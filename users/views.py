from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, CustomProfileForm
from tracker.utils import get_total_oz, get_live_gold, get_live_silver, get_live_platinum, multiply

# Create your views here.

def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    user = request.user.profile
    total_silver = get_total_oz(user, 'silver')
    total_gold = get_total_oz(user, 'gold')
    total_platinum = get_total_oz(user, 'platinum')
    gold_price = get_live_gold()
    silver_price = get_live_silver()
    platinum_price = get_live_platinum()
    gmv = multiply(total_gold, gold_price)
    smv = multiply(total_silver, silver_price)
    pmv = multiply(total_platinum, platinum_price)


    context = {
        'gmv': gmv,
        'smv': smv,
        'pmv': pmv,
        'gold_price': gold_price,
        'silver_price': silver_price,
        'platinum_price': platinum_price,
        'total_silver': total_silver,
        'total_gold': total_gold,
        'total_platinum': total_platinum,
        'profile': profile
    }
    return render(request, 'users/user-profile.html', context)

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

@login_required(login_url='login-user')
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

@login_required(login_url='login-user')
def deleteAccount(request):
    account = request.user.profile

    if request.method == 'POST':
        account.delete()
        return(redirect('homepage'))

    context = {'account': account}
    return render(request, 'users/delete_account.html', context)