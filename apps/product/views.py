from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from apps.product.models import CartItem, ProductCharacteristic
from .models import *
from .models import  CartItem
from apps.api.serializers import  CartItemSerializer


# class CartListCreateView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     # permission_classes = [IsAuthenticated]

# class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     # permission_classes = [IsAuthenticated]

class CartItemCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [IsAuthenticated]

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [IsAuthenticated]



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, pk):
    quantity = request.data.get('quantity', 1)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

    characteristic_id = request.data.get('characteristic_id')

    try:
        characteristic = ProductCharacteristic.objects.get(pk=characteristic_id)
    except ProductCharacteristic.DoesNotExist:
        return Response({'error': 'Характеристика не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if characteristic.quantity < quantity:
        return Response({'error': f'Недостаточное количество на складе для характеристики: {characteristic.name}'}, status=status.HTTP_400_BAD_REQUEST)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.characteristic_quantities.add(characteristic)
    cart_item.quantity += quantity
    cart_item.save()
    characteristic.quantity -= quantity
    characteristic.save()

    return Response({'message': 'Продукт успешно добавлен в корзину'}, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, pk):
    try:
        cart = Cart.objects.get(user=request.user)

        cart_item = CartItem.objects.get(cart=cart, product__pk=pk)

        cart_item.quantity -= 1

        if cart_item.quantity < 0:
            cart_item.quantity = 0

        product = cart_item.product

        product_characteristics = cart_item.characteristics.all()
        if product_characteristics:
            characteristic_to_return = product_characteristics.first()
            characteristic_to_return.quantity += 1
            characteristic_to_return.save()
            cart_item.characteristics.remove(characteristic_to_return)

        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

        return Response({'message': 'Продукт успешно удален из корзины'}, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({'error': 'Корзина не найдена'}, status=status.HTTP_404_NOT_FOUND)

    except CartItem.DoesNotExist:
        return Response({'error': 'Продукт не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)