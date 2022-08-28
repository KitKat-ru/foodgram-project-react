from django.urls import include, path

from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()


router.register(r'recipes', views.RecipeViewSet, basename='recipes')
router.register(r'tags', views.TagViewSet, basename='tags')
router.register(r'users', views.CustomUserViewSet, basename='users')
router.register(
    r'ingredients',
    views.IngredientViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
