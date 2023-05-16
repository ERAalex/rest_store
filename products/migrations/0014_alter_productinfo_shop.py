# Generated by Django 4.2.1 on 2023-05-15 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_productinfo_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='shop',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_info', to='products.shop', verbose_name='Магазин'),
        ),
    ]