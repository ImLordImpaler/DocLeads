from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['name','phone', 'email','is_doctor','is_paitent', 'is_active', 'is_superuser', 'is_admin','is_subadmin']
    list_filter = ['is_doctor', 'is_paitent', 'is_admin']
    search_fields = ['phone', 'email']
    ordering = ['phone']

    fieldsets = (
        (None, {
            'fields': ('phone', 'email', 'name', 'password')
        }),
        ('Permissions', {
            'fields': ('is_doctor','is_paitent','is_superuser','is_admin','is_subadmin','is_active', 'is_staff' , 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
        ('Personal info', {
            'fields': ('email', 'name'),
        }),
        ('Permissions', {
            'fields': ('is_doctor','is_paitent','is_active','is_superuser','is_admin','is_subadmin'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
