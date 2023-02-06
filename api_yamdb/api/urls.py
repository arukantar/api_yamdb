from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserViewSet, CategoryViewSet


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/', include(v1_router.urls)),
]
