import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='yahoo_fin.stock_info')

from .models import Gold, Silver, Platinum
from django.db.models import Sum, Q
import requests
from yahoo_fin import stock_info as si




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

def get_cad_to_usd_exchange_rate():
    cad_to_usd_rate = si.get_live_price('USDCAD=X')
    return cad_to_usd_rate

def get_live_gold():
    gold_price = si.get_live_price('GC=F')
    cad_to_usd_rate = get_cad_to_usd_exchange_rate()
    gold_price_in_cad = gold_price * cad_to_usd_rate
    gold_price_rounded = round(gold_price_in_cad, 2)
    gold_price_formatted = "{:.2f}".format(gold_price_rounded)
    print(f"Current gold price: ${gold_price_rounded:.2f} per ounce")
    print(cad_to_usd_rate)
    return gold_price_formatted

def get_live_silver():
    silver_price = si.get_live_price('SI=F')
    cad_to_usd_rate = get_cad_to_usd_exchange_rate()
    silver_price_in_cad = silver_price * cad_to_usd_rate
    silver_price_rounded = round(silver_price_in_cad, 2)
    silver_price_formatted = "{:.2f}".format(silver_price_rounded)
    print(f"Current silver price: ${silver_price_rounded:.2f} per ounce")
    print(cad_to_usd_rate)
    return silver_price_formatted

def get_live_platinum():
    platinum_price = si.get_live_price('PL=F')
    cad_to_usd_rate = get_cad_to_usd_exchange_rate()
    platinum_price_in_cad = platinum_price * cad_to_usd_rate
    platinum_price_rounded = round(platinum_price_in_cad, 2)
    platinum_price_formatted = "{:.2f}".format(platinum_price_rounded)
    print(f"Current platinum price: ${platinum_price_rounded:.2f} per ounce")
    print(cad_to_usd_rate)
    return platinum_price_formatted

def multiply(a, b):
    result = float(a) * float(b)
    result_with_two_decimals = "{:.2f}".format(result)
    return result_with_two_decimals



    # SEARCH FUNCTIONS

def searchMetals(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    gold_items = Gold.objects.distinct().filter(
        Q(item_name__icontains=search_query) |
        Q(metal_type__icontains=search_query) |
        Q(item_type__icontains=search_query) |
        Q(owner__name__icontains=search_query)
    )

    silver_items = Silver.objects.distinct().filter(
        Q(item_name__icontains=search_query) |
        Q(metal_type__icontains=search_query) |
        Q(item_type__icontains=search_query) |
        Q(owner__name__icontains=search_query)
    )

    platinum_items = Platinum.objects.distinct().filter(
        Q(item_name__icontains=search_query) |
        Q(metal_type__icontains=search_query) |
        Q(item_type__icontains=search_query) |
        Q(owner__name__icontains=search_query)
    )

    return {
    'gold_items': gold_items,
    'silver_items': silver_items,
    'platinum_items': platinum_items
    }, search_query