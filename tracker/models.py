from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Gold(models.Model):
    METAL_TYPES = (
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('platinum', 'Platinum'),
    )

    BAR_ROUND_MISC = (
        ('bar', 'Bar'),
        ('round', 'Round'),
        ('misc', 'Misc'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='')
    item_year =models.PositiveIntegerField(max_length=30, null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/gold_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default="")
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Gold"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "

class Silver(models.Model):
    METAL_TYPES = (
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('platinum', 'Platinum'),
    )

    BAR_ROUND_MISC = (
        ('bar', 'Bar'),
        ('round', 'Round'),
        ('misc', 'Misc'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='')
    item_year =models.PositiveIntegerField(max_length=30, null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/silver_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default='')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Silver"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "

class Platinum(models.Model):
    METAL_TYPES = (
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('platinum', 'Platinum'),
    )

    BAR_ROUND_MISC = (
        ('bar', 'Bar'),
        ('round', 'Round'),
        ('misc', 'Misc'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='')
    item_year =models.PositiveIntegerField(max_length=30, null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/platinum_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default='')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Platinum"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "