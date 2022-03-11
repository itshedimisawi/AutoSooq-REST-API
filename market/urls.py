from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views
# URLConf
router = routers.SimpleRouter()
#router.register('profiles', views.UserProfileViewSet, basename='profiles')
router.register('posts', views.PostViewSet, basename='posts')
router.register('myposts', views.MyPostViewSet, basename='myposts')
router.register('myfavorites', views.FavoritesViewSet, basename='myfavorites')
router.register('postimages', views.PostImageModelViewSet, basename='postimages')
router.register('carmodels', views.CarModelViewSet, basename='carmodels')



urlpatterns = [
    path('', include(router.urls)),
]

