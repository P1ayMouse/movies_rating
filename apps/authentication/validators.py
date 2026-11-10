from rest_framework import serializers

MIN_LENGTH = 6


def check_username(value):
    if len(value) < MIN_LENGTH:
        raise serializers.ValidationError('Username is too small')
    return value


def check_passwords(password, password2):
    if password != password2:
        raise serializers.ValidationError({'detail': 'Password mismatch'})
    if len(password) < MIN_LENGTH:
        raise serializers.ValidationError({'detail': 'Password is too small'})
