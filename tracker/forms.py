from django.forms import ModelForm
from django import forms
from .models import Gold, Silver, Platinum

class MetalSelectForm(forms.Form):
    METAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('platinum', 'Platinum'),
    ]

class GoldForm(forms.ModelForm):
    class Meta:
        model = Gold
        fields = "__all__"

#  the code below changes the class of the field items to input
#  so the css works.
    def __init__(self,*args, **kwargs):
        super(GoldForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class SilverForm(forms.ModelForm):
    class Meta:
        model = Silver
        fields = "__all__"

#  the code below changes the class of the field items to input
#  so the css works.
    def __init__(self,*args, **kwargs):
        super(SilverForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class PlatinumForm(forms.ModelForm):
    class Meta:
        model = Platinum
        fields = "__all__"

#  the code below changes the class of the field items to input
#  so the css works.
    def __init__(self,*args, **kwargs):
        super(PlatinumForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})