import random
import string

from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from reviews.models import User, Category
from .serializers import SignupSerializer, UserSerializer, CategorySerializer
from .constants import CONFIRMATION_CODE_LENGTH


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['POST'])
def signup(request):
    """Регистрация новых пользователей."""

    serializer = SignupSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    if serializer.is_valid():
        new_code = ''.join(random.choices(
            string.ascii_uppercase + string.digits,
            k=CONFIRMATION_CODE_LENGTH
        ))
        new_user = serializer.save(confirmation_code=new_code)
        new_user.email_user(subject='Confirmation code', message=new_code)

        return Response(request.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
