from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from Users.models import *
from EnviroVista_dep import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional detailed description
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)  # Icon or image for the category
    parent_category = models.ForeignKey( 'self', on_delete=models.CASCADE, related_name='subcategories', blank=True, null=True)  # For hierarchical categories (subcategories)
    is_active = models.BooleanField(default=True)  # To deactivate categories if needed
    created_at = models.DateTimeField(default=now, editable = False)
    updated_at = models.DateTimeField(default=now, editable = False)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    category = models.ManyToManyField(Category, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable = False)
    updated_at = models.DateTimeField(auto_now=True, editable = False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    def is_in_stock(self):
        return self.stock > 0


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Address(models.Model):
    user_id=models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    username=models.CharField(max_length=50)
    country=models.CharField(max_length=30)
    state=models.CharField(max_length=15)
    door_no=models.TextField(max_length=15)
    locality = models.TextField(max_length=100)
    landmark = models.CharField(blank=True, max_length=50, null=True) # Optional field
    city = models.CharField(max_length=30)
    pincode = models.CharField(max_length=6)
    delivery_num = models.CharField(max_length=10)

    class Meta:
        ordering = ['user_id'] # Orders by user id



class Orders(models.Model):
    class Mop_Choices(models.TextChoices):
        COD = "COD", "Cash on Delivery"
        ONLINE = "ONLINE", "Online Payment"
    
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]


    user_id=models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    prod_id=models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at=models.DateTimeField(auto_now_add= True, editable = False)
    order_status = models.CharField(max_length= 20, choices = STATUS_CHOICES, default= "Ordered")
    mode_of_payment=models.CharField(max_length= 10, choices=Mop_Choices.choices, default=Mop_Choices.COD)

    class Meta:
        ordering = ['-ordered_at']  # Show latest orders first
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.product.name}"


# Create your models here.
