from rest_framework.views import APIView
from rest_framework.response import Response
from apps.auth.services import AuthService
from apps.auth.serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from apps.auth.models import User

class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = AuthService.register_user(serializer.validated_data)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({"access": str(access), "refresh": str(refresh)}, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    def post(self, request):
        token = request.data.get('refresh')
        if token is None:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token_obj = RefreshToken(token)  
            token_obj.blacklist()
        except Exception:
            return Response({'error': 'Failed to blacklist token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)