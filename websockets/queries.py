from auctions.models.auctions import Auction, AuctionImage
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async


@database_sync_to_async
def get_auction(auction_id: int):
    auction = get_object_or_404(Auction, pk=auction_id)

    auction_data = AuctionImage.objects.get(auction=auction)

    if auction_data.auction.status:
        return auction_data