from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(blank=True, max_length=254, null=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category', blank=True, null=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(blank=True, max_length=254, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    rating = models.DecimalField(
        blank=True, decimal_places=2, max_digits=6, null=True
    )
    image_url = models.URLField(blank=True, max_length=1024, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name
