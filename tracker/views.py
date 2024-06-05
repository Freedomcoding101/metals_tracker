from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.utils import searchMetals, paginateMetals, profit_loss, get_live_gold, get_live_silver, get_live_platinum
from.models import Gold, Silver, Platinum
from .forms import GoldForm, SilverForm, PlatinumForm
from django.http import HttpResponseNotFound
from decimal import Decimal

# Create your views here.

def homepage(request):
    return render(request, 'tracker/index.html')

@login_required(login_url='login-user')
def searchMetal(request):
    results, search_query = searchMetals(request)
    gold_items = results['gold_items']
    silver_items = results['silver_items']
    platinum_items = results['platinum_items']
    metal_objects = list(gold_items) + list(silver_items) + list(platinum_items)
    custom_range, metal_objects = paginateMetals(request, metal_objects, 6)

    context = {'metal_objects': metal_objects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'tracker/searchreturn.html', context)

@login_required(login_url='login-user')
def metalPage(request, metal_type):
    metal_objects = None
    template_name = None
    results, search_query = searchMetals(request)

    if metal_type == 'gold':
        spot_price = Decimal(get_live_gold())
        if search_query:
            metal_objects = results['gold_items']
        else:
            metal_objects = Gold.objects.filter(owner=request.user.profile)
        template_name = 'tracker/gold.html'
    elif metal_type == 'silver':
        spot_price = Decimal(get_live_silver())
        if search_query:
            metal_objects = results['silver_items']
        else:
            metal_objects = Silver.objects.filter(owner=request.user.profile)
        template_name = 'tracker/silver.html'
    elif metal_type == 'platinum':
        spot_price = Decimal(get_live_platinum())
        if search_query:
            metal_objects = results['platinum_items']
        else:
            metal_objects = Platinum.objects.filter(owner=request.user.profile)
        template_name = 'tracker/platinum.html'
    else:
        return HttpResponseNotFound("Metal type not found.")

    custom_range, metal_objects = paginateMetals(request, metal_objects, 6)

    for object in metal_objects:
        object.profit = object.calculate_profit(spot_price)

    for object in metal_objects:
        object.weight = object.weight_troy_oz / object.quantity

    context = {
        'object.weight': object.weight,
        'object.profit': object.profit,
        'spot_price': spot_price,
        'custom_range': custom_range,
        'metal_type': metal_type,
        'metal_objects': metal_objects,
        'search_query': search_query
    }
    return render(request, template_name, context)

@login_required(login_url='login-user')
def singleMetal(request, metal_type, pk):
    metal_model = None

    if metal_type == 'gold':
        spot_price = get_live_gold()
        metal_model = Gold
        metal_object = metal_model.objects.get(pk=pk)
        
    elif metal_type == 'silver':
        spot_price = get_live_silver()
        metal_model = Silver
        metal_object = metal_model.objects.get(pk=pk)
    elif metal_type == 'platinum':
        spot_price = get_live_platinum()
        metal_model = Platinum
        metal_object = metal_model.objects.get(pk=pk)

    # GRAB THE PROFIT/LOSS IF THERE IS THE CORRECT INFORMATION AVAILABLE, OTHERWISE SET TO N/A
    try:
        profit_output = profit_loss(metal_object.cost_to_purchase, metal_object.sell_price, metal_object.shipping_cost)
    except:
        profit_output = 'N/A'

    # SET SELL PRICE AND SOLD TO TO N/A IF THERE IS NONE PRESENT
    if metal_object.sell_price == None:
        metal_object.sell_price = 'N/A'
    if metal_object.sold_to == None:
        metal_object.sold_to = ''

    # GRAB THE CURRENT GOLD PRICE AND OUTPUT THE MELT VALUE TO TEMPLATE
    try:
        melt_string = f"get_live_{metal_object.metal_type}()"
        melt_price = round((Decimal(eval(melt_string)) * Decimal(metal_object.weight_troy_oz)), 2)
    except:
        melt_price = 'N/A'

    cost_per_oz = round(((metal_object.cost_to_purchase + metal_object.shipping_cost) / metal_object.weight_troy_oz), 2)
    object_weight = metal_object.weight_troy_oz / metal_object.quantity
    profit_loss = metal_object.calculate_profit(spot_price)

    context = { 'profit_loss': profit_loss,
                'object_weight': object_weight,
                'metal_object': metal_object,
                'cost_per_oz': cost_per_oz,
                'profit_output': profit_output,
                'melt_price': melt_price}

    return render(request, 'tracker/single_metal_page.html', context)

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
    initial_weight_unit = None
    initial_weight = None
    
    if item.initial_weight_unit:
        print("THERE IS!")
        initial_weight_unit = item.initial_weight_unit
        print(initial_weight_unit)
        
        if initial_weight_unit == 'GRAMS':
            initial_weight = item.weight_grams
            print(f"{initial_weight} grams")

        elif initial_weight_unit == "TROY_OUNCES":
            initial_weight = item.weight_troy_oz
            print(f"{initial_weight} oz")

    if request.method == 'POST':
        # If the form is submitted, validate and save it
        form = form_class(request.POST, request.FILES, instance=item)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('singleMetal', metal_type=metal_type, pk=item.pk)
    else:
        # For GET requests, render the form with the item data
        form = form_class(instance=item, initial={'weight_unit': initial_weight_unit, 'weight': initial_weight})

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