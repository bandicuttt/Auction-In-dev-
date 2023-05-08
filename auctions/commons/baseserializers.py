from rest_framework import serializers
from auctions.models.auctions import Auction, AuctionImage

class BaseAuctionSerializer(serializers.ModelSerializer):

   class Meta:
      model = Auction
      fields = (
         'title',
         'description',
         'start_time',
         'starting_price',
      )

class BaseAuctionImageSerializer(BaseAuctionSerializer):

   auction = BaseAuctionSerializer()

   class Meta:
      model = AuctionImage
      fields = (
         'auction',
         'image',
      )
