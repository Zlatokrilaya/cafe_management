# Generated by Django 5.1.6 on 2025-03-07 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.TextField(),
        ),
    ]
