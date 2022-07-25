from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации унаследованная от дефолтной."""
    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name', 'password')


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пароля унаследованная от дефолтной."""
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields