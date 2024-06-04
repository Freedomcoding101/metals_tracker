# Generated by Django 5.0.6 on 2024-05-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0023_alter_gold_featured_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='item_year',
            field=models.PositiveIntegerField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='platinum',
            name='item_year',
            field=models.PositiveIntegerField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='silver',
            name='item_year',
            field=models.PositiveIntegerField(blank=True, default=None, max_length=30, null=True),
        ),
    ]