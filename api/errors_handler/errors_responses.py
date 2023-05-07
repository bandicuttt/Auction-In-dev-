from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from auctions.views.auctions import AuctionView


def custom_exception_handler(exc, context):
    print(exc)
    print(type(exc))
    response = exception_handler(exc, context)

    if isinstance(exc, Http404) and isinstance(context.get('view'), AuctionView):
        return Response({
            'info':'error',
            'message': {
                'status': 'Auction you provided is not found',
            }
        },status=status.HTTP_404_NOT_FOUND)

    return response