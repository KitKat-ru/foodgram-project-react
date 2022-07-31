from django.urls import include, path
# from rest_framework import permissions
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')
router.register(r'tags', views.TagViewSet, basename='tags')

# router.register(
#     r'recipes/(?P<recipes_id>\d+)/favorite',
#     views.***, 
#     basename='favorite') # Доделать сериализер

# router.register(
#     r'users/(?P<user_id>\d+)/subscribe',
#     views.CustomUserViewSet,
#     basename='subscribe') # Доделать сериализер
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     views.CommentViewSet,
#     basename='comments'
# )

urlpatterns = [
    # path('users/subscriptions/'),
    # path('users/<int:user_id>/subscribe/'),
    path('auth/', include('djoser.urls.authtoken')),

    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
