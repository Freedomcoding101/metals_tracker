from django.db import models
import uuid

# Create your models here.

class Gold(models.Model):
    item_name = models.CharField(max_length=100)
    AGW = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=6)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2)
    purchased_from = models.CharField(max_length=100)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Gold"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "

class Silver(models.Model):
    item_name = models.CharField(max_length=100)
    ASW = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=6)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2)
    purchased_from = models.CharField(max_length=100)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Silver"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "

class Platinum(models.Model):
    item_name = models.CharField(max_length=100)
    APtW = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    purity = models.DecimalField(max_digits=15, decimal_places=6)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2)
    purchased_from = models.CharField(max_length=100)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Platinum"

    def __str__(self):
        return f"{self.item_name} - {self.purity} - {self.weight_troy_oz}oz "