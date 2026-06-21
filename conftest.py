import pytest 
from rest_framework.test import APIClient 
from apps.accounts.tests.factories import UserFactory
from apps.auction.tests.factories import AuctionFactory, BidFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def active_user():
    return UserFactory(is_active=True)

@pytest.fixture
def auth_client(active_user):
    client = APIClient()
    client.force_authenticate(user=active_user)
    return client

@pytest.fixture
def auction():
    return AuctionFactory()

@pytest.fixture
def bid():
    return BidFactory()
