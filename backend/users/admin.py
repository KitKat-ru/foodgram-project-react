from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import Favorite, ShoppingBasket, Subscription

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class FavoriteInline(admin.TabularInline):
    model = Favorite


class ShoppingBasketInline(admin.TabularInline):
    model = ShoppingBasket


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'counts_subscription',
    ]
    inlines = (FavoriteInline, ShoppingBasketInline, SubscriptionInline, )
    empty_value_display = '-пусто-'
    search_fields = ('username', 'email', )
    list_filter = ('username', 'email', )
    readonly_fields = ['counts_subscription']

    def counts_subscription(self, obj):
        return obj.following.count()


admin.site.register(User, CustomUserAdmin)
