from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'is_active', 'created_at', 'updated_at')  # Columns to display in the admin list view
    list_filter = ('is_active', 'created_at', 'parent_category')  # Filters for the sidebar
    search_fields = ('name', 'description')  # Search by name or description
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug
    ordering = ('name',)  # To sort alphabetically
    list_editable = ('is_active',)  # Allow editing of 'is_active' directly in the list view
    readonly_fields = ('created_at', 'updated_at')  # Disables editing the timestamps
    fieldsets = (
        ('Basic Information', {
            'fields': ('name','slug', 'description', 'icon', 'parent_category', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at', 'image')  # Display columns
    list_filter = ('category', 'updated_at')  # Sidebar filters
    search_fields = ('name', 'description')  # Search by name or description
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)  # To sort alphabetically
    list_editable = ('price', 'stock', 'image')  # For quick edits in the list view
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'stock', 'image')
        }),
        ('Category', {
            'fields': ('category',)  # Supports Many-to-Many or ForeignKey
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    filter_horizontal = ('category',)  # Makes multi-select for categories easier