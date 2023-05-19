from django.urls import path, re_path

from websockets.consumers import AuctionConsumer

websocket_urlpatterns = [
    re_path(r'ws/auctions/(?P<auction_id>[1-9][0-9]*)/$', AuctionConsumer.as_asgi())
]