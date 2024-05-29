from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import ContactForm


# Create your views here.

def tos_view(request):
    return render(request, 'legal/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')

def about(request):
    return render(request, 'legal/about_us.html')

def contact(request):
    form = ContactForm()


    context={'form': form}
    return render(request, 'legal/contact.html', context)