from rest_framework import serializers

from reviews.models import User, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


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
