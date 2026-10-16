from django.conf import settings
from django.db import models
from django.db.models import Sum
from .models import Product
import uuid


class Order(models.Model):
    order_number = models.CharField(editable=False, max_length=32, null=False)
    full_name = models.CharField(blank=False, max_length=50, null=False)
    email = models.EmailField(blank=False, max_length=254, null=False)
    phone_number = models.CharField(blank=False, max_length=20, null=False)
    country = models.CharField(blank=False, max_length=40, null=False)
    postcode = models.CharField(blank=True, max_length=20, null=True)
    town_or_city = models.CharField(blank=False, max_length=40, null=False)
    street_address1 = models.CharField(blank=False, max_length=80, null=False)
    street_address2 = models.CharField(blank=True, max_length=80, null=True)
    county = models.CharField(blank=True, max_length=80, null=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        decimal_places=2, default=0, max_digits=6, null=False
    )
    order_total = models.DecimalField(
        decimal_places=2, default=0, max_digits=10, null=False
    )
    grand_total = models.DecimalField(
        decimal_places=2, default=0, max_digits=10, null=False
    )


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    product_size = models.CharField(blank=True, max_length=2, null=True)
    quantity = models.IntegerField(blank=False, default=0, null=False)
    lineitem_total = models.DecimalField(
        blank=False, decimal_places=2, editable=False, max_digits=6, null=False
    )
