from rest_framework.generics import ListCreateAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.product.models import ProductCharacteristic
from .serializers import *
from .models import *


class DocumentationSectionList(ListAPIView):
    serializer_class = DocumentationSectionSerializer

    def get_queryset(self):
        return DocumentationSection.objects.filter(parent_section__isnull=True)

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        price_range = self.request.query_params.get('price')
        if price_range:
            min_price, max_price = price_range.split('-')
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        return queryset

class ProductImageListCreateView(ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ProductImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCharacteristicList(ListCreateAPIView):
    serializer_class = ProductCharacteristicSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            # Filter characteristics by the specified product
            return ProductCharacteristic.objects.filter(product=product_id)
        else:
            # If no product_id is provided, return all characteristics
            return ProductCharacteristic.objects.all()




class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset    

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer