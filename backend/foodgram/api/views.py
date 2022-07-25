from djoser.views import UserViewSet, TokenCreateView
from api.serializers import CustomUserSerializer
from users.models import User



# # class CustomTokenCreateView(TokenCreateView):
# #     serializer_class = CustomUserSerializer
# #     queryset = User.objects.all()



class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()