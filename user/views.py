# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from django.core.cache import cache
from .models import User
from .services import send_otp_mail



@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            send_otp_mail(user)

            return Response({
                "message": "User registered successfully! OTP sent on email",
                "user_id": str(user.id)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self,request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        stored_otp = cache.get(f"otp:{email}")

        if not stored_otp :
            return Response({"error":"OTP expired or not found"}, status=400)
        if stored_otp != otp:
            return Response({"error":"Invalid OTP"}, status=400)
        
        user = User.objects.get(email= email)
        user.is_verified = True
        user.save()


        cache.delete(f"otp:{email}")
        return Response({"message": "Email verified successfully"})





