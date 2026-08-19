from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from .serializers import ContactSerializer
from .services import send_contact_email
from apps.common.responses import success_response,error_response

logger = logging.getLogger(__name__)

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            email_address = serializer.validated_data.get('email')
            logger.info(f"Received contact form submission from: {email_address}")
            try:
                send_contact_email(serializer.validated_data)
                logger.info(f"Contact email sent successfully for submission from: {email_address}")
            except Exception as exc:
                logger.error(f"Failed to send contact email for {email_address}: {str(exc)}", exc_info=True)
                return error_response(
                    message="Failed to send email, please try again later",
                    errors=str(exc),
                    status_code=500
                )

            return success_response(message= "Message sent successfully")

        logger.warning(f"Contact form submission failed due to validation errors: {serializer.errors}")
        return error_response(
            message="Failed to send message",
            errors=serializer.errors,
        )