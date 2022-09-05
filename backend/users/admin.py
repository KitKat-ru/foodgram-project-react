from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from recipes.models import Favorite, ShoppingBasket

# from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Subscription, User


class FavoriteInline(admin.TabularInline):
    model = Favorite


class ShoppingBasketInline(admin.TabularInline):
    model = ShoppingBasket


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    model = User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'email',
                'first_name',
                'last_name',
            ),
        }),
    )
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


class SubscriptionAdminForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'

    def clean(self):
        if self.cleaned_data['user'] == self.cleaned_data['following']:
            raise forms.ValidationError('Нельзя подписать самого себя!')
        return self.cleaned_data


class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionAdminForm
    model = Subscription
    list_display = [
        'pk',
        'user',
        'following',
    ]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
