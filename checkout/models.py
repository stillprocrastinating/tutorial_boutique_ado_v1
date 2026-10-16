from django.conf import settings
from django.db import models
from django.db.models import Sum
from products.models import Product
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

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """

        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added, accounting for delivery costs
        """

        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost

        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number if it hasn't been set already
        """

        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

        def __str__(self):
            return self.order_number


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

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total and update the order total
        """

        self.lineitem_total = self.product.price * self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
