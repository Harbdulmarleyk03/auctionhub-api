from rest_framework import viewsets, status
from apps.auction.serializers import (AuctionListSerializer, AuctionWriteSerializer,
                                      AuctionDetailSerializer, BidSerializer)
from apps.auction.models import Auction
from apps.auction.permissions import IsOwnerOrAdminAuction
from rest_framework.decorators import action
from apps.auction.services import AuctionService
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


@extend_schema_view(
    list=extend_schema(
        summary="List my auctions",
        description="Returns all auctions belonging to the currently authenticated user.",
        responses={200: AuctionListSerializer(many=True)},
        tags=["Auctions"],
    ),
    retrieve=extend_schema(
        summary="Get auction details",
        description="Returns full details of a single auction owned by the authenticated user.",
        responses={200: AuctionDetailSerializer},
        tags=["Auctions"],
    ),
    create=extend_schema(
        summary="Create an auction",
        description="Creates a new auction. The authenticated user is automatically set as the owner.",
        request=AuctionWriteSerializer,
        responses={201: AuctionWriteSerializer},
        tags=["Auctions"],
    ),
    update=extend_schema(
        summary="Update an auction",
        description="Fully updates an existing auction. Only the owner or admin can do this.",
        request=AuctionWriteSerializer,
        responses={200: AuctionWriteSerializer},
        tags=["Auctions"],
    ),
    partial_update=extend_schema(
        summary="Partially update an auction",
        description="Updates one or more fields of an existing auction.",
        request=AuctionWriteSerializer,
        responses={200: AuctionWriteSerializer},
        tags=["Auctions"],
    ),
    destroy=extend_schema(
        summary="Delete an auction",
        description="Deletes an auction. Only the owner or admin can perform this action.",
        responses={204: None},
        tags=["Auctions"],
    ),
)
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Place a bid on an auction",
        description=(
            "Places a bid on the specified auction. "
            "The bid price must be higher than the current highest bid. "
            "Returns the created bid on success."
        ),
        request=BidSerializer,
        responses={
            201: BidSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Valid bid",
                value={"bid_price": "250.00"},
                request_only=True,
            ),
            OpenApiExample(
                "Bid too low",
                value={"error": ["Bid price must be higher than the current highest bid."]},
                response_only=True,
                status_codes=["400"],
            ),
        ],
        tags=["Auctions"],
    )
    @action(detail=True, methods=['post'])
    def place_bid(self, request, pk=None):
        try:
            bid = AuctionService.place_bid(
                auction_id=pk, user=request.user, bid_price=request.data['bid_price']
            )
            return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Close an auction",
        description=(
            "Closes the specified auction, preventing any further bids. "
            "Only the owner or admin can close an auction."
        ),
        request=None,
        responses={200: None},
        tags=["Auctions"],
    )
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        AuctionService.close_auction(auction_id=pk)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary="Get bid history for an auction",
        description="Returns the full bid history for the specified auction.",
        responses={
            200: BidSerializer(many=True),
        },
        tags=["Auctions"],
    )
    @action(detail=True, methods=['get'])
    def store_bid_history(self, request, pk=None):
        AuctionService.get_auction_bid_history(auction_id=pk)
        return Response(BidSerializer(many=True), status=status.HTTP_200_OK)