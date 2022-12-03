from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from core.views import UserTokenObtainPairView
from core.views import RegistrationView
from core.views import TransactionListCreateAPIView
from core.views import CategoryListCreateAPIView
from core.views import CategoryRetrieveUpdateDestroyApiView
from core.views import UserProfileInfo


urlpatterns = [
    path('login/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='list_create_transaction'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='list_create_category'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyApiView.as_view(), name='retrieve_update_destroy_category'),
    path('profile/', UserProfileInfo.as_view(), name='profile'),
]
