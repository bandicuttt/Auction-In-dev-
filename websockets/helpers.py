from urllib.parse import parse_qs
from knox.auth import TokenAuthentication
from src.settings import HTTP_HEADER_ENCODING
from asgiref.sync import sync_to_async
from rest_framework.exceptions import AuthenticationFailed


async def get_authenticated_user(self):

    knoxAuth = TokenAuthentication()
    qs = self.scope['query_string'].decode('utf-8')
    query_params = parse_qs(qs)
    tokenString = query_params.get('token', [''])[0]

    if tokenString:
        try:
            authenticate_credentials_async = sync_to_async(knoxAuth.authenticate_credentials)
            return await authenticate_credentials_async(tokenString.encode(HTTP_HEADER_ENCODING))
        except AuthenticationFailed:
            return False