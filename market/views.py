from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from market.filters import CarModelFilter, PostFilter
from market.pagination import DefaultPagination

from .models import CarModel, Favorites, Post, PostImage
from .serializers import (Add_Favorite_serializer, CarModel_serializer, Favorite_serializer,
                          Post_serializer, PostDetail_serializer,
                          PostImage_serializer)

from rest_framework.decorators import api_view
from rest_framework import status

class PostViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Post.objects.prefetch_related('user').prefetch_related('carmodel').prefetch_related('postimage_set').order_by('-created_at').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title','description','carmodel__model','carmodel__make']
    ordering_fields = ['price']
    filterset_class = PostFilter
    pagination_class = DefaultPagination
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetail_serializer
        return Post_serializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id,
        'request':self.request}  #pass pk from url to serializer so it can use it when overriding save

class MyPostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = Post_serializer
    search_fields = ['title','description']
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Post.objects.prefetch_related('postimage_set').filter(user_id=self.request.user.id).order_by('-created_at')
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id,
        'request':self.request}  #pass pk from url to serializer so it can use it when overriding save
    
    """ def destroy(self, request, *args, **kwargs):
       instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT) """

class PostImageModelViewSet(ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImage_serializer

class FavoritesViewSet(ListModelMixin, DestroyModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return Favorite_serializer
        return Add_Favorite_serializer
    
    def get_queryset(self):
        return Favorites.objects.select_related('post').filter(user_id=self.request.user.id)

    def get_serializer_context(self):
        return {'user_id':self.request.user.id,
        'request':self.request}


# List of car makes should be shipped with the app to reduce traffic
class CarModelViewSet(ListModelMixin, GenericViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = CarModel.objects.all()
    serializer_class = CarModel_serializer
    filterset_class = CarModelFilter
