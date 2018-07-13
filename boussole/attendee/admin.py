from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .models import User, Token, Team


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password', 'token')}),
        (_('Personal info'), {'fields': (
            'last_name', 'first_name', 'email', 'phonetic', 'receipt_no', 'org_name', 'team', 'check_in')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('token',)
    list_display = ('username', 'receipt_no', 'email', 'get_full_name',
                    'phonetic', 'team', 'check_in', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'team')
    search_fields = ('username', 'full_name', 'email', 'org_name')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Token)
admin.site.register(Team)
