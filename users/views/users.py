import uuid
from auctions.commons.responses import UserResponses

from users.serializers.users import CreateUserSerializer, LoginSerializer
from users.models.users import User
from users.tasks import account_activate, send_email_confirmation

from knox import views as knox_views
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema_view, extend_schema,\
OpenApiResponse, OpenApiParameter,OpenApiTypes


@extend_schema_view(
    create=extend_schema(
    summary='Регистрация пользователя',
    tags=['users'],
    )
)
class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


@extend_schema_view(
    post=extend_schema(summary='Авторизация пользователя', tags=['users']),
)
class LoginAPIView(knox_views.LoginView):

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
            token = response.data.get('token')
            response.set_cookie(key='Autorization', value=f'Token {token}')
        else:
            return UserResponses.error_login(serializer.errors)
        return UserResponses.success_login(response.data)
    
@extend_schema_view(
    create=extend_schema(
        summary='Письмо подтверждения (создание)',
        tags=['users'],
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='id пользователя',
                required=True
            )
        ]
        ),
    retrieve=extend_schema(
        summary='Письмо подтверждения (проверка)',
        tags=['users'],
        parameters=[
                OpenApiParameter(
                    name='uuid',
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description='uuid пользователя',
                    required=True
                )
            ]
        )
)
class SendEmailConfirmationView(viewsets.ViewSet, knox_views.LoginView):

    permission_classes = (AllowAny,)
    http_method_names = ('get','post',)

    def create(self, request):
        id = request.query_params.get('id')
        
        if not id:
            return Response({'detail': 'Wrong creditionals'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=id)
        if not user.is_active:
            if not cache.has_key(id):
                uid = str(uuid.uuid4())
                cache.set(id, uid, 3600)
                send_email_confirmation.delay(id, uid, user.email)
                return Response({'uuid': uid}, status=status.HTTP_201_CREATED)
            return Response({'uuid': cache.get(id)}, status=status.HTTP_200_OK)
        return Response({'info':'Your email already confirmed'}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        uid = request.query_params.get('uuid')

        if not uid:
            return Response({'detail': 'Wrong creditionals'})

        if cache.get(pk) == uid:
            cache.delete(pk)
            account_activate.delay(pk)
            user = User.objects.get(id=pk)
            login(request, user)
            response = super().post(request, format=None)
            return Response({'info': 'Success','data':{'authToken':response.data.get('token')}}, status=status.HTTP_200_OK)  
        return Response({'detail': 'Wrong URL address'}, status=status.HTTP_404_NOT_FOUND)