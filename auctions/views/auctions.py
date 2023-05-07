from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import mixins, viewsets, status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.conf import settings
from auctions.commons.responses import AuctionResponses
from auctions.serializers.auctions import CreateAuctionSerializer, ListAuctionSerializer, RetrieverAuctionSerializer, UpdateAuctionSerializer
from users.tasks import account_activate, send_email_confirmation
from drf_spectacular.utils import extend_schema_view, extend_schema,\
OpenApiResponse, OpenApiParameter,OpenApiTypes
from auctions.models.auctions import Auction, AuctionImage
from rest_framework.response import Response


@extend_schema_view(
    create=extend_schema(
        summary='Create Auction',
        tags=['Auction'],
    ),
    list=extend_schema(
        summary='Get All Auctions',
        tags=['Auction'],
    ),
    retrieve=extend_schema(
        summary='Get Auction',
        tags=['Auction'],
    ),
    partial_update=extend_schema(
        summary='Update Auction',
        tags=['Auction'],
    ),
    destroy=extend_schema(
        summary='Destroy Auction',
        tags=['Auction'],
    ),
)
class AuctionView(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                mixins.ListModelMixin,viewsets.GenericViewSet):
    
    permission_classes = (IsAuthenticated,)
    default_queryset = Auction.objects.all()
    default_serializer_class = RetrieverAuctionSerializer

    multi_serializer_classes = {
        'create': CreateAuctionSerializer,
        'retrieve': RetrieverAuctionSerializer,
        'partial_update': UpdateAuctionSerializer,
        'list': ListAuctionSerializer,
    }

    multi_queryset = {
        'create': Auction.objects.all(),
        'retrieve': Auction.objects.all(),
        'partial_update': Auction.objects.all(),
        'destroy': Auction.objects.all(),
        'list': AuctionImage.objects.all(),
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return self.multi_queryset.get(self.action, self.default_queryset)

    def get_serializer_class(self):
        return self.multi_serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        return AuctionResponses.create_auction_success(data)
    
    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        return AuctionResponses.get_auction_success(data)

    def retrieve(self, request,pk=None, *args, **kwargs):
        if pk:
            data = super().retrieve(request, args, kwargs).data
            return AuctionResponses.get_auction_success(data)
        return AuctionResponses.id_is_not_provided()

    def partial_update(self, request, pk=None, *args, **kwargs):
        if pk:
            data = super().partial_update(request).data
            return AuctionResponses.get_auction_success(data)
        return AuctionResponses.id_is_not_provided()

    def destroy(self, request, pk=None, *args, **kwargs):
        if pk:
            instance = self.get_object()
            if request.user == instance.seller_id and not instance.winner_id and not instance.status:
                self.perform_destroy(instance)
                return AuctionResponses.delete_auction_success()
            return AuctionResponses.no_permissions(view=True)
        return AuctionResponses.id_is_not_provided()