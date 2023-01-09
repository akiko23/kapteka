# Generated by Django 4.1.5 on 2023-01-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_alter_user_inviter_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='invited_users',
            field=models.TextField(help_text='Приглашенные пользователи', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(help_text='Цена товара', null=True, verbose_name='Цена товара'),
        ),
    ]
