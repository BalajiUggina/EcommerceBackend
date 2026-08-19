from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from apps.common.responses import success_response,error_response
from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)


class ProductView(APIView):
    def get(self,request):
        try:
            products = Product.objects.all()
        except DatabaseError as exc:
            logger.error("Database error while fetching all products", exc_info=True)
            return error_response(
                message="Database error while fetching products",
                errors=str(exc),
                status_code=500,
            )

        try:
            # If there are no products, return an empty list (client-friendly)
            if not products.exists():
                logger.info("Products list requested, but no products exist in the database.")
                return success_response(message="No products found", data=[], status_code=200)

            serializer = ProductSerializer(products, many=True)
            logger.info(f"Successfully retrieved {products.count()} products.")
            return success_response(message="Products retrieved successfully", data=serializer.data, status_code=200)

        except Exception as exc:
            logger.error("Internal server error while preparing products data", exc_info=True)
            return error_response(
                message="Internal server error while preparing products",
                errors=str(exc),
                status_code=500,
            )
            
            
class GetProductView(APIView):
    def get(self,request,product_id):
        # Validate and fetch
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.warning(f"Product search failed: Product with ID {product_id} does not exist.")
            return error_response(message="Product not found", errors="Invalid id or product deleted", status_code=404)
        except (ValueError, TypeError) as exc:
            logger.warning(f"Product search failed: Invalid product ID type/value '{product_id}'. Error: {str(exc)}")
            return error_response(message="Invalid product id", errors=str(exc), status_code=400)
        except DatabaseError as exc:
            logger.error(f"Database error while fetching product with ID {product_id}", exc_info=True)
            return error_response(message="Database error while fetching product", errors=str(exc), status_code=500)

        # Serialize and respond
        try:
            serializer = ProductSerializer(product)
            logger.info(f"Product with ID {product_id} retrieved successfully.")
            return success_response(message="Product retrieved successfully", data=serializer.data, status_code=200)
        except Exception as exc:
            logger.error(f"Internal server error while preparing product data for ID {product_id}", exc_info=True)
            return error_response(
                message="Internal server error while preparing product",
                errors=str(exc),
                status_code=500,
            )


