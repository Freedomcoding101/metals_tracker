# Generated by Django 5.0.4 on 2024-04-12 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_rename_agw_silver_agw'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gold',
            old_name='agw',
            new_name='AGW',
        ),
        migrations.RenameField(
            model_name='platinum',
            old_name='agw',
            new_name='APW',
        ),
        migrations.RenameField(
            model_name='silver',
            old_name='AGW',
            new_name='ASW',
        ),
    ]