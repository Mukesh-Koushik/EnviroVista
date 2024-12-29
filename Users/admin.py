from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_no', 'profile_pic', 'bio', 'gc_coins', 'location')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_no', 'profile_pic', 'bio', 'gc_coins', 'location')}),
    )

    list_display = ['username', 'email', 'phone_no', 'gc_coins', 'location']
    list_editable = ['gc_coins']

admin.site.register(CustomUser, CustomUserAdmin)
