from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    photo_id = models.TextField(help_text="Телеграмм id фото товара", null=True)
    name = models.CharField(max_length=160, help_text="Название товара", null=True)
    description = models.TextField(help_text="Описание товара", null=True)
    price = models.IntegerField(help_text="Цена товара", verbose_name="Цена товара", null=True)
    category = models.CharField(max_length=160, verbose_name="Категория товара", null=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=160, help_text="Название категории")


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(help_text="Телеграмм id пользователя")
    inviter_id = models.IntegerField(help_text="Телеграмм id приглашателя(реферала)", default=0, null=True)
    invited_users = models.TextField(help_text="Приглашенные пользователи", null=True)
    money = models.IntegerField(help_text="Баланс пользователя", default=0, auto_created=True)


class RefPercent(models.Model):
    percent = models.IntegerField(help_text="Реферальный процент с покупок")
