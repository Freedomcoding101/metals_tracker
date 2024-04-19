from django.shortcuts import render, redirect
from .models import Gold, Silver, Platinum
from .forms import GoldForm, SilverForm, PlatinumForm
from django.http import HttpResponseNotFound

# Create your views here.

def homepage(request):
    return render(request, 'tracker/index.html')

def metalPage(request, metal_type):
    metal_objects = None
    template_name = None

    if metal_type == 'gold':
        metal_objects = Gold.objects.all()
        template_name = 'tracker/gold.html'
    elif metal_type == 'silver':
        metal_objects = Silver.objects.all()
        template_name = 'tracker/silver.html'
    elif metal_type == 'platinum':
        metal_objects = Platinum.objects.all()
        template_name = 'tracker/platinum.html'
    else:
        # If metal_type is unrecognized, return a 404 response
        return HttpResponseNotFound("Metal type not found.")

    context = {'metal_objects': metal_objects}
    return render(request, template_name, context)

def updatePage(request):
    form = GoldForm()

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
            form.save()
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