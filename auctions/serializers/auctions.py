import datetime
import pytz

from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from django.db import transaction

from auctions.commons.baseserializers import BaseAuctionImageSerializer, BaseAuctionSerializer
from auctions.commons.responses import AuctionResponses
from auctions.models.auctions import Auction, AuctionImage


class RetrieverAuctionSerializer(BaseAuctionSerializer):
   pass


class WSAuctionListSerailizer(BaseAuctionSerializer):
   pass


class ListAuctionSerializer(serializers.ModelSerializer):
   images_data = serializers.ListField()

   class Meta:
        model = Auction
        fields = (
            'id',
            'title',
            'description',
            'start_time',
            'starting_price',
            'images_data',
        )


class UpdateAuctionSerializer(BaseAuctionSerializer):

   def validate(self, validated_data):
      starting_price = validated_data.get('starting_price')
      start_time = validated_data.get('start_time')

      if not starting_price or not start_time:
         return validated_data

      if start_time < datetime.datetime.now(tz=pytz.utc):
         raise serializers.ValidationError(AuctionResponses.invalid_start_time())
      
      if starting_price <= 0:
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


class CreateAuctionSerializer(BaseAuctionImageSerializer):

   def validate(self, validated_data):
      starting_price = validated_data.get('auction').get('starting_price')
      start_time = validated_data.get('auction').get('start_time')
      request = self.context.get('request')
      seller = request.user

      if start_time < datetime.datetime.now(tz=pytz.utc):
         raise serializers.ValidationError(AuctionResponses.invalid_start_time())

      if starting_price <= 0:
         raise serializers.ValidationError(AuctionResponses.invalid_starting_price())

      if isinstance(seller, AnonymousUser):
            raise serializers.ValidationError(AuctionResponses.anon_user())

      return validated_data

   @transaction.atomic
   def create(self, validated_data):
      request = self.context.get('request')
      auction_data = validated_data.pop('auction')
      image = validated_data.pop('image')
      seller = request.user

      auction = Auction.objects.create(seller_id=seller, **auction_data)
      auction_image = AuctionImage.objects.create(auction=auction,image=image,)

      auction_image.save()
      return auction_image