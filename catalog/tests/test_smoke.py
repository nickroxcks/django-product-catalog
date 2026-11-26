"""Smoke tests: the project boots, settings load, and the admin is reachable."""

from django.urls import reverse


def test_admin_login_page_renders(client):
    response = client.get(reverse("admin:login"))
    assert response.status_code == 200
