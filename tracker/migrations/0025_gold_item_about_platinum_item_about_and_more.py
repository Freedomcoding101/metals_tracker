# Generated by Django 5.0.6 on 2024-05-27 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0024_gold_item_year_platinum_item_year_silver_item_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='item_about',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='platinum',
            name='item_about',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='silver',
            name='item_about',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='platinum',
            name='featured_image',
            field=models.ImageField(blank=True, default='images/platinum_avatar.jpg', null=True, upload_to=''),
        ),
    ]