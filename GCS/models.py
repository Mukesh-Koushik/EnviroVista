from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional detailed description
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)  # Icon or image for the category
    parent_category = models.ForeignKey( 'self', on_delete=models.CASCADE, related_name='subcategories', blank=True, null=True)  # For hierarchical categories (subcategories)
    is_active = models.BooleanField(default=True)  # To deactivate categories if needed
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:# Used for sorting alphabetically 
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_subcategories(self):
        return self.subcategories.filter(is_active=True)



class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default='category')
    price_gc = models.DecimalField(max_digits=10, decimal_places=2)  # Price in GC Coins
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

# Create your models here.
