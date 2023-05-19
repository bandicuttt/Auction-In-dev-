from django.db.models.signals import post_save
from django.dispatch import receiver

from auctions.models.auctions import Auction
from websockets.consumers import BaseConsumer


@receiver(post_save, sender=Auction)
def handle_auction_update(sender, instance, **kwargs):
    BaseConsumer().notify_auction_update(instance)