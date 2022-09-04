from django.urls import include, path

from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()


router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('tags', views.TagViewSet, basename='tags')
router.register('users', views.CustomUserViewSet, basename='users')
router.register(
    'ingredients',
    views.IngredientViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
