from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.api.views import *
from apps.seller.views import *
from apps.user.views import *
from apps.product.views import *

urlpatterns = [
    #   ! product 
    path('parent_categories/', ParentCategoryListCreateView.as_view(), name='parentcategory-list-create'),
    path('parent_category/<int:pk>/', ParentCategoryRetrieveUpdateDestroyView.as_view(), name='parent-category-rud'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-rud'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/serach/', ProductListCreateView.as_view(), name='product-list-search'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-rud'),
    path('characteristics/', ProductCharacteristicList.as_view(), name='product-characteristics-list'),

    path('product-images/', CharacteristicImageListCreateView.as_view(), name='chatacterstic-image-list-create'),
    path('chatacterstic-image/<int:pk>/', CharacteristicImageRetrieveUpdateDestroyView.as_view(), name='chatacterstic-image-rud'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),

    # path('carts/', CartListCreateView.as_view(), name='cart-list-create'),
    # path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    # path('cartitems/', CartItemCreateView.as_view(), name='cart-item-create'),
    # path('cartitems/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    # path('product/add-to-favorites/', AddToFavoritesView.as_view(), name='add-to-favorites'),
    # path('product/remove-from-favorites/', RemoveFromFavoritesView.as_view(), name='remove-from-favorites'),


    path('user/<int:id>/cartitems/', CartItemCreateView.as_view(), name='cart-item-create'),
    path('user/<int:id>/cartitems/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('user/<int:id>/add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('user/<int:id>/remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),


    #   !seller and user
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