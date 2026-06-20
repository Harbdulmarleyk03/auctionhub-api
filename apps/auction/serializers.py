from rest_framework import serializers
from apps.auction.models import Auction

class AuctionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'starting_price', 'start_time', 'end_time']
        
class AuctionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = "__all__"
        
class AuctionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'title', 'current_price']