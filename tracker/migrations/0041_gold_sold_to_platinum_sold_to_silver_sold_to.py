# Generated by Django 5.0.6 on 2024-06-12 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0040_gold_sell_price_platinum_sell_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='sold_to',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='platinum',
            name='sold_to',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='silver',
            name='sold_to',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
    ]