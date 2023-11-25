from rest_framework.generics import ListCreateAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.product.models import ProductCharacteristic
from django.db.models import F, Sum
from django.db.models import OuterRef, Subquery


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

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        seller = self.request.query_params.get('seller')
        if seller:
            queryset = queryset.filter(seller=seller)


        price_range = self.request.query_params.get('price')
        if price_range:
            min_price, max_price = price_range.split('-')
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        characteristic_value = self.request.query_params.get('characteristic')
        if characteristic_value:
            queryset = queryset.filter(characteristics__value=characteristic_value)
            queryset = queryset.annotate(
                characteristic_price=F('characteristics__price')
            ).order_by('characteristic_price')

        # subquery = ProductImage.objects.filter(product=OuterRef('pk')).order_by('characteristic_id').values('image')[:1]
        # queryset = queryset.annotate(main_image=Subquery(subquery))

        return queryset

class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class CharacteristicImageListCreateView(ListCreateAPIView):
    queryset = CharacteristicImage.objects.all()
    serializer_class = CharacteristicImageSerializer

class CharacteristicImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CharacteristicImage.objects.all()
    serializer_class = CharacteristicImageSerializer


class ProductCharacteristicList(ListCreateAPIView):
    serializer_class = ProductCharacteristicSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            return ProductCharacteristic.objects.filter(product=product_id)
        else:
            return ProductCharacteristic.objects.all()





class ParentCategoryListCreateView(ListCreateAPIView):
    serializer_class = ParentCategorySerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = ParentCategory.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset    

class ParentCategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer



class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name')
        parent = self.request.query_params.get('parent')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if parent:
            queryset = queryset.filter(parent__name__icontains=parent)

        return queryset

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer