# Generated by Django 4.1.5 on 2023-01-07 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_user_invited_users_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefPercent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(help_text='Реферальный процент с покупок')),
            ],
        ),
    ]