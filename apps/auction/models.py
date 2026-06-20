from django.db import models
from django.conf import settings
from django.utils import timezone

class Auction(models.Model):

    STATUS_CHOICES = (
        ("completed", "completed"),
        ("active", "active"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='auctions', default=1)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_time = timezone.now()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)  

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='bids', default=1)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = timezone.now()
