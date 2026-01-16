from django.contrib import admin
from django.urls import path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from loyalty.views import (
    RegisterView,
    MyLoyaltyCardView,
    AddBonusView,
    WalletHistoryView,
    CreateOrderView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Loyalty API",
        default_version='v1',
        description="Full Loyalty Backend API",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),

    # LOYALTY
    path('loyalty/my-card/', MyLoyaltyCardView.as_view()),
    path('loyalty/add-bonus/', AddBonusView.as_view()),
    path('loyalty/history/', WalletHistoryView.as_view()),

    # ORDERS
    path('orders/create/', CreateOrderView.as_view()),

    # SWAGGER
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]

