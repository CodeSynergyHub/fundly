from datetime import datetime, timedelta
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import jwt

from campaign.models import Campaign


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def auth_client(api_client, user):
    # Define the token expiration time
    expire = datetime.now() + timedelta(minutes=60)

    # Define the payload (data contained in the token)
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': expire,  # Expiration time
        'iat': datetime.now(),  # Issued at time
        'aud': "http://127.0.0.1:8000",
    }

    # Create the JWT token using the secret key and the HS256 algorithm
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    # For Python 3.5+, jwt.encode returns a byte string, so decode it to a string
    # Set the Authorization header
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token if isinstance(token, str) else token.decode('utf-8')}')

    return api_client


@pytest.fixture
def secondary_user():
    return User.objects.create_user(username='testuser2', password='testpassword')


@pytest.fixture
def secondary_auth_client(api_client, secondary_user):
    # Define the token expiration time
    expire = datetime.now() + timedelta(minutes=60)

    # Define the payload (data contained in the token)
    payload = {
        'id': secondary_user.id,
        'username': secondary_user.username,
        'exp': expire,  # Expiration time
        'iat': datetime.now(),  # Issued at time
        'aud': "http://127.0.0.1:8000",
    }

    # Create the JWT token using the secret key and the HS256 algorithm
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    # For Python 3.5+, jwt.encode returns a byte string, so decode it to a string
    # Set the Authorization header
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token if isinstance(token, str) else token.decode('utf-8')}')

    return api_client


@pytest.fixture
def campaign(user):
    return Campaign.objects.create(
        title='Test Campaign',
        description='Description of test campaign',
        goal_amount=1000,
        start_date='2024-01-01',
        end_date='2024-12-31',
        creator_id=user.id
    )


@pytest.fixture
def campaigns():
    return [
        Campaign.objects.create(
            title='Campaign 1',
            description='Description for Campaign 1',
            goal_amount=500,
            start_date='2024-01-01',
            end_date='2024-12-31',
            creator_id=1,
        ),
        Campaign.objects.create(
            title='Campaign 2',
            description='Description for Campaign 2',
            goal_amount=1000,
            start_date='2024-01-01',
            end_date='2024-12-31',
            creator_id=2,
        ),
        Campaign.objects.create(
            title='Another Campaign',
            description='Description for Another Campaign',
            goal_amount=1500,
            start_date='2024-01-01',
            end_date='2024-12-31',
            creator_id=3,
        ),
    ]

