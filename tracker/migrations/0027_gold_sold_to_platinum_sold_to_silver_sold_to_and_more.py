# Generated by Django 5.0.6 on 2024-05-28 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0026_alter_gold_item_about_alter_platinum_item_about_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='sold_to',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='platinum',
            name='sold_to',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='silver',
            name='sold_to',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gold',
            name='item_about',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='gold',
            name='sell_price',
            field=models.DecimalField(blank=True, decimal_places=2, default='', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='platinum',
            name='item_about',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='silver',
            name='item_about',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
    ]
