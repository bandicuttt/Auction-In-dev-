from auctions.models.auctions import Auction
from django.shortcuts import get_object_or_404


def get_auction(auction_id: int):
    auction: Auction = get_object_or_404(Auction, pk=auction_id)

    return Auction.objects.get(auction=auction)
