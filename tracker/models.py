from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import uuid
from users.models import Profile
from decimal import Decimal
import requests
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
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
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    total_cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    weight_per_unit = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Gold"

    def __str__(self):
        return (f"{self.item_year} {self.metal_type} {self.item_name} {self.item_type} {self.id}")

    def reverse_sale(self, sale, metal_object):
        pass

    def calculate_profit(self, spot_price):
        if self.quantity > 0:
            try:
                melt_value = Decimal(self.weight_troy_oz) * Decimal(spot_price) 
                profit = melt_value - (self.total_cost_per_unit * self.quantity)
            except Exception as e:
                print(f'There has been an error {e}')
            
            return profit
        
        else:
            profit = 0.00
            return profit

    def update_weight(self):
        if self.quantity > 0:
            try:
                if self.weight_grams is not None:
                    self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
                elif self.weight_troy_oz is not None:
                    self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
            except Exception as e:
                print(f'There has been an error {e}')
        
        else: 
            self.weight_troy_oz = 0
            self.weight_grams = 0

    def calculate_cost_per_unit(self):
        try:
            if self.cost_to_purchase and self.quantity != 0:
                self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)
            self.save()
        except Exception as e:
            print(f'There has been an error {e}')
            self.cost_per_unit = 0.00

    def calculate_total_cost_per_unit(self):
        try:
            if self.cost_to_purchase is not None and self.shipping_cost is not None and self.weight_troy_oz is not None:
                self.total_cost_per_unit = round(((Decimal(self.cost_to_purchase) + Decimal(self.shipping_cost)) / Decimal(self.quantity)), 2)
            else:
                return "One or more required fields are None"
        except Exception as e:
            print(f'An error occurred in the model/cacluclate_total_cost_per_unit: {e}')
        self.save()

    def calculate_premium(self):
        if self.cost_to_purchase and self.spot_at_purchase and self.quantity > 0:
            try:
                if self.spot_at_purchase is not None:
                    self.premium = Decimal(self.cost_per_unit) - (Decimal(self.spot_at_purchase) * (Decimal(self.weight_troy_oz) / Decimal(self.quantity)))
            except Exception as e:
                print(f'There has been an error calculating premium in the model file... {e}')

        else:
            self.cost_per_unit = 0.00

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
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    total_cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    weight_per_unit = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Silver"

    def __str__(self):
        return (f"{self.item_year} {self.metal_type} {self.item_name} {self.item_type} {self.id}")

    def reverse_sale(self, sale, metal_object):
        sell_quantity = sale.sell_quantity
        metal_object.quantity += sell_quantity
        metal_object.save()
        metal_object.update_weight()
        metal_object.calculate_cost_per_unit()
        pass

    def calculate_profit(self, spot_price):
        if self.quantity > 0:
            try:
                melt_value = Decimal(self.weight_troy_oz) * Decimal(spot_price) 
                profit = melt_value - (self.total_cost_per_unit * self.quantity)
            except Exception as e:
                print(f'There has been an error {e}')
            
            return profit
        
        else:
            profit = 0.00
            return profit

    def update_weight(self):
        if self.quantity > 0:
            try:
                if self.weight_grams is not None:
                    self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
                elif self.weight_troy_oz is not None:
                    self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
            except Exception as e:
                print(f'There has been an error {e}')
        
        else: 
            self.weight_troy_oz = 0
            self.weight_grams = 0

    def calculate_cost_per_unit(self):
        try:
            if self.cost_to_purchase and self.quantity != 0:
                self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)
            self.save()
        except Exception as e:
            print(f'There has been an error {e}')
            self.cost_per_unit = 0.00

    def calculate_total_cost_per_unit(self):
        try:
            if self.cost_to_purchase is not None and self.shipping_cost is not None and self.weight_troy_oz is not None:
                self.total_cost_per_unit = round(((Decimal(self.cost_to_purchase) + Decimal(self.shipping_cost)) / Decimal(self.quantity)), 2)
            else:
                return "One or more required fields are None"
        except Exception as e:
            print(f'An error occurred in the model/cacluclate_total_cost_per_unit: {e}')
        self.save()

    def calculate_premium(self):
        if self.cost_per_unit:
            try:
                if self.spot_at_purchase is not None:
                    self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)
                self.save()
            except Exception as e:
                print(f'There has been an error {e}')

        else:
            self.cost_per_unit = 0.00

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
    created = models.DateTimeField(auto_now_add=True)
    cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    total_cost_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=None)
    weight_per_unit = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    initial_weight_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='TROY_OUNCES')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Platinum"

    def __str__(self):
        return (f"{self.item_year} {self.metal_type} {self.item_name} {self.item_type} {self.id}")

    def calculate_profit(self, spot_price):
        if self.quantity > 0:
            try:
                melt_value = Decimal(self.weight_troy_oz) * Decimal(spot_price) 
                profit = melt_value - (self.total_cost_per_unit * self.quantity)
            except Exception as e:
                print(f'There has been an error {e}')
            
            return profit
        
        else:
            profit = 0.00
            return profit

    def update_weight(self):
        if self.quantity > 0:
            try:
                if self.weight_grams is not None:
                    self.weight_troy_oz = Decimal(self.weight_grams) / Decimal(31.1035)
                elif self.weight_troy_oz is not None:
                    self.weight_grams = Decimal(self.weight_troy_oz) * Decimal(31.1035)
            except Exception as e:
                print(f'There has been an error {e}')
        
        else: 
            self.weight_troy_oz = 0
            self.weight_grams = 0

    def calculate_cost_per_unit(self):
        try:
            if self.cost_to_purchase and self.quantity != 0:
                self.cost_per_unit = Decimal(self.cost_to_purchase) / Decimal(self.quantity)
            self.save()
        except Exception as e:
            print(f'There has been an error {e}')
            self.cost_per_unit = 0.00

    def calculate_total_cost_per_unit(self):
        try:
            if self.cost_to_purchase is not None and self.shipping_cost is not None and self.weight_troy_oz is not None:
                self.total_cost_per_unit = round(((Decimal(self.cost_to_purchase) + Decimal(self.shipping_cost)) / Decimal(self.quantity)), 2)
            else:
                return "One or more required fields are None"
        except Exception as e:
            print(f'An error occurred in the model/cacluclate_total_cost_per_unit: {e}')
        self.save()

    def calculate_premium(self):
        if self.cost_per_unit:
            try:
                if self.spot_at_purchase is not None:
                    self.premium = Decimal(self.cost_per_unit) - Decimal(self.spot_at_purchase)
                self.save()
            except Exception as e:
                print(f'There has been an error {e}')

        else:
            self.cost_per_unit = 0.00


class Sale(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sell_id = models.IntegerField(primary_key=True, editable=False)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    sell_quantity = models.DecimalField(max_digits=30, decimal_places=2, null=False, blank=False)
    sold_to = models.CharField(max_length=100, null=True, blank=True, default='')
    shipping_cost = models.DecimalField(max_digits=30, decimal_places=2, null=False, blank=False)
    date_sold = models.DateField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    spot_price = models.DecimalField(max_digits=20, decimal_places=2)
    profit = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    #Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.UUIDField(default=uuid.uuid4, editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        item = self.content_object

        if not self.created:
            self.created = timezone.now()
        
        if self.sell_quantity > item.quantity:
            raise ValidationError('You cannot sell more than you have!')
        elif item.quantity == 0:
            raise ValidationError('You cannot sell an item with a quantity of 0!')
        else:
            item.quantity -= self.sell_quantity
            if item.initial_weight_unit == 'GRAMS':
                item.weight_grams = item.weight_per_unit * item.quantity
                item.weight_troy_oz = item.weight_grams / Decimal(31.1035)
                item.cost_to_purchase = item.quantity * item.cost_per_unit
            elif item.initial_weight_unit == 'TROY_OUNCES':
                item.weight_troy_oz = item.weight_per_unit * item.quantity
                item.weight_grams = item.weight_troy_oz * Decimal(31.1035)
                item.cost_to_purchase = item.quantity * item.cost_per_unit
            item.save()
        
        if item.initial_weight_unit == "TROY_OUNCES":
            item.weight_troy_oz = item.weight_per_unit * item.quantity
            item.weight_grams = item.weight_troy_oz * Decimal(31.1035)

        elif item.initial_weight_unit == "GRAMS":
            item.weight_grams = item.weight_per_unit * item.quantity
            item.weight_troy_oz = item.weight_grams / Decimal(31.1035)

        item.cost_to_purchase = item.quantity * item.cost_per_unit
        item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sell_quantity} of {self.content_object} sold to {self.sold_to}"


class MetalsData(models.Model):
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
    timestamp = models.IntegerField(default=0)
    rates = models.JSONField(default=dict)
    currency = models.CharField(max_length=30)
    current_gold_price = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    current_silver_price = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    current_platinum_price = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Metals Data"

    def __str__(self):
        return f"Gold: {self.current_gold_price}, Platinum: {self.current_platinum_price}, Silver: {self.current_silver_price}"

    def get_api_data(self, user):
        response = requests.get('https://api.metalpriceapi.com/v1/latest?api_key=6178fa0527aabdb25fa2c141a7b07f62&base=CAD&currencies=XAU,%20XAG,%20XPT')
        data = response.json()
        print(data)
        self.owner = user.profile
        self.timestamp = data['timestamp']
        self.rates = data['rates']
        self.current_gold_price = data['rates']['CADXAU']
        self.current_silver_price = data['rates']['CADXAG']
        self.current_platinum_price = data['rates']['CADXPT']
        self.save()
