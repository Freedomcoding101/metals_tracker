from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from tracker.models import MetalsData
from .models import Profile
from .forms import CustomUserCreationForm, CustomProfileForm
from tracker.utils import get_total_oz, multiply, get_total_invested
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

# Create your views here.

@login_required(login_url='login-user')
def profile(request, pk):
    metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
    profile = Profile.objects.get(id=pk)
    user = request.user.profile
    total_silver = round(Decimal(get_total_oz(user, 'silver')), 2)
    total_gold = round(Decimal(get_total_oz(user, 'gold')), 2)
    total_platinum = round(Decimal(get_total_oz(user, 'platinum')), 2)
    total_gold_cost, total_silver_cost, total_platinum_cost =  get_total_invested(profile)
    # Calculate DCA using Decimal and rounding to 2 decimal places
    try:
        if total_gold != 0:
            gdca = (total_gold_cost / total_gold).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            gdca_str = f"{gdca:.2f}"
        else:
            gdca = 'N/A'
            gdca_str = 'N/A'
    except InvalidOperation:
        gdca = 'N/A'
        gdca_str = 'N/A'
    try:
        if total_silver != 0:
            sdca = (total_silver_cost / total_silver).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            sdca_str = f"{sdca:.2f}"
        else:
            sdca = 'N/A'
            sdca_str = 'N/A'
    except InvalidOperation:
        sdca = 'N/A'
        sdca_str = 'N/A'
    try:
        if total_platinum != 0:
            pdca = (total_platinum_cost / total_platinum).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            pdca_str = f"{pdca:.2f}"
        else:
            pdca = 'N/A'
            pdca_str = 'N/A'
    except InvalidOperation:
        pdca = 'N/A'
        pdca_str = 'N/A'

    try:
        gold_price = Decimal(metals_data.current_gold_price)
        silver_price = Decimal(metals_data.current_silver_price)
        platinum_price = Decimal(metals_data.current_platinum_price)
    except Exception as e:
        print(f'There has been an error in the profile view: {e}')
        gold_price = 'N/A'
        silver_price = 'N/A'
        platinum_price = 'N/A'

    try:
        # GOLD MARKET VALUE
        gmv = multiply(total_gold, gold_price)
        # SILVER MARKET VALUE
        smv = multiply(total_silver, silver_price)
        # PLATINUM MARKET VALUE
        pmv = multiply(total_platinum, platinum_price)
        # GOLD TO SILVER RATIO
        gsr = round((float(gold_price) / float(silver_price)), 2)
        # PLATINUM TO SILVER RATIO
        psr = round((float(platinum_price) / float(silver_price)), 2)
        # PLATINUM TO GOLD RATIO
        pgr = round((float(gold_price) / float(platinum_price)), 2)

    except:
        pgr = 'N/A'
        psr = 'N/A'
        gmv = 'N/A'
        smv = 'N/A'
        pmv = 'N/A'
        gsr = 'N/A'


    context = {
        'gdca': gdca_str,
        'sdca': sdca_str,
        'pdca': pdca_str,
        'pgr': pgr,
        'psr': psr,
        'gsr': gsr,
        'gmv': gmv,
        'smv': smv,
        'pmv': pmv,
        'total_gold_cost': total_gold_cost,
        'total_silver_cost': total_silver_cost,
        'total_platinum_cost': total_platinum_cost,
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

    messages.info(request, 'PLEASE REMEMBER TO USE A PSEUDONAME AND A EMAIL ACCOUNT NOT LINKED TO YOUR NAME')

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
    messages.success(request, 'User successfully logged out')
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

            return redirect('profile', pk=profile.id)

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