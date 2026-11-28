"""Catalog models: Category, Tag, Product.

Primary keys: no model declares one, so Django adds an auto-incrementing `id`
(BigAutoField, from DEFAULT_AUTO_FIELD in config/settings.py) to each.
"""

from django.db import models
from django.db.models import Q, UniqueConstraint
from django.db.models.functions import Lower


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="unique_category_name_ci",
                violation_error_message="A category with this case-insensitive name already exists",
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="unique_tag_name_ci",
                violation_error_message="A tag with this name already exists (case-insensitive).",
            )
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    # its possible names could be the same for products. Don't use unique here
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    # Use PROTECT as deleting a category must not silently delete its products.
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="product_price_non_negative")
        ]

    def __str__(self):
        return self.name
