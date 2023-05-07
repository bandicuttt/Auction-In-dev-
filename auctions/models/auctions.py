from django.db import models
from users.models.users import User

class Auction(models.Model):

    title=models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
    description=models.TextField(
        max_length=1500,
        blank=False,
        null=False,
    )
    start_time=models.DateTimeField(
        blank=False,
        null=False,
    )
    end_time=models.DateTimeField(
        blank=True,
        null=True,
    )
    starting_price=models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )
    current_price=models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
    )
    status=models.BooleanField(
        default=False,
    )
    seller_id=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='seller_auctions',
    )
    winner_id=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='won_auctions',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Auction'
        verbose_name_plural='Auctions'


class AuctionImage(models.Model):
    
    auction=models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='auction_images/'
    )