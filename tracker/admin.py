from django.contrib import admin
from .models import Gold, Silver, Platinum, Sale, MetalsData
# Register your models here.

admin.site.register(Gold)
admin.site.register(Silver)
admin.site.register(Platinum)
admin.site.register(MetalsData)

class SaleAdmin(admin.ModelAdmin):
    list_display = ('sell_id', 'owner', 'sell_price', 'sell_quantity', 'sold_to', 'shipping_cost', 'date_sold', 'created', 'profit')

admin.site.register(Sale, SaleAdmin)