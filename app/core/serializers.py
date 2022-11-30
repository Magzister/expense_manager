from django.contrib.auth.models import User
from django.contrib.auth.base_user import password_validation
from django.contrib.auth.validators import validators

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)

        #Add custom claims
        token['username'] = user.username
        return token


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
                required=True,
                validators=[UniqueValidator(queryset=User.objects.all())]
                )

    password = serializers.CharField(
                    write_only=True,
                    required=True,
                    validators=[password_validation.validate_password]
                    )
    password2 = serializers.CharField(
                    write_only=True,
                    required=True
                    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                        {"password": "Password fields didn't match."}
                        )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
            )

        return user

    class Meta:
        model = User
        fields = (
                'username',
                'password',
                'password2',
                'email',
                'first_name',
                'last_name'
                )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
            }
