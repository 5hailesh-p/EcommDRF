from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True)
    class Meta:
        model = User
        fields = ['email','full_name','password','role']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise serializers.ValidationError("Email not verified")

        return user