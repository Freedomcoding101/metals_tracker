import requests
from .models import Gold, Silver, Platinum
from django.db.models import Sum, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests
from decimal import Decimal

# DASHBOARD FUNCTIONS

def get_total_oz(user, metal_type):
    model = {
        'silver': Silver,
        'gold': Gold,
        'platinum': Platinum
    }.get(metal_type.lower())

    if model is None:
        return 0

    total = model.objects.filter(owner=user).aggregate(total_weight=Sum('weight_troy_oz'))['total_weight']
    return total if total else 0

def multiply(a, b):
    result = Decimal(a) * Decimal(b)
    result_with_two_decimals = "{:.2f}".format(result)
    return result_with_two_decimals

def profit_loss(total_cost_per_unit, sell_price, quantity, customer_shipping_cost):
    profit_loss = (Decimal(sell_price) - (Decimal(total_cost_per_unit) * quantity)) + Decimal(customer_shipping_cost)
    return profit_loss

def get_total_invested(profile):
    gold_costs = Gold.objects.filter(owner=profile).aggregate(total_cost=Sum('cost_to_purchase'))['total_cost'] or 0
    silver_costs = Silver.objects.filter(owner=profile).aggregate(total_cost=Sum('cost_to_purchase'))['total_cost'] or 0
    platinum_costs = Platinum.objects.filter(owner=profile).aggregate(total_cost=Sum('cost_to_purchase'))['total_cost'] or 0

    # Convert all values to Decimal
    total_gold_cost = Decimal(gold_costs)
    total_silver_cost = Decimal(silver_costs)
    total_platinum_cost = Decimal(platinum_costs)
    # Ensure all Decimal values are rounded to two decimal places
    total_gold_cost = total_gold_cost.quantize(Decimal('0.01'))
    total_silver_cost = total_silver_cost.quantize(Decimal('0.01'))
    total_platinum_cost = total_platinum_cost.quantize(Decimal('0.01'))

    return total_gold_cost, total_silver_cost, total_platinum_cost

    # SEARCH FUNCTIONS

def searchMetals(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    gold_items = Gold.objects.distinct().filter(
        Q(item_name__icontains=search_query) |
        Q(metal_type__icontains=search_query) |
        Q(item_type__icontains=search_query) |
        Q(owner__name__icontains=search_query)|
        Q(item_year__icontains=search_query)
    )

    silver_items = Silver.objects.distinct().filter(
        Q(item_name__icontains=search_query) |
        Q(metal_type__icontains=search_query) |
        Q(item_type__icontains=search_query) |
        Q(owner__name__icontains=search_query)|
        Q(item_year__icontains=search_query)
    )

    platinum_items = Platinum.objects.distinct().filter(
        Q(item_name__icontains=search_query) |
        Q(metal_type__icontains=search_query) |
        Q(item_type__icontains=search_query) |
        Q(owner__name__icontains=search_query)|
        Q(item_year__icontains=search_query)
    )

    return {
    'gold_items': gold_items,
    'silver_items': silver_items,
    'platinum_items': platinum_items
    }, search_query


    # PAGINATION

def paginateMetals(request, metal_objects, results):
    page = request.GET.get('page')
    paginator = Paginator(metal_objects, results)
    try:
        metal_objects = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        metal_objects = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        metal_objects = paginator.page(page)


    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
        
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, metal_objects
