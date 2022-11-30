from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from core.serializers import RegistrationSerializer
from core.serializers import UserSerializer
from core.serializers import UserTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint that allows users to get token.
    """

    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_clases = [AllowAny]
