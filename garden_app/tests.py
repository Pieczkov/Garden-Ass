
import pytest
from django.test import Client
from django.urls import reverse




@pytest.mark.django_db
def test_index():
    client = Client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert 'Assistant Gardeners' in str(response.content)


# @pytest.mark.django_db
# def test_index():
#     client = Client()
#     url = 'add_unit'
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'Add unit' in str(response.content)
