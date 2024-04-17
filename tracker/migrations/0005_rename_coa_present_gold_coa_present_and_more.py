# Generated by Django 5.0.4 on 2024-04-12 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_rename_agw_gold_agw_rename_agw_platinum_apw_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gold',
            old_name='coa_present',
            new_name='COA_PRESENT',
        ),
        migrations.RenameField(
            model_name='platinum',
            old_name='coa_present',
            new_name='COA_PRESENT',
        ),
        migrations.RenameField(
            model_name='silver',
            old_name='coa_present',
            new_name='COA_PRESENT',
        ),
        migrations.RemoveField(
            model_name='platinum',
            name='APW',
        ),
        migrations.AddField(
            model_name='platinum',
            name='APtW',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='gold',
            name='AGW',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='gold',
            name='sell_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='platinum',
            name='sell_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='silver',
            name='ASW',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='silver',
            name='sell_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]