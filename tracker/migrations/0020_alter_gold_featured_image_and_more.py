# Generated by Django 5.0.4 on 2024-04-18 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0019_alter_gold_featured_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='platinum',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='silver',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
