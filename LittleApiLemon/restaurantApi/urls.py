from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *
#! Some names might be different but the main functionality work

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Items & cato
    path("menu-items", MenuList.as_view(), name="menu-Items"),
    path("catagories", CatagoriesView.as_view(), name="catagories"),
    path("catagories/<str:cato>", SpecCatagorieView.as_view(), name="specCatagories"),
    path("cart", CartView.as_view(), name="cart"),

    # customers & drivers
    path("driver", drivers.as_view(), name="driver"),
    path("orders", ListOrder.as_view(), name="orders"),


    # Users
    path("users", UserList.as_view(), name="users"),
    path("register", RegisterApi.as_view(), name='register'),
    path("add-manager", SetManager.as_view(), name="add-manager"),
]
