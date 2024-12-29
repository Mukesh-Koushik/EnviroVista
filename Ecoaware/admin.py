from django.contrib import admin
from Ecoaware.models import *

@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'mode', 'reward', 'created_at', 'updated_at')  # Columns to display in the admin list view
    list_filter = ('mode', 'created_at', 'updated_at')  # Filters for the sidebar
    search_fields = ('name', 'mode')  # Search by name or description
    # prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug
    ordering = ('name',)  # To sort alphabetically
    list_editable = ('reward','image', )  # Allow editing of 'is_active' directly in the list view
    readonly_fields = ('created_at', 'updated_at')  # Disables editing the timestamps
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image', 'mode', 'reward')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# Register your models here.
