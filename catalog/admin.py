"""Admin configuration for the catalog models."""

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from catalog.models import Category, Product, Tag


class ProductCountMixin:
    """Adds a "Products" column computed in one grouped query, not one COUNT per row."""

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(product_count=Count("products"))

    @admin.display(description="Products", ordering="product_count")
    def product_count(self, obj) -> int:
        return obj.product_count


@admin.register(Category)
class CategoryAdmin(ProductCountMixin, admin.ModelAdmin):
    list_display = ("name", "product_count")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(ProductCountMixin, admin.ModelAdmin):
    list_display = ("name", "product_count")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "updated_at")
    # Join only category for the list column (Django's fallback is a bare
    # select_related(), which follows every non-null FK).
    list_select_related = ("category",)
    list_filter = ("category", "tags")
    search_fields = ("name", "sku", "description")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at")
