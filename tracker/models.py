from django.db import models

# Create your models here.

class Gold(models.Model):
    ITEM_TYPE_CHOICES = (
        ('Round', 'Round'),
        ('Bar', 'Bar'),
        ('Misc', 'Miscellaneous')
    )
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    agw = models.DecimalField(max_digits=10, decimal_places=4)
    purity = models.DecimalField(max_digits=15, decimal_places=6)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2)
    coa_present = models.BooleanField(default=False) #Certificate of Authentication
    purchased_from = models.CharField(max_length=100)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Gold"

    def __str__(self):
        return f"{self.name} - {self.item_type} - {self.purity} - {self.weight_troy_oz}oz "

class Silver(models.Model):
    ITEM_TYPE_CHOICES = (
        ('Round', 'Round'),
        ('Bar', 'Bar'),
        ('Misc', 'Miscellaneous')
    )
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    agw = models.DecimalField(max_digits=10, decimal_places=4)
    purity = models.DecimalField(max_digits=15, decimal_places=6)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2)
    coa_present = models.BooleanField(default=False) #Certificate of Authentication
    purchased_from = models.CharField(max_length=100)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Silver"

    def __str__(self):
        return f"{self.name} - {self.item_type} - {self.purity} - {self.weight_troy_oz}oz "

class Platinum(models.Model):
    ITEM_TYPE_CHOICES = (
        ('Round', 'Round'),
        ('Bar', 'Bar'),
        ('Misc', 'Miscellaneous')
    )
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    agw = models.DecimalField(max_digits=10, decimal_places=4)
    purity = models.DecimalField(max_digits=15, decimal_places=6)
    quantity = models.IntegerField()
    weight_troy_oz = models.DecimalField(max_digits=10, decimal_places=4)
    cost_to_purchase = models.DecimalField(max_digits=20, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2)
    coa_present = models.BooleanField(default=False) #Certificate of Authentication
    purchased_from = models.CharField(max_length=100)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Platinum"

    def __str__(self):
        return f"{self.name} - {self.item_type} - {self.purity} - {self.weight_troy_oz}oz "