from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from core.views import UserTokenObtainPairView
from core.views import RegistrationView


urlpatterns = [
    path('login/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
