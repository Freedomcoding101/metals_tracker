from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Gold, Silver, Platinum, Sale
from decimal import Decimal

def update_quantity(sender, instance, **kwargs):
    sale = instance
    update_quantity = sale.sell_quantity
    pk = sale.object_id
    content_type = sale.content_type
    print(f"Content type: {content_type}")

    if str(content_type) == 'Tracker | gold':
        metal_model = Gold
        metal_object = metal_model.objects.get(pk=pk)
        metal_object.quantity += update_quantity
        metal_object.save()
        if metal_object.initial_weight_unit == 'GRAMS':
            metal_object.weight_grams = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_troy_oz = Decimal(metal_object.weight_grams) / Decimal(31.1035)
        elif metal_object.initial_weight_unit == 'TROY_OUNCES':
            metal_object.weight_troy_oz = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_grams = Decimal(metal_object.weight_troy_oz) * Decimal(31.1035)
        metal_object.cost_to_purchase = Decimal(metal_object.quantity) * Decimal(metal_object.cost_per_unit)
        metal_object.save()
        print(f'quantity has been updated for gold')
        
    elif str(content_type) == 'Tracker | silver':
        metal_model = Silver
        metal_object = metal_model.objects.get(pk=pk)
        metal_object.quantity += update_quantity
        metal_object.save()
        if metal_object.initial_weight_unit == 'GRAMS':
            metal_object.weight_grams = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_troy_oz = Decimal(metal_object.weight_grams) / Decimal(31.1035)
        elif metal_object.initial_weight_unit == 'TROY_OUNCES':
            metal_object.weight_troy_oz = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_grams = Decimal(metal_object.weight_troy_oz) * Decimal(31.1035)
        metal_object.cost_to_purchase = Decimal(metal_object.quantity) * Decimal(metal_object.cost_per_unit)
        metal_object.save()
        print('quantity has been updated for silver')
        
    elif str(content_type) == 'Tracker | platinum':
        metal_model = Platinum
        metal_object = metal_model.objects.get(pk=pk)
        metal_object.quantity += update_quantity
        metal_object.save()
        if metal_object.initial_weight_unit == 'GRAMS':
            metal_object.weight_grams = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_troy_oz = Decimal(metal_object.weight_grams) / Decimal(31.1035)
        elif metal_object.initial_weight_unit == 'TROY_OUNCES':
            metal_object.weight_troy_oz = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_grams = Decimal(metal_object.weight_troy_oz) * Decimal(31.1035)
        metal_object.cost_to_purchase = Decimal(metal_object.quantity) * Decimal(metal_object.cost_per_unit)
        metal_object.save()
        print('quantity has been updated for platinum')
        
    else:
        print("Oops! None of the above is working. Maybe it's time to mine some new ideas!")

post_delete.connect(update_quantity, sender=Sale)