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

    COA_PRESENT = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='round')
    coa_present = models.CharField(max_length=100, choices=COA_PRESENT, default='no')
    item_year =models.PositiveIntegerField(null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/gold_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=30, decimal_places=4)
    weight_grams = models.DecimalField(max_digits=30, decimal_places=4, default=0.00)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    spot_at_purchase = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default="")
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_sold = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    weight_per_unit = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Gold"

    def __str__(self):
        return self.item_name

    def calculate_profit(self, spot_price):
        try:
            melt_value = Decimal(self.weight_troy_oz) * Decimal(spot_price)
        except:
            print('There has been an error calculating profit')
        
        return melt_value - self.cost_to_purchase

    def update_sold(self, *args, **kwargs):
        try:
            if self.sold_to and self.sell_price and not self.date_sold:
                self.date_sold = timezone.now().date

        except:
            print('There has been an error updating date_sold')

    # def set_initial_weight_unit(self, *args, **kwargs):
    #     try:
    #         if self.initial_weight_unit == 'TROY_OUNCES':
    #             self.weight_per_unit = Decimal(weight_troy_oz) / Decimal(self.quantity)
    #         elif self.initial_weight_unit == 'GRAMS':
    #             self.weight_per_unit = Decimal(weight_grams) / Decimal(self.quantity)
    #     except:
    #         print('There has been an error calculating weight_per_unit')
    
    def save(self, *args, **kwargs):
        try:
            if self.cost_to_purchase and self.quantity:
                self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)
        except:
            print('There has been an error calculating cost_per_unit')

        try:
            if self.spot_at_purchase is not None:
                self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)
        except:
            print('There has been an error calculating premium')

        try:
            if self.weight_grams is not None:
                self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
            elif self.weight_troy_oz is not None:
                self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
        except:
            print('There has been an error calculating the troy_oz or the grams')
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

    COA_PRESENT = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='round')
    coa_present = models.CharField(max_length=100, choices=COA_PRESENT, default='no')
    item_year =models.PositiveIntegerField(null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/silver_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=30, decimal_places=4)
    weight_grams = models.DecimalField(max_digits=30, decimal_places=4, default=0.00)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    spot_at_purchase = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default='')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_sold = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    weight_per_unit = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Silver"

    def __str__(self):
        return self.item_name

    def calculate_profit(self, spot_price):
        try:
            melt_value = Decimal(self.weight_troy_oz) * Decimal(spot_price)
        except:
            print('There has been an error calculating profit')
        
        return melt_value - self.cost_to_purchase

    def update_sold(self, *args, **kwargs):
        try:
            if self.sold_to and self.sell_price and not self.date_sold:
                self.date_sold = timezone.now().date
        except:
            print('There has been an error updating date_sold')

    def save(self, *args, **kwargs):
        try:
            if self.cost_to_purchase and self.quantity:
                self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)
        except:
            print('There has been an error calculating cost_per_unit')

        try:
            if self.spot_at_purchase is not None:
                self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)
        except:
            print('There has been an error calculating premium')

        try:
            if self.weight_grams is not None:
                self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
            elif self.weight_troy_oz is not None:
                self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
        except:
            print('There has been an error calculating the troy_oz or the grams')
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

    COA_PRESENT = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True, blank=True, unique=False)
    metal_type = models.CharField(max_length=100, choices=METAL_TYPES, default='')
    item_type = models.CharField(max_length=100, choices=BAR_ROUND_MISC, default='round')
    coa_present = models.CharField(max_length=100, choices=COA_PRESENT, default='no')
    item_year =models.PositiveIntegerField(null=True, blank=True, default=None)
    item_name = models.CharField(max_length=100)
    item_about = models.TextField(max_length=500, null=True, blank=True, default="")
    featured_image = models.ImageField(default='images/platinum_avatar.jpg', null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=30, decimal_places=4)
    weight_grams = models.DecimalField(max_digits=30, decimal_places=4, default=0.00)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    spot_at_purchase = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchased_from = models.CharField(max_length=100)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default='')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_sold = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    weight_per_unit = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Platinum"

    def __str__(self):
        return self.item_name

    def calculate_profit(self, spot_price):
        try:
            melt_value = Decimal(self.weight_troy_oz) * Decimal(spot_price)
        except:
            print('There has been an error calculating profit')
        
        return melt_value - self.cost_to_purchase

    def update_sold(self, *args, **kwargs):
        try:
            if self.sold_to and self.sell_price and not self.date_sold:
                self.date_sold = timezone.now().date
        except:
            print('There has been an error updating date_sold')

    def save(self, *args, **kwargs):
        try:
            if self.cost_to_purchase and self.quantity:
                self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)
        except:
            print('There has been an error calculating cost_per_unit')

        try:
            if self.spot_at_purchase is not None:
                self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)
        except:
            print('There has been an error calculating premium')

        try:
            if self.weight_grams is not None:
                self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
            elif self.weight_troy_oz is not None:
                self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
        except:
            print('There has been an error calculating the troy_oz or the grams')
        super().save(*args, **kwargs)