"""The committed sample-data fixture must load cleanly against the current models."""

import pytest
from django.core.management import call_command

from catalog.models import Category, Product, Tag

pytestmark = pytest.mark.django_db


def test_sample_data_fixture_loads():
    """Catches a fixture that drifts out of sync with a model or constraint change."""
    call_command("loaddata", "sample_data", verbosity=0)

    # Minimums rather than exact counts, so adding sample rows doesn't break the test.
    assert Category.objects.count() >= 5
    assert Tag.objects.count() >= 10
    assert Product.objects.count() >= 20
    assert not Product.objects.filter(tags__isnull=True).exists()
