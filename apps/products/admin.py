from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category,Product,ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "created_at"
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "selling_price",
        "stock_quantity",
        "is_active",
        "created_at"
    )

    list_filter = (
        "category",
        "is_active"
    )

    search_fields = (
        "name",
        "description"
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [
        ProductImageInline
    ]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "is_primary",
        "created_at"
    )

    list_filter = (
        "is_primary",
    )