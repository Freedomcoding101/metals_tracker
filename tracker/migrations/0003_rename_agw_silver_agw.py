# Generated by Django 5.0.4 on 2024-04-12 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_gold_created_platinum_created_silver_created_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='silver',
            old_name='agw',
            new_name='AGW',
        ),
    ]
