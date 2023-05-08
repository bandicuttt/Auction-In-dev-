import json
from django.http import QueryDict
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, viewsets
from django.core.cache import cache
from auctions.commons.responses import AuctionResponses
from auctions.serializers.auctions import CreateAuctionSerializer,\
ListAuctionSerializer, RetrieverAuctionSerializer, UpdateAuctionSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
from auctions.models.auctions import Auction, AuctionImage
from drf_nested_forms.parsers import NestedMultiPartParser
from rest_framework import serializers


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
    
    permission_classes = (AllowAny,)
    default_queryset = Auction.objects.all()
    default_serializer_class = RetrieverAuctionSerializer
    parser_classes = [NestedMultiPartParser]

    multi_serializer_classes = {
        'create': CreateAuctionSerializer,
        'retrieve': RetrieverAuctionSerializer,
        'partial_update': UpdateAuctionSerializer,
        'list': ListAuctionSerializer,
    }

    multi_queryset = {
        'create': AuctionImage.objects.all(),
        'retrieve': Auction.objects.all(),
        'partial_update': Auction.objects.all(),
        'destroy': Auction.objects.all(),
        'list': AuctionImage.objects.all(),
    }

    http_method_names = ('get', 'post', 'patch', 'delete')

    def __transform_request_data(self, data):
        '''
        Метод позвояет работать с form-data, перехватывать данные
        преобразовывать их в то, что этой нехорошей точке нужно (в JSON)
        '''
        if type(data) == QueryDict:
            data = data.dict()
        
        for key, value in self.get_serializer().get_fields().items():
            if isinstance(value, serializers.ListSerializer) or \
            isinstance(value, serializers.ModelSerializer):
                if key in data and type(data[key]) == str:
                    try:
                        data[key] = None if \
                        data[key] == '' else \
                        json.loads(data[key]) 
                    except:
                        raise serializers.ValidationError(AuctionResponses.invalid_json_data())
        return data

    def get_queryset(self):
        return self.multi_queryset.get(self.action, self.default_queryset)

    def get_serializer_class(self):
        return self.multi_serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        data = self.__transform_request_data(request.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return AuctionResponses.create_auction_success(serializer.data)
    
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
            return AuctionResponses.no_permissions(view=True)
        return AuctionResponses.id_is_not_provided()