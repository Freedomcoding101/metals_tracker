from django.db import models
import uuid
from users.models import Profile
from decimal import Decimal
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

    UNIT_CHOICES = [
        ('GRAMS', 'Grams'),
        ('TROY_OUNCES', 'Troy Ounces'),
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='')
    item_year =models.PositiveIntegerField(null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/gold_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    weight_grams = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    spot_at_purchase = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default="")
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Gold"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "

    def save(self, *args, **kwargs):
        if self.cost_to_purchase and self.quantity:
            self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)
            
        if self.spot_at_purchase is not None:
            self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)

        if self.weight_grams is not None:
            self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
        elif self.weight_troy_oz is not None:
            self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
        super().save(*args, **kwargs)

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

    UNIT_CHOICES = [
        ('GRAMS', 'Grams'),
        ('TROY_OUNCES', 'Troy Ounces'),
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='')
    item_year =models.PositiveIntegerField(null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/silver_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    weight_grams = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    spot_at_purchase = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default='')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Silver"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "

    def save(self, *args, **kwargs):
        if self.cost_to_purchase and self.quantity:
            self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)

        if self.spot_at_purchase is not None:
            self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)

        if self.weight_grams is not None:
            self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
        elif self.weight_troy_oz is not None:
            self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
        super().save(*args, **kwargs)

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

    UNIT_CHOICES = [
        ('GRAMS', 'Grams'),
        ('TROY_OUNCES', 'Troy Ounces'),
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='')
    item_year =models.PositiveIntegerField(null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/platinum_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    weight_grams = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    spot_at_purchase = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default='')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Platinum"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "

    def save(self, *args, **kwargs):
        if self.cost_to_purchase and self.quantity:
            self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)

        if self.spot_at_purchase is not None:
            self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)

        if self.weight_grams is not None:
            self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
        elif self.weight_troy_oz is not None:
            self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)  
        super().save(*args, **kwargs)