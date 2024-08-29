from django.contrib import admin
from .models import Property, Agent, ContactMessage

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'agent', 'price', 'location', 'listed_date', 'is_featured')
    list_filter = ('is_featured', 'property_type', 'listed_date')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'title': ('location',)}

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'phone_number')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('sent_at',)
