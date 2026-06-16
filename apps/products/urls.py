from django.urls import path
from .views import ProductView,GetProductView

urlpatterns = [
    path('',ProductView.as_view(),name="products"),
    path('<int:product_id>',GetProductView.as_view(),name="product"),
]