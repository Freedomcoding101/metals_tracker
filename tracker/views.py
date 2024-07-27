from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .utils import searchMetals, paginateMetals, profit_loss, calculate_roi
from .models import Gold, Silver, Platinum, Sale, MetalsData
from .forms import GoldForm, SilverForm, PlatinumForm, create_sell_form
from django.http import HttpResponseNotFound
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import requests
import time
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .signals import update_sale


def homepage(request):
    is_index = True
    context = {'is_index': is_index}
    try:
        return render(request, 'tracker/index.html', context)
    except Exception as e:
        raise Http404("Page not found")


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
            print('chocolate pancake')
            # metals_data.get_api_data(request.user) 

        gold_price = metals_data.current_gold_price
        silver_price = metals_data.current_silver_price
        platinum_price = metals_data.current_platinum_price

        if metal_objects:
            spot_price = None
            
            for object in metal_objects:
                if object.metal_type == 'gold':
                    spot_price = gold_price
                    object.profit = object.calculate_profit(spot_price)
                elif object.metal_type == 'silver':
                    spot_price = silver_price
                    object.profit = object.calculate_profit(spot_price)
                elif object.metal_type == 'platinum':
                    spot_price = platinum_price
                    object.profit = object.calculate_profit(spot_price)
                else:
                    raise Http404("Somehow you managed to mess up something that shouldn't ever happen, congrats!")

            for object in metal_objects:
                if object.quantity != 0:
                    object.weight = object.weight_troy_oz / object.quantity
                else:
                    object.weight = None  # or handle the zero quantity case appropriately

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
        print('strawberry pancakes')
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
        print('blueberry pancake')
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


@login_required(login_url='login-user')
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


@login_required(login_url='login-user')
def editPage(request, metal_type, pk):
    metal_model = None
    form_class = None

    # Determine the model class and form class based on the metal_type
    if metal_type == 'gold':
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

    item = get_object_or_404(metal_model, pk=pk)
    initial_weight_unit = item.initial_weight_unit if item.initial_weight_unit else None
    item_weight = item.weight_grams if item.initial_weight_unit == 'GRAMS' else item.weight_troy_oz
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            updated_item = form.save(commit=False)
            new_metal_type = form.cleaned_data['metal_type']
            new_weight_unit = form.cleaned_data['weight_unit']

            if new_metal_type != metal_type:
                new_model = None
                if new_metal_type == 'gold':
                    new_model = Gold
                elif new_metal_type == 'silver':
                    new_model = Silver
                elif new_metal_type == 'platinum':
                    new_model = Platinum
                
                if new_model:
                    new_item = new_model.objects.create(
                        owner=item.owner,
                        metal_type=new_metal_type,
                        item_type=item.item_type,
                        coa_present=item.coa_present,
                        item_year=item.item_year,
                        item_name=item.item_name,
                        item_about=item.item_about,
                        featured_image=item.featured_image if item.featured_image else new_model._meta.get_field('featured_image').default,
                        purity=item.purity,
                        quantity=item.quantity,
                        weight_troy_oz=item.weight_troy_oz,
                        weight_grams=item.weight_grams,
                        cost_to_purchase=item.cost_to_purchase,
                        spot_at_purchase=item.spot_at_purchase,
                        premium=item.premium,
                        shipping_cost=item.shipping_cost,
                        purchased_from=item.purchased_from,
                        created=item.created,
                        cost_per_unit=item.cost_per_unit,
                        total_cost_per_unit=item.total_cost_per_unit,
                        weight_per_unit=item.weight_per_unit,
                        initial_weight_unit=item.initial_weight_unit,
                    )
                    item.delete()
                    updated_item = new_item
            
            elif new_weight_unit != initial_weight_unit:
                if new_weight_unit == 'GRAMS':
                    updated_item.initial_weight_unit = new_weight_unit
                elif new_weight_unit == 'TROY_OUNCES':
                    updated_item.initial_weight_unit = new_weight_unit

            # Save the updated item
            updated_item.save()
            
            # Perform calculations
            updated_item.update_weight()
            updated_item.calculate_cost_per_unit()
            updated_item.calculate_premium()
            updated_item.calculate_total_cost_per_unit()
            
            # Save again to persist all changes
            updated_item.save()
            return redirect('singleMetal', metal_type=new_metal_type, pk=updated_item.pk)
    else:
        initial_data = {
            'weight': item_weight,
            'weight_unit': initial_weight_unit,
        }
        form = form_class(instance=item, initial=initial_data)

    context = {'form': form}
    return render(request, 'tracker/metals_form.html', context)


@login_required(login_url='login-user')
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


@login_required(login_url='login-user')
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


@login_required(login_url='login-user')
def salesPage(request, sell_id, metal_type, pk, name):
    metal_model = None
    metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
    user = request.user.profile
    sale = get_object_or_404(Sale, object_id=pk, sold_to=name, sell_id=sell_id)
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

    try:
        roi = calculate_roi(profit_output, metal_object.total_cost_per_unit)

    except Exception as e:
        print(f'An exception has occurred calculating roi {e}')

    context = {'sale': sale,
            'roi': roi,
            'sales': sales,
            'profit_output': profit_output,
            'metal_object': metal_object,
            'spot_price': spot_price,
            'cost_to_purchase': cost_to_purchase
            }
    return render(request, 'tracker/sales_page.html', context)


@login_required(login_url='login-user')
def deleteSale(request, metal_type, pk, name):
    sale = get_object_or_404(Sale, object_id=pk, sold_to=name)
    sale.delete()
    return redirect('singleMetal', metal_type=metal_type, pk=pk)


@login_required(login_url='login-user')
def soldItemsPage(request):
    context = {}
    return render(request, 'tracker/sold_items.html', context)


def update_metals_data(request):
    metals_data, created = MetalsData.objects.get_or_create(owner=request.user.profile)
    metals_data.get_api_data(request.user) 
    return JsonResponse({'metals_data': 'success'})