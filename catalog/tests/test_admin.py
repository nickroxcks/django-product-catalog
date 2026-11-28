"""Admin tests: pages render, counts are correct, and list views avoid N+1 queries."""

from decimal import Decimal

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from catalog.models import Category, Product

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("model", ["category", "tag", "product"])
@pytest.mark.parametrize("view", ["changelist", "add"])
def test_admin_pages_render(admin_client, model, view):
    """Every catalog admin list and add page loads for a superuser."""
    response = admin_client.get(reverse(f"admin:catalog_{model}_{view}"))
    assert response.status_code == 200


def test_category_changelist_shows_product_counts(admin_client, product):
    """The annotated count is right, including 0 for a category with no products."""
    Category.objects.create(name="Plumbing")
    response = admin_client.get(reverse("admin:catalog_category_changelist"))
    counts = {c.name: c.product_count for c in response.context["cl"].result_list}
    assert counts == {"Electrical": 1, "Plumbing": 0}


def test_tag_changelist_shows_product_count(admin_client, product, tag):
    """Tag counts come through the M2M join table."""
    product.tags.add(tag)
    response = admin_client.get(reverse("admin:catalog_tag_changelist"))
    [row] = response.context["cl"].result_list
    assert row.product_count == 1


def _add_products(category: Category, start: int, count: int) -> None:
    Product.objects.bulk_create(
        Product(
            name=f"Product {i}",
            sku=f"SKU-{i:03d}",
            description="x",
            price=Decimal("1.00"),
            category=category,
        )
        for i in range(start, start + count)
    )


def _changelist_query_count(client) -> int:
    with CaptureQueriesContext(connection) as ctx:
        response = client.get(reverse("admin:catalog_product_changelist"))
    assert response.status_code == 200
    return len(ctx.captured_queries)


def test_product_changelist_query_count_is_constant(admin_client, category):
    """N+1 guard: 10x the rows must not mean more queries."""
    _add_products(category, start=0, count=1)
    with_one = _changelist_query_count(admin_client)
    _add_products(category, start=1, count=9)
    with_ten = _changelist_query_count(admin_client)
    assert with_ten == with_one
