from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Gold, Silver, Platinum, Sale

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
        print(f'quantity has been updated for gold')
        
    elif str(content_type) == 'Tracker | silver':
        metal_model = Silver
        metal_object = metal_model.objects.get(pk=pk)
        metal_object.quantity += update_quantity
        metal_object.save()
        print('quantity has been updated for silver')
        
    elif str(content_type) == 'Tracker | platinum':
        metal_model = Platinum
        metal_object = metal_model.objects.get(pk=pk)
        metal_object.quantity += update_quantity
        metal_object.save()
        print('quantity has been updated for platinum')
        
    else:
        print("Oops! None of the above is working. Maybe it's time to mine some new ideas!")

post_delete.connect(update_quantity, sender=Sale)