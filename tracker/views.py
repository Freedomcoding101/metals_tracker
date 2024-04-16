from django.shortcuts import render, redirect
from .models import Gold, Silver, Platinum
from .forms import GoldForm, SilverForm, PlatinumForm

# Create your views here.

def homepage(request):
    return render(request, 'tracker/index.html')

def metal_page(request, metal_type):
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

    context = {'metal_objects': metal_objects}
    return render(request, template_name, context)

def updatePage(request):
    form = GoldForm()

    if request.method == 'POST':
        #Determine the metal type from the incoming data
        metal_type = request.POST.get('metal_type')
        
        if metal_type.lower() == 'gold':
            form = GoldForm(request.POST)
        elif metal_type.lower() == 'silver':
            form = SilverForm(request.POST)
        elif metal_type.lower() == 'platinum':
            form = PlatinumForm(request.POST)
        else:
            print('Unrecognized Metal Type')

        if form.is_valid():
            form.save()
            return redirect('homepage')

    context = {'form': form}
    return render(request, 'tracker/metals_form.html', context)