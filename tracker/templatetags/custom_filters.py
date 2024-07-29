from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def subtract(value, arg):
    return Decimal(value) - Decimal(arg)

@register.filter
def absolute(value):
    return abs(value)

@register.filter
def divide(value, arg):
    return Decimal(value) / Decimal(arg)

@register.filter
def multiply(value, arg):
    return Decimal(value) * Decimal(arg)