from django.urls import path
from rest_framework_simplejwt import views as jwt_v


from .views import (
    ViewClient,
    ViewProduct,
    ViewSignUp,
    viewFileClients
)

urlpatterns = [
    path('token/', jwt_v.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_v.TokenRefreshView.as_view(), name='token_refresh'),
    path('signin/', ViewSignUp.as_view(), name='signin'),
    path('client/', ViewClient.as_view(), name='one_client'),
    path('product/', ViewProduct.as_view(), name='one_product'),
    path('clients/', viewFileClients.as_view(), name='file_clients')
]
