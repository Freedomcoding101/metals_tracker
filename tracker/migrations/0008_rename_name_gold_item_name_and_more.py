# Generated by Django 5.0.4 on 2024-04-12 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_remove_gold_item_type_remove_platinum_item_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gold',
            old_name='name',
            new_name='item_name',
        ),
        migrations.RenameField(
            model_name='platinum',
            old_name='name',
            new_name='item_name',
        ),
        migrations.RenameField(
            model_name='silver',
            old_name='name',
            new_name='item_name',
        ),
        migrations.RemoveField(
            model_name='gold',
            name='COA_PRESENT',
        ),
        migrations.RemoveField(
            model_name='platinum',
            name='COA_PRESENT',
        ),
        migrations.RemoveField(
            model_name='silver',
            name='COA_PRESENT',
        ),
    ]
