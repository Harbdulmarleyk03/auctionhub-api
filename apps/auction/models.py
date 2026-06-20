from django.db import models
from apps.accounts.models import User 

class Auction(models.Model):

    STATUS_CHOICES = (
        ("completed", "completed"),
        ("active", "active"),
    )
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)  

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='bids')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
