from django.contrib.auth import get_user_model
from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

User = get_user_model()
# TODO Здесь нам придется переопределить сериалайзер, который использует djoser
# TODO для создания пользователя из за того, что у нас имеются нестандартные поля


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    id = serializers.IntegerField(required=False)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        # exclude = ['image']
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])

        user.save()
        return user

    def save(self, **kwargs):
        user = super().save(**kwargs)
        if kwargs.get("password"):
            user.set_password(kwargs["password"])

        user.save()
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'image']
