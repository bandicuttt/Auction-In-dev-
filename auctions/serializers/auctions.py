import datetime
import pytz
from rest_framework import serializers
from rest_framework.response import Response
from auctions.commons.baseserializers import BaseAuctionSerializer
from auctions.commons.responses import AuctionResponses

from auctions.models.auctions import Auction, AuctionImage
from users.models.users import User


class RetrieverAuctionSerializer(BaseAuctionSerializer):
   pass

class UpdateAuctionSerializer(BaseAuctionSerializer):

   def validate(self, validated_data):
      starting_price = validated_data.get('starting_price')
      start_time = validated_data.get('start_time')

      if not starting_price or not start_time:
         return validated_data

      if start_time < datetime.datetime.now(tz=pytz.utc):
         raise serializers.ValidationError(AuctionResponses.invalid_start_time())

      if starting_price < 0:
         raise serializers.ValidationError(AuctionResponses.invalid_starting_price())
      
      return validated_data
   
   def update(self, instance, validated_data):
      if instance.id:
         request = self.context.get('request')
         seller = request.user
         if seller == instance.seller_id and not instance.winner_id and not instance.status:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance   
      raise serializers.ValidationError(AuctionResponses.no_permissions())

class CreateAuctionSerializer(BaseAuctionSerializer):

   def validate(self, validated_data):
      starting_price = validated_data.get('starting_price')
      start_time = validated_data.get('start_time')

      if start_time < datetime.datetime.now(tz=pytz.utc):
         raise serializers.ValidationError(AuctionResponses.invalid_start_time())

      if starting_price < 0:
         raise serializers.ValidationError(AuctionResponses.invalid_starting_price())
      
      return validated_data

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


class ListAuctionSerializer(BaseAuctionSerializer):

   auction = RetrieverAuctionSerializer()

   class Meta:
      model = AuctionImage
      fields = '__all__'