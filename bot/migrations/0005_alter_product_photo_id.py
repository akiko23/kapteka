# Generated by Django 4.1.5 on 2023-01-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_alter_product_category_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo_id',
            field=models.TextField(help_text='Телеграмм id фото товара', null=True),
        ),
    ]
