from django.urls import reverse
from rest_framework import status

from campaign.models import Campaign
import pytest


@pytest.mark.django_db
def test_campaign_retrieve_success(api_client, campaign):
    # Define the URL for the retrieve endpoint
    url = reverse('campaign:campaign_detail', kwargs={'pk': campaign.pk})

    # Send a GET request
    response = api_client.get(url)

    # Assert status code and response data
    assert response.status_code == status.HTTP_200_OK
    assert response.data['data']['title'] == 'Test Campaign'
    assert response.data['data']['description'] == 'Description of test campaign'
    assert response.data['data']['goal_amount'] == 1000
    assert response.data['data']['start_date'] == '2024-01-01'
    assert response.data['data']['end_date'] == '2024-12-31'


@pytest.mark.django_db
def test_campaign_retrieve_not_found(api_client):
    # Define a non-existing campaign ID
    non_existing_campaign_id = 999

    # Define the URL for the retrieve endpoint
    url = reverse('campaign:campaign_detail', kwargs={'pk': non_existing_campaign_id})

    # Send a GET request
    response = api_client.get(url)

    # Assert status code and response data
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Campaign matches the given query.'


