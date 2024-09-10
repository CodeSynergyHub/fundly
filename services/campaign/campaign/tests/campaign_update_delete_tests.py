import pytest
from django.urls import reverse
from rest_framework import status

from campaign.models import Campaign


@pytest.mark.django_db
def test_campaign_update_success(auth_client, campaign):
    # Define the URL for the update endpoint
    url = reverse('campaign:campaign_ud', kwargs={'pk': campaign.pk})

    # Define the update data
    data = {
        'title': 'Updated Title',
        'description': 'Updated Description',
        'goal_amount': 200
    }

    # Send a PUT request
    response = auth_client.put(url, data, format='json')

    # Assert status code and response data
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Campaign updated successfully'

    # Verify the Campaign was updated in the database
    campaign.refresh_from_db()
    assert campaign.title == 'Updated Title'
    assert campaign.description == 'Updated Description'
    assert campaign.goal_amount == 200


@pytest.mark.django_db
def test_campaign_update_not_found(auth_client):
    # Define a non-existing campaign ID
    non_existing_campaign_id = 999

    # Define the URL for the update endpoint
    url = reverse('campaign:campaign_ud', kwargs={'pk': non_existing_campaign_id})

    # Define the update data
    data = {
        'title': 'Updated Title'
    }

    # Send a PUT request
    response = auth_client.put(url, data, format='json')

    # Assert status code and response data
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Campaign matches the given query.'


@pytest.mark.django_db
def test_campaign_update_invalid_data(auth_client, campaign):
    # Define the URL for the update endpoint
    url = reverse('campaign:campaign_ud', kwargs={'pk': campaign.pk})

    # Define the update data with invalid 'goal_amount'
    data = {
        'goal_amount': -100  # Invalid data
    }

    # Send a PUT request
    response = auth_client.put(url, data, format='json')

    # Assert status code and response data
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'goal_amount' in response.data['message']


@pytest.mark.django_db
def test_campaign_update_creator_permission(secondary_auth_client, campaign):
    # Define the URL for the update endpoint
    url = reverse('campaign:campaign_ud', kwargs={'pk': campaign.pk})

    # Define the update data with invalid 'goal_amount'
    data = {
        'goal_amount': 1000  # Invalid data
    }

    # Send a PUT request
    response = secondary_auth_client.put(url, data, format='json')

    # Assert status code and response data
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == 'You do not have permission to perform this action.'


@pytest.mark.django_db
def test_campaign_delete_success(auth_client, campaign):
    # Define the URL for the delete endpoint
    url = reverse('campaign:campaign_ud', kwargs={'pk': campaign.pk})

    # Send a DELETE request
    response = auth_client.delete(url)

    # Assert status code and response data
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Campaign deleted successfully'

    # Verify the Campaign was deleted from the database
    assert Campaign.objects.count() == 0


@pytest.mark.django_db
def test_campaign_delete_not_found(auth_client):
    # Define a non-existing campaign ID
    non_existing_campaign_id = 999

    # Define the URL for the delete endpoint
    url = reverse('campaign:campaign_ud', kwargs={'pk': non_existing_campaign_id})

    # Send a DELETE request
    response = auth_client.delete(url)

    # Assert status code and response data
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Campaign matches the given query.'


@pytest.mark.django_db
def test_campaign_delete_creator_permission(secondary_auth_client, campaign):
    # Define the URL for the update endpoint
    url = reverse('campaign:campaign_ud', kwargs={'pk': campaign.pk})

    # Send a PUT request
    response = secondary_auth_client.delete(url)

    # Assert status code and response data
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == 'You do not have permission to perform this action.'