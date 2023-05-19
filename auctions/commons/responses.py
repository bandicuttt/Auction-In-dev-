from rest_framework.response import Response
from rest_framework import status


class UserResponses:

    def success_login(data):
        return Response({
            'message': {
                'info':'success',
                'status': 'successful authorization',
                'data': data
            }
        },status=status.HTTP_200_OK)
    
    def error_login(data):
        return Response({
            'message': {
                'info':'error',
                'status': 'provided invalid data',
                'data': data
            }
        },status=status.HTTP_200_OK)

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
                'status': 'provided invalid starting price',
            }
        }
    
    def invalid_start_time():
        return {
            'message': {
                'info': 'error',
                'status': 'provided invalid start time',
            }
        }
    
    def id_is_not_provided():
        return Response({
            'message': {
                'info':'error',
                'status': 'auction ID is not provided',
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
                    'status': 'you have not permissions to do this action',
                }
            }, status=status.HTTP_403_FORBIDDEN)
        return {
            'message': {
                'info':'error',
                'status': 'you have not permissions to do this action',
            }
        }
    
    def invalid_json_data():
        return {
            'message': {
                'info':'error',
                'status': 'you have provided invalid data',
            }
        }
    
    def anon_user():
         return {
            'message': {
                'info':'error',
                'status': 'you are not logged in',
            }
        }