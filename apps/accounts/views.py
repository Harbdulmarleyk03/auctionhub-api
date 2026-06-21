from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from apps.accounts.models import User

from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Register a new user",
        description=(
            "Creates a new user account. "
            "Password must be at least 8 characters. "
            "Email must be unique."
        ),
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Valid registration",
                value={
                    "username": "john_doe",
                    "email": "john@example.com",
                    "password": "securepass123",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Email already exists",
                value={"email": ["Email already exists."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Password too short",
                value={"password": ["Password must be at least 8 characters long."]},
                response_only=True,
                status_codes=["400"],
            ),
        ],
        tags=["Auth"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    @extend_schema(
        summary="Login and obtain JWT tokens",
        description=(
            "Authenticates a user with email and password. "
            "Returns a JWT access token (short-lived) and a refresh token (long-lived). "
            "Use the access token in the Authorization header as: `Bearer <access>`."
        ),
        request=LoginSerializer,
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                },
            ),
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Valid login",
                value={"email": "john@example.com", "password": "securepass123"},
                request_only=True,
            ),
            OpenApiExample(
                "Success response",
                value={
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
        tags=["Auth"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({"access": str(access), "refresh": str(refresh)}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    @extend_schema(
        summary="Logout and blacklist refresh token",
        description=(
            "Invalidates the provided refresh token by adding it to the blacklist. "
            "After this, the refresh token can no longer be used to obtain new access tokens. "
            "Requires `djangorestframework-simplejwt` token blacklisting to be enabled."
        ),
        request=inline_serializer(
            name="LogoutRequest",
            fields={"refresh": serializers.CharField()},
        ),
        responses={
            204: None,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Valid logout",
                value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                request_only=True,
            ),
            OpenApiExample(
                "Missing token",
                value={"error": "Refresh token is required"},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Invalid or expired token",
                value={"error": "Token is invalid or expired"},
                response_only=True,
                status_codes=["400"],
            ),
        ],
        tags=["Auth"],
    )
    def post(self, request):
        token = request.data.get('refresh')
        if token is None:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token_obj = RefreshToken(token)
            token_obj.blacklist()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)