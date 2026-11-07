from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from apps.authentication.serializer import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegistrationUserSerializer,
    UpdateUserSerializer,
)

User = get_user_model()


class CurrentUserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return self.request.user


class UserRegistrationView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RegistrationUserSerializer
    queryset = User.objects.all()


class PasswordResetRequestView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # same answer either way, so the form can't be used to check who is registered
        return Response({'detail': 'If this email is registered, we have sent a reset link to it.'})


class PasswordResetConfirmView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password changed'})
