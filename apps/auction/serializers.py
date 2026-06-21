from rest_framework import serializers
from apps.auction.models import Auction, Bid 
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username']

class AuctionWriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'starting_price', 'start_time', 'end_time', 'user']
        
class AuctionDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'current_price', 'starting_price', 'start_time', 'end_time', 'user']
        
class AuctionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'title', 'current_price']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid  
        fields = ['user', 'auction', 'bid_price', 'created_at']