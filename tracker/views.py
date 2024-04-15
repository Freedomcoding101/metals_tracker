from django.shortcuts import render, redirect
from .models import Gold
from .forms import GoldForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def homepage(request):
    return render(request, 'tracker/index.html')

def goldpage(request):
    return render(request, 'tracker/gold.html')

def silverpage(request):
    return render(request, 'tracker/silver.html')

def platinumpage(request):
    return render(request, 'tracker/platinum.html')

def updatePage(request):
    form = GoldForm()

    if request.method == 'POST':
        form = GoldForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')

    context = {'form': form}
    return render(request, 'tracker/metals_form.html', context)