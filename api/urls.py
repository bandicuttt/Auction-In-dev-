from django.urls import include, path
from .spectacular.urls import urlpatterns as doc_urls

app_name = 'api'
urlpatterns = [
]
urlpatterns+=doc_urls