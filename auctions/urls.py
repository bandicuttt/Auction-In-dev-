from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auctions.views.auctions import AuctionView

router = DefaultRouter()
router.register(r'auction', AuctionView,'auction')

urlpatterns = [
    
]
urlpatterns += router.urls
