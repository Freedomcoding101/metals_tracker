from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.utils import searchMetals
from.models import Gold, Silver, Platinum
from .forms import GoldForm, SilverForm, PlatinumForm
from django.http import HttpResponseNotFound

# Create your views here.

def homepage(request):
    return render(request, 'tracker/index.html')

def searchMetal(request):
    results, search_query = searchMetals(request)
    gold_items = results['gold_items']
    silver_items = results['silver_items']
    platinum_items = results['platinum_items']
    metal_objects = list(gold_items) + list(silver_items) + list(platinum_items)

    context = {'metal_objects': metal_objects, 'search_query': search_query}
    return render(request, 'tracker/searchreturn.html', context)

@login_required
def metalPage(request, metal_type):
    metal_objects = None
    template_name = None
    results, search_query = searchMetals(request)

    if metal_type == 'gold':
        if search_query:
            metal_objects = results['gold_items']
        else:
            metal_objects = Gold.objects.filter(owner=request.user.profile)
        template_name = 'tracker/gold.html'
    elif metal_type == 'silver':
        if search_query:
            metal_objects = results['silver_items']
        else:
            metal_objects = Silver.objects.filter(owner=request.user.profile)
        template_name = 'tracker/silver.html'
    elif metal_type == 'platinum':
        if search_query:
            metal_objects = results['platinum_items']
        else:
            metal_objects = Platinum.objects.filter(owner=request.user.profile)
        template_name = 'tracker/platinum.html'
    else:
        return HttpResponseNotFound("Metal type not found.")

    context = {
        'metal_type': metal_type,
        'metal_objects': metal_objects,
        'search_query': search_query
    }
    return render(request, template_name, context)

def updatePage(request):
    form = GoldForm()
    profile = request.user.profile

    if request.method == 'POST':
        #Determine the metal type from the incoming data
        metal_type = request.POST.get('metal_type')
        
        if metal_type.lower() == 'gold':
            form = GoldForm(request.POST, request.FILES)
        elif metal_type.lower() == 'silver':
            form = SilverForm(request.POST, request.FILES)
        elif metal_type.lower() == 'platinum':
            form = PlatinumForm(request.POST, request.FILES)
        else:
            print('Unrecognized Metal Type')

        if form.is_valid():
            newmetal= form.save(commit=False)
            newmetal.owner = profile
            newmetal.save()
            return redirect('homepage')

    context = {'form': form}
    return render(request, 'tracker/metals_form.html', context)

def editPage(request, metal_type, pk):
    metal_model = None
    form_class = None

    # Determine the model class and form class based on the metal_type
    if metal_type == 'gold':
        metal_model = Gold
        form_class = GoldForm
    elif metal_type == 'silver':
        metal_model = Silver
        form_class = SilverForm
    elif metal_type == 'platinum':
        metal_model = Platinum
        form_class = PlatinumForm
    else:
        # Handle the error gracefully
        return HttpResponseServerError("Invalid metal type provided.")

    item = metal_model.objects.get(pk=pk)
    form = form_class(instance=item)

    if request.method == 'POST':
        # If the form is submitted, validate and save it
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('metal_page', metal_type=metal_type)
    else:
        # For GET requests, render the form with the item data
        form = form_class(instance=item)

    context = {'form': form}
    return render(request, 'tracker/metals_form.html', context)

def deletePage(request, metal_type, pk):
    metal_model = None
    form_class = None

    # Determine the model class and form class based on the metal_type
    if metal_type == 'gold':
        metal_model = Gold
        form_class = GoldForm
    elif metal_type == 'silver':
        metal_model = Silver
        form_class = SilverForm
    elif metal_type == 'platinum':
        metal_model = Platinum
        form_class = PlatinumForm
    else:
        # Handle the error gracefully
        return HttpResponseServerError("Invalid metal type provided.")

    item = metal_model.objects.get(pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('metal_page', metal_type=metal_type)

    context = {'item': item}
    return render(request, 'tracker/delete_template.html', context)