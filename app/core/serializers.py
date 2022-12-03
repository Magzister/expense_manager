from django.contrib.auth.models import User
from django.contrib.auth.base_user import password_validation


from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from core.models import Profile
from core.models import Category
from core.models import DefaultCategory
from core.models import Transaction


class ProfileSerializer(serializers.ModelSerializer):
    money = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = Profile
        fields = ['money']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(required=False)

    class Meta:
        model = Transaction
        fields = '__all__'


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)

        #Add custom claims
        token['username'] = user.username
        return token


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ],
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
    profile = ProfileSerializer()

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        
        Profile.objects.create(user=user, **profile_data)
        
        #Attach default categories to user
        default_categories = DefaultCategory.objects.all()
        categories_to_add = []
        for default_category in default_categories:
            categories_to_add.append(Category(user=user, name=default_category.name))
        Category.objects.bulk_create(categories_to_add)

        return user
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'profile',
        ]
