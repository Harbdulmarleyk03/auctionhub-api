from django.db import transaction
from apps.auction.models import Auction, Bid
from django.core.exceptions import ValidationError
from django.utils import timezone

class AuctionService:

    @staticmethod
    def place_bid(auction_id, user, bid_price):
        with transaction.atomic():
            auction = Auction.objects.select_for_update().get(id=auction_id)
            if auction.user == user:
                raise ValidationError("Auction owner cannot bid their own auction")
            if auction.status != "active" or auction.end_time < timezone.now():
               raise ValidationError("Auction is not opened for bidding")
            if bid_price <= auction.current_price:
                raise ValidationError("Bid must be higher than current price.")
            bid = Bid.objects.create(auction=auction, user=user, bid_price=bid_price)
            auction.current_price = bid_price
            auction.save()
        return bid 
        
    @staticmethod
    def close_auction(auction_id):
        with transaction.atomic():
            auction = Auction.objects.select_for_update().get(id=auction_id)
            if auction.status != "active":
                return 
            if auction.end_time > timezone.now():
                return 
            highest_bid = auction.bids.order_by('bid_price').first()
            if highest_bid:
                auction.winner = highest_bid.user
            auction.status = "completed"
            auction.save()

    @staticmethod
    def get_auction_bid_history(auction_id):
        return Bid.objects.filter(auction_id=auction_id).order_by('created_at')