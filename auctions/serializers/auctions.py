from rest_framework import serializers
from rest_framework.response import Response

from auctions.models.auctions import Auction, AuctionImage
from users.models.users import User

class AuctionImageSerializer(serializers.ModelSerializer):
   class Meta:
      model = AuctionImage
      fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):
   image = AuctionImageSerializer()

   class Meta:
      model = Auction 
      fields = '__all__'

class CreateAuctionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Auction
      fields = (
         'title',
         'description',
         'start_time',
         'starting_price',
      )

   def create(self, validated_data):
      request = self.context.get('request')
      seller = request.user

      auction = Auction.objects.create(
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            start_time=validated_data.get('start_time'),
            starting_price=validated_data.get('starting_price'),
            seller_id=seller,
      )
      auction.save()
      return auction
   
   def update(self, instance, validated_data):
      pass
