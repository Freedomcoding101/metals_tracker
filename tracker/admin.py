from django.contrib import admin
from .models import Gold, Silver, Platinum, Sale
# Register your models here.

admin.site.register(Gold)
admin.site.register(Silver)
admin.site.register(Platinum)
admin.site.register(Sale)