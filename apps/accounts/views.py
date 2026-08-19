from .serializers import LoginSerializer,RegisterSerializer,GoogleLoginSerializer,ProfileUpdateSerializer,ForgotPasswordSerializer,ResetPasswordSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from apps.common.responses import success_response,error_response
import logging

logger = logging.getLogger(__name__)

User=get_user_model()

@extend_schema(
    request=LoginSerializer
)
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data["user"]
            logger.info(f"User login successful for email: {user.email}")
            refresh=RefreshToken.for_user(user)
            data={
                "user":{
                    "full_name": getattr(user, "full_name", None),
                    "email": getattr(user, "email", None),
                    "role": getattr(user, "role", None),
                },
                "access":str(refresh.access_token),
                "refresh":str(refresh),
            }
            return success_response(message="Login successful",data=data,status_code=200)
        logger.warning(f"User login validation failed: {serializer.errors}")
        return error_response(message="Login failed",errors=serializer.errors)
            
@extend_schema(
    request=RegisterSerializer
)   
class RegisterView(APIView):
    
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User registered successfully: {user.email}")
            return success_response(message="User registered successfully",data=serializer.data,status_code=201)
        logger.warning(f"User registration validation failed: {serializer.errors}")
        return error_response(message="Registration failed",errors=serializer.errors)
    

class VerifyEmailView(APIView):

    def get(self,request,uid64,token):
        try:
            uid=force_str(
                urlsafe_base64_decode(uid64)
            )

            user=User.objects.get(id=uid)
        except Exception as exc:
            logger.error(f"Email verification failed: Invalid user ID encoded as {uid64}. Exception: {str(exc)}")
            return Response(
                {"error":"Invalid user"},status=400
            )
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.is_email_verified=True
            user.save()
            logger.info(f"Email verification successful for user: {user.email}")
            return Response(
                {"message":"Email verified successfully"},status=200
            )
        logger.warning(f"Email verification failed: Invalid or expired token for user {user.email}")
        return Response(
            {"error":"Invalid or expired token"},status=400
        )
    
@extend_schema(
    request=GoogleLoginSerializer
)
class GoogleLoginView(APIView):
    def post(self,request):
        serializer=GoogleLoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data["user"]
            logger.info(f"Google login successful for user: {user.email}")
            refresh=RefreshToken.for_user(user)
            data={
                "user":{
                    "full_name": getattr(user, "full_name", None),
                    "email": getattr(user, "email", None),
                    "address":getattr(user,"address",None),
                    "role": getattr(user, "role", None),
                },
                "access":str(refresh.access_token),
                "refresh":str(refresh),
            }
            return success_response(message="Login successful",data=data,status_code=200)
        logger.warning(f"Google login failed due to invalid token or parameters: {serializer.errors}")
        return error_response(message="Registration failed",errors=serializer.errors)

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        data={
            "full_name":request.user.full_name,
            "email":request.user.email,
            "address":request.user.address,
            "role":request.user.role,
        }
        return success_response(message="Profile data retrieved",data=data)


class ProfileUpdateView(APIView):
    permission_classes=[IsAuthenticated]

    def patch(self,request):
        serializer=ProfileUpdateSerializer(instance=request.user,data=request.data,partial=True)
        if not serializer.is_valid():
            logger.warning(f"Profile update validation failed for user {request.user.email}: {serializer.errors}")
            return error_response(message="Profile data update failed", errors=serializer.errors, status_code=400)
        serializer.save()
        logger.info(f"User profile updated successfully for: {request.user.email}")
        return success_response(message="Profile data updated",data=serializer.data)

    

class ForgotPasswordView(APIView):
    def post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data["email"]
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link=f"http://localhost:3000/reset-password/{uid}/{token}"

            try:
                email_sent = send_mail(
                    subject="Password Reset Link",
                    message=f"Click here to reset password: {reset_link}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False
                )
                print(f"Emails sent: {email_sent}")
                logger.info(f"Password reset link sent successfully for: {user.email}")
                return success_response(message= "Password reset link sent successfully")

            except Exception as e:
                print(e)
                print(f"Error sending email: {e}")
                logger.error(f"Error sending email: {e}")
                return error_response(message= "Failed to send reset link",errors="SMTP Failure")
        logger.error(f"Failed to send password reset link for :{user.email}")
        return error_response(message="Failed to send reset link",errors=serializer.errors)


class ResetPasswordView(APIView):
    def post(self,request):
        try:
            serializer=ResetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                uid=serializer.validated_data["uid"]
                token=serializer.validated_data["token"]
                password=serializer.validated_data["password"]
                pk=force_str(urlsafe_base64_decode(uid))
                user=User.objects.get(id=pk)
                if not default_token_generator.check_token(user,token):
                    logger.warning(f"Token failed or Expired token for user:{user.email}")
                    return error_response(message="Invalid Token or expired Token",errors="Token Failed")
                user.set_password(password)
                logger.info(f"Password successfully changed for user:{user.email}")
                user.save()
                return success_response(message="Password changed successfully")
            return error_response(message="Failed to reset password",errors=serializer.errors)
        except Exception as e:
            logger.error(f"Failed to reset password for user:{user.email} due to invalid token or uid")
            return error_response(message="Failed to reset password",errors="Invalid token or uid")
