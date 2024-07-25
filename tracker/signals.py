from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Gold, Silver, Platinum, Sale
from users.models import Profile
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

def update_sale(sender, instance, **kwargs):
    sale = instance
    update_sale = sale.sell_quantity
    pk = sale.object_id
    content_type = sale.content_type

    try:
        if str(content_type) == 'Tracker | gold':
            metal_model = Gold
        elif str(content_type) == 'Tracker | silver':
            metal_model = Silver
        elif str(content_type) == 'Tracker | platinum':
            metal_model = Platinum
        else:
            print("Oops! None of the above is working. Maybe it's time to mine some new ideas!")
            return

        metal_object = metal_model.objects.get(pk=pk)
        metal_object.quantity += update_sale
        metal_object.save()

        if metal_object.initial_weight_unit == 'GRAMS':
            metal_object.weight_grams = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_troy_oz = Decimal(metal_object.weight_grams) / Decimal(31.1035)
        elif metal_object.initial_weight_unit == 'TROY_OUNCES':
            metal_object.weight_troy_oz = Decimal(metal_object.quantity) * Decimal(metal_object.weight_per_unit)
            metal_object.weight_grams = Decimal(metal_object.weight_troy_oz) * Decimal(31.1035)

        metal_object.cost_to_purchase = Decimal(metal_object.quantity) * Decimal(metal_object.cost_per_unit)
        metal_object.save()

    except metal_model.DoesNotExist:
        print(f"Error: {metal_model.__name__} object with pk={pk} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

post_delete.connect(update_sale, sender=Sale)


