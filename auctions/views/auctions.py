from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import mixins, viewsets, status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.conf import settings
from auctions.commons.responses import AuctionResponses
from auctions.serializers.auctions import AuctionSerializer, CreateAuctionSerializer
from users.tasks import account_activate, send_email_confirmation
from drf_spectacular.utils import extend_schema_view, extend_schema,\
OpenApiResponse, OpenApiParameter,OpenApiTypes
from auctions.models.auctions import Auction
from rest_framework.response import Response


@extend_schema_view(
    create=extend_schema(
        summary='Create Auction',
        tags=['Auction'],
        request=CreateAuctionSerializer,
        responses={
            status.HTTP_201_CREATED: CreateAuctionSerializer,
        },
    ),
    list=extend_schema(
        summary='Get All Auctions',
        tags=['Auction'],
        responses={201:OpenApiResponse(response=CreateAuctionSerializer)}
    ),
    retrieve=extend_schema(
        summary='Get Auction',
        tags=['Auction'],
        responses={
            status.HTTP_200_OK: CreateAuctionSerializer,
        },
    ),
    update=extend_schema(
        summary='Update Auction',
        tags=['Auction'],
        responses={201:OpenApiResponse(response=AuctionSerializer)}
    ),
    partial_update=extend_schema(
        summary='Update Auction',
        tags=['Auction'],
        responses={201:OpenApiResponse(response=AuctionSerializer)}
    ),
    destroy=extend_schema(
        summary='Update Auction',
        tags=['Auction'],
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    ),
)
class ActuionView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Auction.objects.all()
    permission_classes = (IsAuthenticated,)
    default_serializer_class = AuctionSerializer

    multi_serializer_classs = {
        'create': CreateAuctionSerializer,
        'retrieve': CreateAuctionSerializer,
        'partial_update': AuctionSerializer,
        'destroy': AuctionSerializer,
        'list': AuctionSerializer,
        'update': AuctionSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete','update')

    def get_serializer_class(self):
        return self.multi_serializer_classs.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        return AuctionResponses.create_auction_success(data)

    def retrieve(self, request,pk=None, *args, **kwargs):
        if pk:
            data = super().retrieve(request, args, kwargs).data
            return AuctionResponses.get_auction_success(data)
        return AuctionResponses.id_is_not_provided()
    
    def update(self, request, *args, **kwargs):
        data = super().retrieve(request, args, kwargs).data
        return Response({
            'INFO': 'SUCCESS',
            'DATA':data,
        })
    
    def list(self, request):
        pass

    def partial_update(self, request):
        pass

    def destroy(self, request):
        pass