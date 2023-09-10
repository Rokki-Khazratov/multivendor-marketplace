from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import *
from .serializers import *
from rest_framework import filters

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filtering by category ID
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)


        # Filtering by name
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        # Filtering by price range
        price_range = self.request.query_params.get('price')
        if price_range:
            min_price, max_price = price_range.split('-')
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)


        # Filtering by quantity
        quantity_range = self.request.query_params.get('quantity')
        if quantity_range:
            min_price, max_price = quantity_range.split('-')
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        # Filtering by in the cart or not
        # in_cart = self.request.query_params.get('in_cart')
        # if in_cart:
        #     user = self.request.user  # Assuming you have authentication
        #     if in_cart == 'true':
        #         queryset = queryset.filter(cartitem__user=user)
        #     else:
        #         queryset = queryset.exclude(cartitem__user=user)

        return queryset

class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SellerListCreateView(ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class SellerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer