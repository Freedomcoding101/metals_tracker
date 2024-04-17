# Generated by Django 5.0.4 on 2024-04-15 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0010_rename_name_gold_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='metal_type',
            field=models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver'), ('platinum', 'Platinum')], default='', max_length=100),
        ),
        migrations.AddField(
            model_name='platinum',
            name='metal_type',
            field=models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver'), ('platinum', 'Platinum')], default='', max_length=100),
        ),
        migrations.AddField(
            model_name='silver',
            name='metal_type',
            field=models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver'), ('platinum', 'Platinum')], default='', max_length=100),
        ),
    ]