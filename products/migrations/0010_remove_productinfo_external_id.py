# Generated by Django 4.2.1 on 2023-05-12 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_orderitem_orderitem_unique_order_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinfo',
            name='external_id',
        ),
    ]
