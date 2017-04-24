from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class Topping(models.Model):
    title = models.CharField(max_length=20)


class Pizza(models.Model):
    title = models.CharField(max_length=30)
    toppings = models.ManyToManyField(Topping)