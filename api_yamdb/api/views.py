import random
import string

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter

from reviews.models import User, Category
from .serializers import (
    SignupSerializer,
    UserSerializer,
    AdminUserSerializer,
    CategorySerializer,
    TokenSerializer
)
from .constants import CONFIRMATION_CODE_LENGTH
from .permissions import AdminOnly


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get(
            'confirmation_code'
        )
        user = get_object_or_404(User, username=username)
        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
@permission_classes((AllowAny,))
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
        serializer.save(confirmation_code=new_code)
        send_mail(
            subject='Confirmation code',
            message=f'confirmation_code: {new_code}',
            from_email='arukantar@gmail.com',
            recipient_list=[serializer.validated_data.get('email')],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated, ],
        url_path='me',
        url_name='me'
    )
    def user_me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = AdminUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
