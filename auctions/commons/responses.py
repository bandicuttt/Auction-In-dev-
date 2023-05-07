from rest_framework.response import Response
from rest_framework import status

class AuctionResponses:
    def get_auction_success(data):
        return Response({
            'message': {
                'info':'success',
                'status': 'auction recieved',
                'data': data
            }
        },status=status.HTTP_200_OK)
    
    def invalid_starting_price():
        return {
            'message': {
                'info': 'error',
                'status': 'Provided invalid starting price',
            }
        }
    
    def invalid_start_time():
        return {
            'message': {
                'info': 'error',
                'status': 'Provided invalid start time',
            }
        }
    
    def id_is_not_provided():
        return Response({
            'message': {
                'info':'error',
                'status': 'Auction ID is not provided',
            }
        },status=status.HTTP_400_BAD_REQUEST)
    
    def create_auction_success(data):
        return Response({
            'message': {
                'info':'success',
                'status': 'auction created',
                'data': data
            }
        },status=status.HTTP_201_CREATED)
    
    def no_permissions(view=False):
        if view:
            return Response({
                'message': {
                    'info':'error',
                    'status': 'You have not permissions to do this action',
                }
            }, status=status.HTTP_403_FORBIDDEN)
        return {
            'message': {
                'info':'error',
                'status': 'You have not permissions to do this action',
            }
        }
    
    def delete_auction_success():
        return Response({
            'message': {
                'info':'success',
                'status': 'auction deleted',
            }
        },status=status.HTTP_205_RESET_CONTENT)

