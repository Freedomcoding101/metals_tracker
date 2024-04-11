from django.shortcuts import render, redirect

# Create your views here.

def homepage(request):
    return render(request, 'tracker/index.html')

def goldpage(request):
    return render(request, 'tracker/gold.html')

def silverpage(request):
    return render(request, 'tracker/silver.html')

def platinumpage(request):
    return render(request, 'tracker/platinum.html')