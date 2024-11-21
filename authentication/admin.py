from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'company_name', 'phone1', 'phone2', 'is_active', 'is_staff', 'subscription_type', 'mem_activation_status')
    search_fields = ('username', 'email', 'company_name')
    readonly_fields = ('registration_date', 'current_activation_date', 'expiry_current_activation')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('company_name', 'email', 'company_logo', 'address', 'province_code', 'area_code')}),
        ('Contact Info', {'fields': ('phone1', 'phone2')}),
        ('Subscription Info', {'fields': ('subscription_type', 'mem_activation_status', 'note_and_description')}),
        ('Activation Dates', {'fields': ('registration_date', 'current_activation_date', 'expiry_current_activation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Register the CustomUser model with the admin
admin.site.register(CustomUser, CustomUserAdmin)
