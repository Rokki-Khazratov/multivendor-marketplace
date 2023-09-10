from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-rud'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-rud'),

    path('sellers/', SellerListCreateView.as_view(), name='sellers-list-create'),
    path('seller/<int:pk>/', SellerRetrieveUpdateDestroyView.as_view(), name='seller-rud'),
]