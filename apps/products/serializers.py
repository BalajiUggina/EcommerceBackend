from .models import Product,Category,ProductImage
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
    
class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        if not obj.image:
            return None
        
        # Reconstruct full URL if it is an external URL (e.g. Unsplash) that got split by Cloudinary
        try:
            if hasattr(obj.image, 'public_id') and hasattr(obj.image, 'format') and obj.image.format:
                if '/' in obj.image.format or obj.image.public_id.startswith('http'):
                    return f"{obj.image.public_id}.{obj.image.format}"
        except Exception:
            pass

        try:
            # preferred: CloudinaryResource has a `url` attribute
            return obj.image.url
        except Exception:
            # fallback to string representation or None
            val_str = str(obj.image)
            if val_str.startswith('image/upload/'):
                return f"https://res.cloudinary.com/dlaa9abs3/{val_str}"
            return val_str
    class Meta:
        model=ProductImage
        fields=["id","image","is_primary"]

class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=["id","name","description","selling_price","original_price","stock_quantity","is_active","images"]