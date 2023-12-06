from django.http import HttpResponseBadRequest
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.product.models import ProductCharacteristic
from django.db.models import F, Sum
from django.db.models import OuterRef, Subquery


from .serializers import *
from .models import *

class YourProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print(f"Response status code: {response.status_code}")

        return response


class CustomPagination(PageNumberPagination):
    page_size = 20  #the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 2000

class DocumentationSectionList(ListAPIView):
    serializer_class = DocumentationSectionSerializer

    def get_queryset(self):
        return DocumentationSection.objects.filter(parent_section__isnull=True)
    

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter] 
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category_id')
        name = self.request.query_params.get('name')
        seller = self.request.query_params.get('seller')
        price_range = self.request.query_params.get('price')
        characteristic_value = self.request.query_params.get('characteristic')

        try:
            print("try")
            if category_id:
                print("category_id exists:", category_id)
                # Convert category_id to an actual Category instance
                category_id = int(category_id)
                category = Category.objects.get(id=category_id)
                queryset = queryset.filter(category=category)
                print("Category filtered:", queryset)
            else:
                print("else")
        except ValueError:
            print("error")
            return HttpResponseBadRequest("Invalid category_id. Must be an integer.")


        if name:
            queryset = queryset.filter(name__icontains=name)

        if seller:
            queryset = queryset.filter(seller=seller)


        if price_range:
            min_price, max_price = price_range.split('-')
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        if characteristic_value:
            queryset = queryset.filter(characteristics__value=characteristic_value)
            queryset = queryset.annotate(
                characteristic_price=F('characteristics__price')
            ).order_by('characteristic_price')

        # subquery = ProductImage.objects.filter(product=OuterRef('pk')).order_by('characteristic_id').values('image')[:1]
        # queryset = queryset.annotate(main_image=Subquery(subquery))

        return queryset
    
    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     print(f"Serializer data: {response.data}")
    #     return response


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