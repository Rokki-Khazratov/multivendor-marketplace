from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.api.views import *
from apps.seller.views import *
from apps.user.views import *
from apps.product.views import *

urlpatterns = [
    
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-rud'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('product-characteristics/', ProductCharacteristicList.as_view(), name='product-characteristics-list'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-rud'),

    path('product/<int:pk>/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('product/<int:pk>/remove-from-cart/', remove_from_cart, name='remove-from-cart'),

    path('product/add-to-favorites/', AddToFavoritesView.as_view(), name='add-to-favorites'),
    path('product/remove-from-favorites/', RemoveFromFavoritesView.as_view(), name='remove-from-favorites'),



    path('sellers/', SellerListCreateView.as_view(), name='sellers-list-create'),
    path('seller/<int:pk>/', SellerRetrieveUpdateDestroyView.as_view(), name='seller-rud'),

    path('seller-application/', SellerApplicationCreateView.as_view(), name='seller-application-create'),

    path('seller-applications/', SellerApplicationListView.as_view(), name='seller-application-list'),
    path('seller-application/<int:pk>/', SellerApplicationDetailView.as_view(), name='seller-application-detail'),

    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('user/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('docs/', DocumentationSectionList.as_view(), name='documentation-api'),

]