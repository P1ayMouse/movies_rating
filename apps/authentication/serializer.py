from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers

from apps.authentication.models import UserToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']


class RegistrationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'username']

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password2 != password:
            raise serializers.ValidationError({'detail': 'Password mismatch'})
        elif len(password) < 6:
            raise serializers.ValidationError({'detail': 'Password is too small'})

        username = self.validated_data['username']
        if len(username) < 6:
            raise serializers.ValidationError({'detail': 'Username is too small'})

        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password2 = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        read_only_fields = ['email']

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Username is too small')
        return value

    def validate(self, attrs):
        password = attrs.get('password', '')

        if password or attrs.get('password2'):
            if password != attrs.get('password2'):
                raise serializers.ValidationError({'detail': 'Password mismatch'})
            if len(password) < 6:
                raise serializers.ValidationError({'detail': 'Password is too small'})
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password', '')
        validated_data.pop('password2', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        user = User.objects.filter(email__iexact=self.validated_data['email']).first()
        if user is None:
            return None

        user_token = UserToken.objects.create(user=user)
        link = f'{settings.SITE_URL}/password-reset/{user_token.token}/'
        hours = int(settings.PASSWORD_RESET_LINK_LIFETIME.total_seconds() // 3600)
        send_mail(
            subject='Reset your Diploma MDB password',
            message=(
                f'To set a new password, open this link:\n\n{link}\n\n'
                f'The link works once and expires in {hours} hour(s). '
                'If you did not ask for a password reset, ignore this email.'
            ),
            from_email=None,
            recipient_list=[user.email],
        )
        return user_token


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'detail': 'Password mismatch'})
        if len(attrs['password']) < 6:
            raise serializers.ValidationError({'detail': 'Password is too small'})

        oldest_valid = timezone.now() - settings.PASSWORD_RESET_LINK_LIFETIME
        user_token = UserToken.objects.select_related('user').filter(
            token=attrs['token'],
            used_at__isnull=True,
            created_at__gte=oldest_valid,
        ).first()
        if user_token is None:
            raise serializers.ValidationError({'detail': 'The reset link is invalid or expired'})

        attrs['user_token'] = user_token
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user_token'].user
        user.set_password(self.validated_data['password'])
        user.save(update_fields=['password'])
        # a link works once; this also cancels any other links sent earlier
        user.user_tokens.filter(used_at__isnull=True).update(used_at=timezone.now())
        return user
