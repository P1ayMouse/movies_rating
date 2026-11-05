from apps.authentication.serializer import RegistrationUserSerializer, UpdateUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

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
