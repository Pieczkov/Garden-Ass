
import pytest
from django.test import Client
from django.urls import reverse

from garden_app.models import Unit


@pytest.mark.django_db
def test_index():
    client = Client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Assistant Gardeners' in str(response.content)


@pytest.mark.django_db
def test_add_unit_get():
    client = Client()
    url = reverse('add_unit')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Add unit' in str(response.content)


@pytest.mark.django_db
def test_add_unit_post():
    client = Client()
    url = reverse('add_unit')
    data = {"name": "baba"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(url)
    # assert Unit.objects.get(name='baba')


