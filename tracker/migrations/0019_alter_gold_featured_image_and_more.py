# Generated by Django 5.0.4 on 2024-04-17 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0018_alter_gold_featured_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold',
            name='featured_image',
            field=models.ImageField(blank=True, default='gold_avatar.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='platinum',
            name='featured_image',
            field=models.ImageField(blank=True, default='platinum_avatar.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='silver',
            name='featured_image',
            field=models.ImageField(blank=True, default='silver_avatar.jpg', null=True, upload_to=''),
        ),
    ]