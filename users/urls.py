from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import get_conf_code, get_token

urlpatterns = [
        path('email/', get_conf_code),
        path('token/', get_token, name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
