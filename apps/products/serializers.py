from .models import Product,Category,ProductImage
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
    
class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        # CloudinaryField returns a CloudinaryResource — serialize to a URL string
        try:
            # preferred: CloudinaryResource has a `url` attribute
            return obj.image.url
        except Exception:
            # fallback to string representation or None
            return str(obj.image) if obj.image else None
    class Meta:
        model=ProductImage
        fields=["id","image","is_primary"]

class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=["id","name","description","selling_price","original_price","stock_quantity","is_active","images"]