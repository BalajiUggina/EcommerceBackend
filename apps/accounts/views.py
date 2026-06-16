from .serializers import LoginSerializer,RegisterSerializer,GoogleLoginSerializer,ProfileUpdateSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from apps.common.responses import success_response,error_response

User=get_user_model()

@extend_schema(
    request=LoginSerializer
)
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data["user"]
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
        return error_response(message="Login failed",errors=serializer.errors)
            
@extend_schema(
    request=RegisterSerializer
)   
class RegisterView(APIView):
    
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="User registered successfully",data=serializer.data,status_code=201)
        return error_response(message="Registration failed",errors=serializer.errors)
    

class VerifyEmailView(APIView):

    def get(self,request,uid64,token):
        try:
            uid=force_str(
                urlsafe_base64_decode(uid64)
            )

            user=User.objects.get(id=uid)
        except Exception:
            return Response(
                {"error":"Invalid user"},status=400
            )
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.is_email_verified=True
            user.save()
            return Response(
                {"message":"Email verified successfully"},status=200
            )
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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Profile data updated",data=serializer.data)