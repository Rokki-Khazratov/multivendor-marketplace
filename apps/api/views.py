from rest_framework.generics import ListCreateAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from apps.product.models import Cart,CartItem
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer  

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return user


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, pk):
    quantity = request.data.get('quantity', 1)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if product.quantity < quantity:
        return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += quantity
    product.quantity -= quantity
    cart_item.save()
    product.save()

    return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, pk):
    try:
        # Find the cart associated with the authenticated user
        cart = Cart.objects.get(user=request.user)

        # Find the cart item to remove based on the product's primary key
        cart_item = CartItem.objects.get(cart=cart, product__pk=pk)

        # Reduce the cart item's quantity by 1 (you can adjust the logic here)
        cart_item.quantity -= 1

        # Ensure the quantity doesn't go below zero
        if cart_item.quantity < 0:
            cart_item.quantity = 0

        # Save the cart item
        cart_item.save()

        # Optionally, you can also remove the cart item completely if its quantity reaches zero
        if cart_item.quantity == 0:
            cart_item.delete()

        return Response({'message': 'Product removed from cart successfully'}, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    except CartItem.DoesNotExist:
        return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)


















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