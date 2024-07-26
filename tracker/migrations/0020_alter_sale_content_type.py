# Generated by Django 5.0.6 on 2024-07-21 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tracker', '0019_alter_sale_profit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
    ]