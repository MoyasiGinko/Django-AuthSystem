from django.contrib import admin
from .models import ContactMessage, Companyinfo

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('sent_at',)

@admin.register(Companyinfo)
class CompanyinfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'province_code', 'phone1', 'company_email', 'subscription_type')
    search_fields = ('company_name', 'user__username', 'company_email', 'province_code', 'phone1')
    list_filter = ('subscription_type', 'member_activation_status')
    readonly_fields = ('registration_date',)
