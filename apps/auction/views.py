from rest_framework import viewsets 
from apps.auction.serializers import AuctionListSerializer, AuctionWriteSerializer, AuctionDetailSerializer
from apps.auction.models import Auction 

class AuctionViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        
        if self.action in ["create", "update", "partial_update"]:
            return AuctionWriteSerializer
        elif self.action == "list":
            return AuctionListSerializer
        elif self.action == "retrieve":
            return AuctionDetailSerializer
        return AuctionWriteSerializer
    
    def get_queryset(self):
        return Auction.objects.filter(user=self.request.user)