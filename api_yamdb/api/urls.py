from django.urls import path, include
from rest_framework import routers

from .views import CategoryViewSet

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
urlpatterns = [
    path('v1/', include(v1_router.urls))
]
