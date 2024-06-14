# Generated by Django 5.0.6 on 2024-06-13 01:47

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tracker', '0038_gold_weight_per_unit_platinum_weight_per_unit_and_more'),
        ('users', '0003_rename_owener_review_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold',
            name='sell_price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='gold',
            name='sold_to',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='platinum',
            name='sell_price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='platinum',
            name='sold_to',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='silver',
            name='sell_price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='silver',
            name='sold_to',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sell_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sell_quantity', models.DecimalField(decimal_places=2, max_digits=30)),
                ('sold_to', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('date_sold', models.DateField(auto_now_add=True)),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]