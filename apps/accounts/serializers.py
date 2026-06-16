from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from google.auth.transport import requests
from google.oauth2 import id_token


User=get_user_model()

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self,data):
        email=data.get("email")
        password=data.get("password")

        try:
            user=User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error":"Invalid Credentials"})
        if not user.check_password(password):
            raise serializers.ValidationError({"error":"Invalid Credentials"})
        
        data["user"]=user

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["full_name","email","password","confirm_password"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "user with this email already exists."
            )
        return value
    
    def validate(self,data):
        if data["password"]!=data["confirm_password"]:
            raise serializers.ValidationError("Password fields must match")
        return data
    
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        user=User.objects.create_user(
            **validated_data
        )
        return user


    

class GoogleLoginSerializer(serializers.Serializer):
    token=serializers.CharField()

    def validate(self,data):
        token=data.get("token")
        try:
            google_user=id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
            print(google_user)

        except Exception as e:
            print(e)
            raise serializers.ValidationError({
                "error":"Invalid Google token"
            })
        
        email=google_user.get("email")
        full_name=google_user.get("name")

        user,created=User.objects.get_or_create(
            email=email,
            defaults={
                "full_name":full_name,
                "is_active":True,
                "is_email_verified":True,
            }
        )

        data["user"]=user
        return data
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=False)
    new_password=serializers.CharField(write_only=True,required=False)
    confirm_password=serializers.CharField(write_only=True,required=False)
    class Meta:
        model=User
        fields=["full_name","email","address","password","new_password","confirm_password",]

    def validate_email(self, value):
        user = self.instance
        email_exists = User.objects.filter(
            email=value
        ).exclude(id=user.id).exists()

        if email_exists:
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, attrs):
        password = attrs.get("password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if password or new_password or confirm_password:

            if not self.instance.check_password(password):
                raise serializers.ValidationError({"errors":"Current password is incorrect"})

            if new_password != confirm_password:
                raise serializers.ValidationError({"errors":"Passwords do not match"})

        return attrs
    
    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)

        new_password = validated_data.pop(
            "new_password",
            None
        )

        validated_data.pop(
            "confirm_password",
            None
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()

        return instance
