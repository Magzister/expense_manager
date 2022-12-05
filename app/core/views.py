import pytz
from decimal import Decimal
from datetime import datetime


from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


from core.models import Transaction
from core.models import Category
from core.models import Profile
from core.serializers import TransactionSerializer
from core.serializers import RegistrationSerializer
from core.serializers import UserSerializer
from core.serializers import UserTokenObtainPairSerializer
from core.serializers import CategorySerializer
from core.permissions import IsOwner


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsOwner]
    serializer_class = CategorySerializer


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = TransactionSerializer

    SORT_VALUES = {'created_at', 'amount'}
    SORT_ORDERS = {'asc': '', 'desc': '-'}
    DATETIME_FORMAT = '%d-%m-%YT%H:%M:%S.%f'
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        start_date = self.request.query_params.get('start_date')
        if start_date is not None:
            dt_start_date = datetime.strptime(start_date, self.DATETIME_FORMAT).replace(tzinfo=pytz.UTC)
            queryset = queryset.filter(
                created_at__gte=dt_start_date
            )

        end_date = self.request.query_params.get('end_date')
        if end_date is not None:
            dt_end_date = datetime.strptime(end_date, self.DATETIME_FORMAT).replace(tzinfo=pytz.UTC)
            queryset = queryset.filter(
                created_at__lte=dt_end_date
            )
        
        sort = self.request.query_params.get('sort')
        if sort is not None:
            sort_value, sort_order = sort.split(':', 1)
            if sort_value.lower() in self.SORT_VALUES:
                if sort_order.lower() in self.SORT_ORDERS:
                    queryset = queryset.order_by(self.SORT_ORDERS[sort_order]+sort_value)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        category = None
        category_dict = self.request.data.get('category')
        if category_dict:
            category_name = category_dict.get('name')
            if category_name:
                try:
                    category = Category.objects.get(user=user, name=category_name)
                except ObjectDoesNotExist:
                    print('Such category is not exist.')

        profile = Profile.objects.get(user=user)
        profile.money += Decimal(self.request.data['amount'])
        profile.save()

        serializer.save(user=self.request.user, category=category)


class UserProfileInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint that allows users to get token.
    """

    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegistrationView(APIView):
    permission_clases = [AllowAny]

    def get(self, request):
        serializer = RegistrationSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
