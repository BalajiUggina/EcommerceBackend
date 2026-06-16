from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ContactSerializer
from .services import send_contact_email
from apps.common.responses import success_response,error_response

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            try:
                send_contact_email(serializer.validated_data)
            except ValueError:
                raise ValueError({"error":"Failed to send email"})

            return success_response(message= "Message sent successfully")

        return error_response(
            message="Failed to send message",
            errros=serializer.errors,
        )