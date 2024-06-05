from django.forms import ModelForm
from django import forms
from .models import Gold, Silver, Platinum
from decimal import Decimal

class MetalSelectForm(forms.Form):
    METAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('platinum', 'Platinum'),
    ]

class GoldForm(forms.ModelForm):
    weight = forms.DecimalField(max_digits=10, decimal_places=4, required=False, label='Total Weight (Select Units Above)')
    weight_unit = forms.ChoiceField(choices=[('TROY_OUNCES', 'Troy Ounces'), ('GRAMS', 'Grams')], label='Weight Unit')

    class Meta:
        model = Gold
        fields = [
            'metal_type', 'weight_unit', 'item_type', 'item_name', 'item_year',
            'weight', 'quantity', 'purity', 'cost_to_purchase', 'spot_at_purchase', 'shipping_cost',
            'purchased_from', 'featured_image', 'item_about', 'sold_to', 'sell_price'
        ]

        labels = {
            'item_name': 'Item Name',
            'item_about': 'About',
            'spot_at_purchase': 'Spot Price at purchase',
        }

    def __init__(self, *args, **kwargs):
        super(GoldForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        weight = (cleaned_data.get('weight'))
        weight_unit = cleaned_data.get('weight_unit')

        if weight is not None:
            if weight_unit == 'GRAMS':
                cleaned_data['weight_grams'] = weight
                cleaned_data['weight_troy_oz'] = weight / Decimal(31.1035)
            elif weight_unit == 'TROY_OUNCES':
                cleaned_data['weight_troy_oz'] = weight
                cleaned_data['weight_grams'] = weight * Decimal(31.1035)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = self.cleaned_data

        instance.initial_weight_unit = cleaned_data.get('weight_unit')

        if cleaned_data.get('weight'):
            if cleaned_data['weight_unit'] == 'GRAMS':
                instance.weight_grams = Decimal(cleaned_data['weight'])
                instance.weight_troy_oz = Decimal(cleaned_data['weight']) / Decimal(31.1035)
            elif cleaned_data['weight_unit'] == 'TROY_OUNCES':
                instance.weight_troy_oz = Decimal(cleaned_data['weight'])
                instance.weight_grams = Decimal(cleaned_data['weight']) * Decimal(31.1035)

        if commit:
            instance.save()
        return instance

# Repeat similar modifications for SilverForm and PlatinumForm


class SilverForm(forms.ModelForm):
    weight = forms.DecimalField(max_digits=10, decimal_places=4, required=False, label='Total Weight (Select Units Above)')
    weight_unit = forms.ChoiceField(choices=[('TROY_OUNCES', 'Troy Ounces'), ('GRAMS', 'Grams')], label='Weight Unit')

    class Meta:
        model = Silver
        fields = [
            'metal_type', 'weight_unit', 'item_type', 'item_name', 'item_year',
            'weight', 'quantity', 'purity', 'cost_to_purchase', 'spot_at_purchase', 'shipping_cost',
            'purchased_from', 'featured_image', 'item_about', 'sold_to', 'sell_price'
        ]

        labels = {
            'item_name': 'Item Name',
            'item_about': 'About',
            'spot_at_purchase': 'Spot Price at purchase',
        }

    def __init__(self, *args, **kwargs):
        super(SilverForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        weight = (cleaned_data.get('weight'))
        weight_unit = cleaned_data.get('weight_unit')

        if weight is not None:
            if weight_unit == 'GRAMS':
                cleaned_data['weight_grams'] = weight
                cleaned_data['weight_troy_oz'] = weight / Decimal(31.1035)
            elif weight_unit == 'TROY_OUNCES':
                cleaned_data['weight_troy_oz'] = weight
                cleaned_data['weight_grams'] = weight * Decimal(31.1035)

        print(cleaned_data['weight_troy_oz'])
        print(cleaned_data['weight_grams'])

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = self.cleaned_data

        instance.initial_weight_unit = cleaned_data.get('weight_unit')

        if cleaned_data.get('weight'):
            if cleaned_data['weight_unit'] == 'GRAMS':
                instance.weight_grams = cleaned_data['weight']
                instance.weight_troy_oz = cleaned_data['weight'] / Decimal(31.1035)
            elif cleaned_data['weight_unit'] == 'TROY_OUNCES':
                instance.weight_troy_oz = cleaned_data['weight']
                instance.weight_grams = cleaned_data['weight'] * Decimal(31.1035)
        
        if commit:
            instance.save()
        return instance


class PlatinumForm(forms.ModelForm):
    weight = forms.DecimalField(max_digits=10, decimal_places=4, required=False, label='Total Weight (Select Units Above)')
    weight_unit = forms.ChoiceField(choices=[('TROY_OUNCES', 'Troy Ounces'), ('GRAMS', 'Grams')], label='Weight Unit')

    class Meta:
        model = Platinum
        fields = [
            'metal_type', 'weight_unit', 'item_type', 'item_name', 'item_year',
            'weight', 'quantity', 'purity', 'cost_to_purchase', 'spot_at_purchase', 'shipping_cost',
            'purchased_from', 'featured_image', 'item_about', 'sold_to', 'sell_price'
        ]

        labels = {
            'item_name': 'Item Name',
            'item_about': 'About',
            'spot_at_purchase': 'Spot Price at purchase',
        }

    def __init__(self, *args, **kwargs):
        super(PlatinumForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        weight = (cleaned_data.get('weight'))
        weight_unit = cleaned_data.get('weight_unit')

        if weight is not None:
            if weight_unit == 'GRAMS':
                cleaned_data['weight_grams'] = weight
                cleaned_data['weight_troy_oz'] = weight / Decimal(31.1035)
            elif weight_unit == 'TROY_OUNCES':
                cleaned_data['weight_troy_oz'] = weight
                cleaned_data['weight_grams'] = weight * Decimal(31.1035)

        print(cleaned_data['weight_troy_oz'])
        print(cleaned_data['weight_grams'])
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = self.cleaned_data

        instance.initial_weight_unit = cleaned_data.get('weight_unit')

        if cleaned_data.get('weight'):
            if cleaned_data['weight_unit'] == 'GRAMS':
                instance.weight_grams = cleaned_data['weight']
                instance.weight_troy_oz = cleaned_data['weight'] / Decimal(31.1035)
            elif cleaned_data['weight_unit'] == 'TROY_OUNCES':
                instance.weight_troy_oz = cleaned_data['weight']
                instance.weight_grams = cleaned_data['weight'] * Decimal(31.1035)
        
        if commit:
            instance.save()
        return instance
