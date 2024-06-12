# Generated by Django 5.0.6 on 2024-06-12 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0039_remove_gold_date_sold_remove_gold_sell_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='sell_price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='platinum',
            name='sell_price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='silver',
            name='sell_price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=20),
        ),
    ]