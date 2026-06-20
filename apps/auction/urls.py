from rest_framework import routers
from apps.auction.views import AuctionViewSet

router = routers.DefaultRouter()
router.register(r'auctions', AuctionViewSet, basename="auctions")
urlpatterns = router.urls 

urlpatterns += [
    
]