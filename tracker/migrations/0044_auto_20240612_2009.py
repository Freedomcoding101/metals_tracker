from django.db import migrations, models
import uuid
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0039_remove_gold_date_sold_remove_gold_sell_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sell_quantity', models.DecimalField(decimal_places=2, max_digits=30)),
                ('sold_to', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('date_sold', models.DateField(blank=True, null=True)),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, serialize=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]