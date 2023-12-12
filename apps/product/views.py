from django.shortcuts import get_object_or_404
from core import settings
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response format
        formatted_data = []
        for cart_item in serializer.data:
            for characteristic in cart_item['characteristics']:
                characteristic['image'] = self.get_characteristic_images(characteristic['id'])
                formatted_data.append(characteristic)

        return Response(formatted_data)

    def get_characteristic_images(self, characteristic_id):
        image_instances = CharacteristicImage.objects.filter(characteristic_id=characteristic_id)
        image_urls = [settings.BASE_URL + image_instance.image.url for image_instance in image_instances]
        return image_urls



class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        return CartItem.objects.filter(cart__user__id=user_id)
    # permission_classes = [IsAuthenticated]


# Assuming your URL configurations look like this:
# path('user/<int:id>/add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
# path('user/<int:id>/remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, id, pk):
    quantity = request.data.get('quantity', 1)

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

    user_profile = get_object_or_404(UserProfile, id=id)
    cart_item, created = CartItem.objects.get_or_create(user_profile=user_profile, product=product)
    cart_item.characteristic_quantities.create(characteristic=characteristic, quantity=quantity)

    characteristic.quantity -= quantity
    characteristic.save()

    return Response({'message': 'Продукт успешно добавлен в корзину'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, id, pk):
    try:
        user_profile = get_object_or_404(UserProfile, id=id)
        cart_item = CartItem.objects.get(user_profile=user_profile, product__pk=pk)

        cart_item.quantity -= 1

        if cart_item.quantity < 0:
            cart_item.quantity = 0

        product_characteristic_quantities = cart_item.characteristic_quantities.all()
        if product_characteristic_quantities:
            characteristic_quantity = product_characteristic_quantities.first()
            characteristic_quantity.quantity += 1
            characteristic_quantity.save()
            cart_item.characteristic_quantities.remove(characteristic_quantity)

        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

        return Response({'message': 'Продукт успешно удален из корзины'}, status=status.HTTP_200_OK)

    except CartItem.DoesNotExist:
        return Response({'error': 'Продукт не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)





