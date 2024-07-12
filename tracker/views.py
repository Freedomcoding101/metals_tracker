from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from.utils import searchMetals, paginateMetals, profit_loss
from.models import Gold, Silver, Platinum, Sale, MetalsData
from .forms import GoldForm, SilverForm, PlatinumForm, create_sell_form
from django.http import HttpResponseNotFound
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import requests
import time

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
    metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
    five_minutes_later = metals_data.timestamp + 300
    unix_time_now = int(time.time())
    if metals_data.current_gold_price == 0:
        metals_data.get_api_data(request.user)
    
    elif (unix_time_now - five_minutes_later) > 300:
        print('pancake')
        # metals_data.get_api_data(request.user) 

    gold_price = metals_data.current_gold_price
    silver_price = metals_data.current_silver_price
    platinum_price = metals_data.current_platinum_price


    if metal_objects:
        spot_price = None
        
        for object in metal_objects:
            if object.metal_type == 'gold':
                spot_price = gold_price
            elif object.metal_type == 'silver':
                spot_price = silver_price
            elif object.metal_type == 'platinum':
                spot_price = platinum_price
            else:
                return HttpResponse("Somehow you managed to mess up something that shouldnt ever happen, congrats!")

        object.profit = object.calculate_profit(spot_price)

        for object in metal_objects:
            object.weight = object.weight_troy_oz / object.quantity

        context = {'metal_objects': metal_objects,
                'search_query': search_query,
                'custom_range': custom_range,
                'object.profit': object.profit,
                'object.weight': object.weight,
                'spot_price': spot_price
                }

    # If there is any errors it will set the context to this to prevent errors when the next page loads
    else:
        context = {'metal_objects': [],
                'search_query': search_query,
                'custom_range': [],
                'object.profit': 0,
                'object.weight': 0,
                'spot_price':  0
    }

    return render(request, 'tracker/searchreturn.html', context)

@login_required(login_url='login-user')
def metalPage(request, metal_type):
    metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
    five_minutes_later = metals_data.timestamp + 300
    unix_time_now = int(time.time())
    if metals_data.current_gold_price == 0:
        metals_data.get_api_data(request.user)
    
    elif (unix_time_now - five_minutes_later) > 300:
        print('pancakes')
        # metals_data.get_api_data(request.user) 

    gold_price = metals_data.current_gold_price
    silver_price = metals_data.current_silver_price
    platinum_price = metals_data.current_platinum_price
    print(f"Gold {gold_price}")
    print(f"Silver {silver_price}")
    print(f"Platinum {platinum_price}")

    metal_objects = None
    template_name = None
    results, search_query = searchMetals(request)
    
    if metal_type == 'gold':
        spot_price = gold_price
        if search_query:
            metal_objects = results.get('gold_items')
        else:
            metal_objects = Gold.objects.filter(owner=request.user.profile)
        template_name = 'tracker/gold.html'
    elif metal_type == 'silver':
        spot_price = silver_price
        if search_query:
            metal_objects = results.get('silver_items')
        else:
            metal_objects = Silver.objects.filter(owner=request.user.profile)
        template_name = 'tracker/silver.html'
    elif metal_type == 'platinum':
        spot_price = platinum_price
        if search_query:
            metal_objects = results.get('platinum_items')
        else:
            metal_objects = Platinum.objects.filter(owner=request.user.profile)
        template_name = 'tracker/platinum.html'
    else:
        raise Http404

    if metal_objects:
        custom_range, metal_objects = paginateMetals(request, metal_objects, 6)

        for object in metal_objects:
            object.profit = object.calculate_profit(spot_price)

        for object in metal_objects:
            object.weight = object.weight_per_unit

        context = {
            'object.weight': object.weight,
            'object.profit': object.profit,
            'spot_price': spot_price,
            'custom_range': custom_range,
            'metal_type': metal_type,
            'metal_objects': metal_objects,
            'search_query': search_query
        }

        # If there is any errors it will set the context to this to prevent errors when the next page loads
    else:
        context = {
            'object.weight': 0,
            'object.profit': 0,
            'spot_price': 0,
            'custom_range': [],
            'metal_type': metal_type,
            'metal_objects': [],
            'search_query': search_query
        }
        print('There are some massive errors going on here!')

    return render(request, template_name, context)

@login_required(login_url='login-user')
def singleMetal(request, metal_type, pk):
    metal_model = None
    metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
    five_minutes_later = metals_data.timestamp + 300
    unix_time_now = int(time.time())
    if metals_data.current_gold_price == 0:
        metals_data.get_api_data(request.user)
    
    elif (unix_time_now - five_minutes_later) > 300:
        print('pancake')
        print(unix_time_now)
        print(five_minutes_later)
        # metals_data.get_api_data(request.user) 

    gold_price = metals_data.current_gold_price
    silver_price = metals_data.current_silver_price
    platinum_price = metals_data.current_platinum_price

    if metal_type == 'gold':
        spot_price = gold_price
        metal_model = Gold
        metal_object = metal_model.objects.get(pk=pk)
        
    elif metal_type == 'silver':
        spot_price = silver_price
        metal_model = Silver
        metal_object = metal_model.objects.get(pk=pk)
    elif metal_type == 'platinum':
        spot_price = platinum_price
        metal_model = Platinum
        metal_object = metal_model.objects.get(pk=pk)

    try:
        metal_content_type = ContentType.objects.get_for_model(metal_object)
        sales = Sale.objects.filter(content_type=metal_content_type, object_id=metal_object.id)
        shipping_profit = sales.aggregate(total=Sum('shipping_cost'))['total']
        total_sell_price = sales.aggregate(total=Sum('sell_price'))['total']
        total_sell_quantity = sales.aggregate(total=Sum('sell_quantity'))['total']
        profit_output = profit_loss(metal_object.total_cost_per_unit, total_sell_price, total_sell_quantity, shipping_profit)
    except Exception as e:
        print(f"An exception occured: {e}")
        profit_output = 'N/A'
        sales = Sale.objects.none()

    # GRAB THE CURRENT GOLD PRICE AND OUTPUT THE MELT VALUE TO TEMPLATE
    try:
        melt_string = f"{metal_object.metal_type}_price"
        melt_price = round((Decimal(eval(melt_string)) * Decimal(metal_object.weight_troy_oz)), 2)
    except:
        melt_price = 'N/A'

    if metal_object.quantity >= 1:
        total_cost_per_unit = metal_object.total_cost_per_unit
        shipping_cost = metal_object.shipping_cost
    else:
        total_cost_per_unit = round(Decimal(0.00), 2)
        shipping_cost = round(Decimal(0.00), 2)

    object_weight = metal_object.weight_per_unit
    profit_loss_ur = metal_object.calculate_profit(spot_price)

    context = { 'profit_loss_ur': profit_loss_ur,
                'object_weight': object_weight,
                'metal_object': metal_object,
                'shipping_cost': shipping_cost,
                'total_cost_per_unit': total_cost_per_unit,
                'profit_output': profit_output,
                'melt_price': melt_price,
                'sales': sales}

    return render(request, 'tracker/single_metal_page.html', context)

def updatePage(request):
    form = GoldForm()
    profile = request.user.profile

    if request.method == 'POST':
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
            newmetal.update_weight()
            newmetal.calculate_cost_per_unit()
            newmetal.calculate_premium()
            newmetal.save()
            newmetal.calculate_total_cost_per_unit()
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
        initial_weight_unit = item.initial_weight_unit
        
        if initial_weight_unit == 'GRAMS':
            initial_weight = item.weight_grams


        elif initial_weight_unit == "TROY_OUNCES":
            initial_weight = item.weight_troy_oz

    if request.method == 'POST':
        # If the form is submitted, validate and save it
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('singleMetal', metal_type=metal_type, pk=item.pk)
        else:
            print(form.errors)
    else:
        # For GET requests, render the form with the item data
        form = form_class(instance=item, initial={'weight_unit': initial_weight_unit, 'weight': initial_weight})

    context = {'form': form}
    return render(request, 'tracker/metals_form.html', context)

def sellPage(request, metal_type, pk):
    metal_model = None

    if metal_type == 'gold':
        metal_model = Gold
    elif metal_type == 'silver':
        metal_model = Silver
    elif metal_type == 'platinum':
        metal_model = Platinum
    else:
        # Handle the error gracefully
        return HttpResponseServerError("Invalid metal type provided.")

    item = metal_model.objects.get(pk=pk)
    user = request.user.profile
    SellForm = create_sell_form()
    form = SellForm()

    if request.method == "POST":
        form = SellForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.owner = user
            sale.content_type = ContentType.objects.get_for_model(type(item))
            sale.object_id = item.id
            sale.save()
            return redirect('singleMetal', metal_type=item.metal_type, pk=item.id)
        else:
            print(form.errors)
            print('Errors occurred during validation!')

    context ={'item': item,
            'form': form,
    }
    return render(request, 'tracker/sell_form.html', context)

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


def salesPage(request, metal_type, pk, name):
    metal_model = None
    metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
    user = request.user.profile
    sale = get_object_or_404(Sale, object_id=pk, sold_to=name)
    gold_price = metals_data.current_gold_price
    silver_price = metals_data.current_silver_price
    platinum_price = metals_data.current_platinum_price

    if metal_type == 'gold':
        spot_price = gold_price
        metal_model = Gold
        metal_object = metal_model.objects.get(pk=pk)
        
    elif metal_type == 'silver':
        spot_price = silver_price
        metal_model = Silver
        metal_object = metal_model.objects.get(pk=pk)
    elif metal_type == 'platinum':
        spot_price = platinum_price
        metal_model = Platinum
        metal_object = metal_model.objects.get(pk=pk)

    try:
        profit_output = profit_loss(metal_object.total_cost_per_unit, sale.sell_price, sale.sell_quantity, sale.shipping_cost)
        cost_to_purchase = metal_object.total_cost_per_unit * sale.sell_quantity

    except Exception as e:
        print(f"An exception occured: {e}")
        profit_output = 'N/A'
        cost_to_purchase = 'N/A'

    try:
        metal_content_type = ContentType.objects.get_for_model(metal_object)
        sales = Sale.objects.filter(content_type=metal_content_type, object_id=metal_object.id)

    except Exception as e:
        print(f"An exception occured: {e}")
        sales = Sale.objects.none()

    context = {'sale': sale,
            'sales': sales,
            'profit_output': profit_output,
            'metal_object': metal_object,
            'spot_price': spot_price,
            'cost_to_purchase': cost_to_purchase
            }
    return render(request, 'tracker/sales_page.html', context)


def editSale(request, metal_type, pk, name):
    sale = get_object_or_404(Sale, object_id=pk, sold_to=name)
    form = create_sell_form(instance=sale)

    if request.method == 'POST':
        form = create_sell_form(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('salesPage', metal_type=metal_type, pk=pk, name=name)
        else:
            print(form.errors)
            print('Errors occurred during validation!')

    context = {'form': form, 'sale': sale}
    return render(request, 'tracker/sell_form.html', context)