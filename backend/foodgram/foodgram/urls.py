from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('', include('recipes.urls', namespace='recipes')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
