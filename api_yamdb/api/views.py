from rest_framework import filters, mixins, viewsets

from reviews.models import Category
from .serializers import CategorySerializer


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
