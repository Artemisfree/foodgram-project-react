from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .utils import DownloadList
from .views import (CreateUserView, FavoriteViewSet, IngredientViewSet,
                    ListViewSet, RecipeViewSet, SubscribeViewSet, TagViewSet)

app_name = 'api'
router_v1 = DefaultRouter()


router_v1.register('v1/users', CreateUserView, basename='users')
router_v1.register(r'v1/tags', TagViewSet, basename='tags')
router_v1.register(r'v1/recipes', RecipeViewSet, basename='recipes')
router_v1.register(
    r'v1/ingredients', IngredientViewSet, basename='ingredients'
)


urlpatterns = [
    path('v1/users/subscriptions/',
         SubscribeViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('v1/recipes/download_shopping_list/',
         DownloadList.as_view({'get': 'download'}), name='download'),
    path('v1/users/<users_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create',
                                   'delete': 'delete'}), name='subscribe'),
    path('v1/recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('v1/recipes/<recipes_id>/shopping_cart/',
         ListViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='list'),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
