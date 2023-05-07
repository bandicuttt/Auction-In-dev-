from rest_framework import serializers
from auctions.models.auctions import Auction

class BaseAuctionSerializer(serializers.ModelSerializer):

    class Meta:
      model = Auction
      fields = (
         'title',
         'description',
         'start_time',
         'starting_price',
      )