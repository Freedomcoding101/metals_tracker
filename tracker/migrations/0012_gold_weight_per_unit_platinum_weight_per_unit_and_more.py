# Generated by Django 5.0.4 on 2024-04-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0011_gold_metal_type_platinum_metal_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='weight_per_unit',
            field=models.DecimalField(decimal_places=2, default='', max_digits=10),
        ),
        migrations.AddField(
            model_name='platinum',
            name='weight_per_unit',
            field=models.DecimalField(decimal_places=2, default='', max_digits=10),
        ),
        migrations.AddField(
            model_name='silver',
            name='weight_per_unit',
            field=models.DecimalField(decimal_places=2, default='', max_digits=10),
        ),
        migrations.AlterField(
            model_name='gold',
            name='weight_troy_oz',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
