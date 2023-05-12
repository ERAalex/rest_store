# Generated by Django 4.2.1 on 2023-05-12 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=80, verbose_name='Модель')),
                ('external_id', models.PositiveIntegerField(verbose_name='Внешний ИД')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('price_rrc', models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_infos', to='products.product', verbose_name='Продукт')),
                ('shop', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_infos', to='products.shop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Информация о продукте',
                'verbose_name_plural': 'Информационный список о продуктах',
            },
        ),
        migrations.AddConstraint(
            model_name='productinfo',
            constraint=models.UniqueConstraint(fields=('product', 'shop', 'external_id'), name='unique_product_info'),
        ),
    ]
