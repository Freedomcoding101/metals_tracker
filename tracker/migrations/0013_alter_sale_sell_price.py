# Generated by Django 5.0.6 on 2024-07-17 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0012_alter_sale_date_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sell_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
