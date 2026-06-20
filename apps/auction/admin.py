from django.contrib import admin
from apps.auction.models import Auction, Bid 

# Register your models here.
admin.site.register(Auction)
admin.site.register(Bid)
