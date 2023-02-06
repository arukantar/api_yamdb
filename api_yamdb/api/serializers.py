<<<<<<< HEAD
from reviews.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
=======
from rest_framework import serializers

from reviews.models import User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'me не может быть использовано в качестве username'
            )
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User
>>>>>>> feature/register_and_auth
