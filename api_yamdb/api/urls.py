from django.urls import path, include
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
urlpatterns = [
    path('v1/', include(v1_router.urls))
]
