from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(
        max_length=60,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        db_table="categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category=models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name=models.CharField(max_length=255)

    slug=models.SlugField(
        unique=True,
        blank=True
    )

    description=models.TextField()

    selling_price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    original_price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_quantity=models.PositiveIntegerField(
        default=1
    )

    is_active=models.BooleanField(
        default=True
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    updated_at=models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table="products"
        ordering=["-created_at"]

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)

        super().save(*args,**kwargs)

    @property
    def is_in_stock(self):
        return self.stock_quantity>0
    
    def __str__(self):
        return self.name


# models for product image
class ProductImage(models.Model):
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image=CloudinaryField("image")

    is_primary=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="product_images"
        
    def __str__(self):
        return f"{self.product.name} Image"