from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auctions.views.auctions import ActuionView

router = DefaultRouter()
router.register(r'auction', ActuionView,'auction')

urlpatterns = [
    
]
urlpatterns += router.urls
