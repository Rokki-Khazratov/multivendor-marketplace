from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-rud'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-rud'),

    path('sellers/', SellerListCreateView.as_view(), name='sellers-list-create'),
    path('seller/<int:pk>/', SellerRetrieveUpdateDestroyView.as_view(), name='seller-rud'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api-login/', LoginView.as_view(), name='api-login'),
    path('api-register/', RegisterView.as_view(), name='api-register'),
    path('api-logout/', LogoutView.as_view(), name='api-logout'),

]