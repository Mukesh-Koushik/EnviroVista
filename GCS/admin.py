from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'is_active', 'created_at', 'updated_at')  # Columns to display in the admin list view
    list_filter = ('is_active', 'created_at', 'parent_category')  # Filters for the sidebar
    search_fields = ('name', 'description')  # Search by name or description
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug based on name if you add a slug field
    ordering = ('name',)  # Order categories alphabetically
    list_editable = ('is_active',)  # Allow editing of 'is_active' directly in the list view
    readonly_fields = ('created_at', 'updated_at')  # Make timestamps read-only
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon', 'parent_category', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
