# Generated by Django 4.0.4 on 2022-04-23 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_address_category_color_product_size_productattribute_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='specs',
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(max_length=255),
        ),
    ]
