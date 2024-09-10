import pytest
from rest_framework import status
from django.urls import reverse
from campaign.models import Campaign



@pytest.mark.django_db
def test_create_campaign(auth_client, user):
    url = reverse('campaign:create_campaign')  # Ensure this matches your URL name
    data = {
        'title': 'New Campaign',
        'description': 'Description of the campaign',
        'goal_amount': 1000,
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
    }

    response = auth_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['message'] == 'Campaign created successfully'

    # Verify the Campaign was created in the database
    assert Campaign.objects.count() == 1
    campaign = Campaign.objects.first()
    assert campaign.title == 'New Campaign'
    assert campaign.description == 'Description of the campaign'
    assert campaign.goal_amount == 1000
    assert str(campaign.start_date) == '2024-01-01'
    assert str(campaign.end_date) == '2024-12-31'
    assert campaign.creator_id == user.id


@pytest.mark.django_db
def test_create_campaign_without_auth(api_client):
    url = reverse('campaign:create_campaign')  # Ensure this matches your URL name
    data = {
        'title': 'Unauthorized Campaign',
        'description': 'This should fail',
        'goal_amount': 500,
        'start_date': '2024-02-01',
        'end_date': '2024-11-30',
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'message' in response.data
    assert response.data['message'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_create_campaign_invalid_data(auth_client, user):
    url = reverse('campaign:create_campaign')  # Ensure this matches your URL name
    data = {
        'title': '',  # Invalid data
        'description': 'Description with missing title',
        'goal_amount': -100,  # Invalid goal amount
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
    }

    response = auth_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'message' in response.data
    assert 'title' in response.data['message']
    assert 'goal_amount' in response.data['message']
