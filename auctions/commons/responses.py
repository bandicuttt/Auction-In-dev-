from rest_framework.response import Response
from rest_framework import status

class AuctionResponses:
    def get_auction_success(data):
        return Response({
            'info':'success',
            'message': {
                'status': 'auction recieved',
                'data': data
            }
        },status=status.HTTP_200_OK)
    
    def id_is_not_provided():
        return Response({
            'info':'error',
            'message': {
                'status': 'Auction ID is not provided',
            }
        },status=status.HTTP_400_BAD_REQUEST)
    
    def create_auction_success(data):
        return Response({
            'info':'success',
            'message': {
                'status': 'auction created',
                'data': data
            }
        },status=status.HTTP_201_CREATED)

