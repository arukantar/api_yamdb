from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserViewSet


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/', include(v1_router.urls)),
]
