import pytest
from apps.auction.models import Auction
from django.utils import timezone
from datetime import datetime, timedelta
from apps.accounts.tests.factories import UserFactory

@pytest.mark.django_db(transaction=True)
def test_user_can_create_auction(active_user, auth_client):
    data = {
        "title": "Macbook Pro",
        "description": "Highest quality",
        "starting_price": "1000",
        "current_price": "1000",
        "end_time": "2026-06-26T09:00:00Z",
        "start_time": "2026-06-22T15:00:00Z",
    }

    response = auth_client.post("/api/v1/auctions/", data, format="json")

    assert response.status_code == 201
    assert Auction.objects.filter(title="Macbook Pro", user=active_user).exists()

@pytest.mark.django_db(transaction=True)
def test_only_owner_can_update_auction(user, api_client):
    auction = Auction.objects.create(
        title="Macbook Pro",
        description="Highest quality",
        starting_price=1000,
        current_price=1000,
        end_time = timezone.make_aware(datetime(2026, 6, 26, 15, 0, 0)),
        start_time = timezone.make_aware(datetime(2026, 6, 22, 15, 0, 0)),
        user=user 
    )

    response = api_client.patch(f"/api/v1/auctions/{auction.id}/", {"title": "Hacked Title"}, format="json")

    assert response.status_code == 403

@pytest.mark.django_db(transaction=True)
def test_bid_must_be_higher_than_current_price(active_user, auth_client):
    auction = Auction.objects.create(
        title="Macbook Pro",
        description="Highest quality",
        starting_price=1000,
        current_price=1000,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(days=3),
        user=active_user,
        status="active"
    )

    data = {
        "auction": auction.id,
        "bid_price": "500",  
    }

    response = auth_client.post(f"/api/v1/auctions/{auction.id}/place_bid/", data, format="json")

    assert response.status_code == 400

@pytest.mark.django_db(transaction=True)
def test_bid_must_be_higher_than_current_price(active_user, auth_client):
    seller = UserFactory()  
    auction = Auction.objects.create(
        title="Macbook Pro",
        description="Highest quality",
        starting_price=1000,
        current_price=1000,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(days=3),
        user=seller,
        status="active"
    )

    data = {
        "auction": auction.id,
        "bid_price": "500",  
    }

    response = auth_client.post(f"/api/v1/auctions/{auction.id}/place_bid/", data, format="json")

    assert response.status_code == 400