from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import User, Token, Team


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'last_name', 'first_name', 'email', 'phonetic', 'receipt_no', 'org_name', 'team')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'get_full_name',
                    'phonetic', 'team', 'is_staff')
    search_fields = ('username', 'full_name', 'email', 'org_name')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Token)
admin.site.register(Team)
