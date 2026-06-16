from django.db import models
from apps.products.models import Product
from django.contrib.auth import get_user_model

User=get_user_model()

class Cart(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    updated_at=models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table="carts"
    
    def __str__(self):
        return f"{self.user.email}'s Cart"


class CartItem(models.Model):
    cart=models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity=models.PositiveIntegerField(
        default=1
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    updated_at=models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table="cart_items"

        constraints=[
            models.UniqueConstraint(
                fields=["cart","product"],
                name="unique_cart_product",
            )
        ]
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"



