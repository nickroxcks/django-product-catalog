from decimal import Decimal

import pytest

from catalog.models import Category, Product, Tag


@pytest.fixture
def category(db):
    return Category.objects.create(name="Electrical")


@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Outdoor")


@pytest.fixture
def product(category):
    return Product.objects.create(
        name="14/2 NMD90 Cable",
        sku="ELEC-001",
        description="75m coil",
        price=Decimal("89.99"),
        category=category,
    )
