from rest_framework import viewsets, status 
from apps.auction.serializers import (AuctionListSerializer, AuctionWriteSerializer, 
                                      AuctionDetailSerializer, BidSerializer)
from apps.auction.models import Auction 
from apps.auction.permissions import IsOwnerOrAdminAuction
from rest_framework.decorators import action 
from apps.auction.services import AuctionService
from rest_framework.response import Response

class AuctionViewSet(viewsets.ModelViewSet):

    permission_classes = [IsOwnerOrAdminAuction] 

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
    
    @action(detail=True, methods=['post'])
    def place_bid(self, request, pk=None):
        bid = AuctionService.place_bid(auction_id=pk, user=request.user, bid_price=request.data['bid_price'])
        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED) 

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        AuctionService.close_auction(auction_id=pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def store_bid_history(self, request, pk=None):
        AuctionService.get_auction_bid_history(auction_id=pk)
        return Response(status=status.HTTP_200_OK)