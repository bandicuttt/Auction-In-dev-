from django.urls import path, include
from users.views.users import CreateUserViewSet, LoginAPIView, SendEmailConfirmationView
from knox.views import LogoutView, LogoutAllView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'create-user', CreateUserViewSet,'create-user')
router.register(r'email-confirmation', SendEmailConfirmationView, 'email-conf')

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
]
urlpatterns += router.urls
