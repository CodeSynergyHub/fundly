import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
def test_campaign_list_success(api_client, campaigns):
    url = reverse('campaign:campaign_list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['data']) == len(campaigns)  # Ensure all campaigns are returned

    titles = [campaign['title'] for campaign in response.data['data']]
    assert 'Campaign 1' in titles
    assert 'Campaign 2' in titles
    assert 'Another Campaign' in titles


@pytest.mark.django_db
def test_campaign_list_search(api_client, campaigns):
    url = reverse('campaign:campaign_list') + '?title=Campaign 1'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['data']) == 1  # Only one campaign should match

    assert response.data['data'][0]['title'] == 'Campaign 1'


@pytest.mark.django_db
def test_campaign_list_no_results(api_client):
    url = reverse('campaign:campaign_list') + '?title=Non-Existent Campaign'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['data']) == 0  # No campaigns should match


@pytest.mark.django_db
def test_campaign_list_server_error(api_client, mocker):
    # Mock an exception in the view to test server error handling
    mocker.patch('campaign.views.CampaignListSearchAPIView.get_queryset', side_effect=Exception('Server error'))

    url = reverse('campaign:campaign_list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data['message'] == 'Server error'
