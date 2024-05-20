from .models import Gold, Silver, Platinum
from django.db.models import Sum

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