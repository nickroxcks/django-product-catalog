from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError

from catalog.models import Category, Product, Tag


# This decorator allows db access and the test to be treated as a transaction
@pytest.mark.django_db
def test_duplicate_tag_rejected():
    """Tags differing only by case are rejected by the LOWER(name) unique index."""
    Tag.objects.create(name="red")
    with pytest.raises(IntegrityError), transaction.atomic():
        Tag.objects.create(name="Red")


@pytest.mark.django_db
def test_duplicate_category_fails_full_clean(category):
    """Model validation surfaces the constraint as a friendly error before hitting the DB."""
    with pytest.raises(ValidationError, match="category"):
        Category(name="electrical").full_clean()


@pytest.mark.django_db
def test_valid_tag():
    """Creating two unique tags is accepted."""
    with transaction.atomic():
        Tag.objects.create(name="red")
        Tag.objects.create(name="blue")
        assert Tag.objects.count() == 2


@pytest.mark.django_db
def test_duplicate_category_rejected():
    """Categories differing only by case are rejected by the LOWER(name) unique index."""
    Category.objects.create(name="Color")

    with pytest.raises(IntegrityError), transaction.atomic():
        Category.objects.create(name="color")


@pytest.mark.django_db
def test_valid_category():
    """Creating two unique categories is accepted."""
    with transaction.atomic():
        Category.objects.create(name="Color")
        Category.objects.create(name="Food")
        assert Category.objects.count() == 2


@pytest.mark.django_db
def test_duplicate_sku_rejected(product):
    """A second product with an existing SKU is rejected by the unique constraint."""
    with pytest.raises(IntegrityError), transaction.atomic():
        Product.objects.create(
            name="Other cable",
            sku=product.sku,
            description="x",
            price=Decimal("1.00"),
            category=product.category,
        )


@pytest.mark.django_db
def test_negative_price_rejected(category):
    """Price boundary: -0.01 violates the price >= 0 check constraint."""
    with pytest.raises(IntegrityError), transaction.atomic():
        Product.objects.create(
            name="Bad price",
            sku="BAD-001",
            description="x",
            price=Decimal("-0.01"),
            category=category,
        )


@pytest.mark.django_db
def test_zero_price_allowed(product):
    """Price boundary: 0 satisfies price >= 0."""
    product.price = Decimal("0")
    product.save()
    product.refresh_from_db()
    assert product.price == Decimal("0")


@pytest.mark.django_db
def test_delete_category_with_product_protected(category, product):
    """PROTECT: a category that still has products cannot be deleted."""
    # ProtectedError is raised by Django's deletion collector before any SQL
    # runs, so no atomic() is needed here.
    with pytest.raises(ProtectedError):
        category.delete()
    assert Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_deleting_tag_keeps_product(product, tag):
    """Deleting a tag removes only the M2M join row, not the product."""
    product.tags.add(tag)
    tag.delete()
    assert Product.objects.filter(pk=product.pk).exists()
    assert product.tags.count() == 0


@pytest.mark.django_db
def test_product_no_tag(product):
    """Products are allowed to be created without a tag."""
    assert product.tags.count() == 0


@pytest.mark.django_db
def test_str(category, tag, product):
    """__str__ returns the name (used by the admin and templates)."""
    assert str(product) == "14/2 NMD90 Cable"
    assert str(tag) == "Outdoor"
    assert str(category) == "Electrical"
