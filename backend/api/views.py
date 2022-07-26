from djoser.views import UserViewSet
from api.serializers import CustomUserSerializer
from users.models import User


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()