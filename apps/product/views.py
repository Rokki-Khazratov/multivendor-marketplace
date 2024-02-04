from django.shortcuts import get_object_or_404
from apps.product.serializers import ProductPostSerializer, ProductSerializer
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
from apps.api.serializers import  CartItemSerializer,CharacteristicQuantitySerializer
from django.db.models import F, Sum



from django.db.models import F, Sum

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        return CartItem.objects.filter(cart__user__id=user_id)






from django.db.models import F

class CartItemCreateView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        return CartItem.objects.filter(user_profile__id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        annotated_queryset = CartItem.objects.filter(
            id__in=queryset.values_list('id', flat=True)
        ).annotate(
            cart_item_name=F('characteristics__name'),
            cart_item_value=F('characteristics__value'),
            cart_item_price=F('characteristics__price'),
            cart_item_discount_price=F('characteristics__discount_price'),
            cart_item_image=F('characteristics__characteristic_images__image'),
            cart_item_parent_product_id=F('product__id'),
            cart_item_product_name=F('product__name')
        ).values('id', 'cart_item_name', 'cart_item_value', 'cart_item_price', 'cart_item_discount_price', 'cart_item_image', 'cart_item_parent_product_id', 'cart_item_product_name').annotate(
            quantity=Sum('quantity')
        )

        formatted_data = list(annotated_queryset)

        # Update image URLs with settings.BASE_URL
        for item in formatted_data:
            if item['cart_item_image']:
                item['cart_item_image'] = settings.BASE_URL + 'storage/' + item['cart_item_image']

        print(f"Formatted Data: {formatted_data}")

        return Response(formatted_data)

@api_view(['POST'])
def add_to_cart(request, id, pk):
    quantities = request.data.get('quantity', 1)
    characteristic_ids = request.data.get('characteristic_id', [])

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

    # Проверка, что все указанные характеристики существуют и принадлежат выбранному продукту
    characteristics = ProductCharacteristic.objects.filter(pk__in=characteristic_ids, product=product)
    if characteristics.count() != len(characteristic_ids):
        return Response({'error': 'Одна или несколько характеристик не найдены у выбранного продукта'}, status=status.HTTP_404_NOT_FOUND)

    user_profile = get_object_or_404(UserProfile, id=id)

    for characteristic in characteristics:
        if characteristic.quantity < int(quantities):
            return Response({'error': f'Недостаточное количество на складе для характеристики: {characteristic.name}'}, status=status.HTTP_400_BAD_REQUEST)

        # Создание или обновление CartItem для каждой характеристики
        cart_item, created = CartItem.objects.get_or_create(user_profile=user_profile, product=product)
        cart_item.quantity = int(quantities)
        cart_item.save()

        # Очистка старых характеристик и добавление новых
        cart_item.characteristics.clear()
        cart_item.characteristics.add(*characteristics)

    return Response({'message': 'Продукт успешно добавлен в корзину'}, status=status.HTTP_200_OK)





@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def remove_from_cart(request, id, pk):
    try:
        user_profile = get_object_or_404(UserProfile, id=id)
        cart_item = CartItem.objects.get(user_profile=user_profile, product__pk=pk)

        cart_item.quantity -= 1

        if cart_item.quantity < 0:
            cart_item.quantity = 0

        product_characteristics = cart_item.characteristics.all()
        if product_characteristics:
            characteristic = product_characteristics.first()
            characteristic_quantity = characteristic.characteristicquantity_set.first()
            if characteristic_quantity:
                cart_item.characteristics.remove(characteristic)

        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

        return Response({'message': 'Продукт успешно удален из корзины'}, status=status.HTTP_200_OK)

    except CartItem.DoesNotExist:
        return Response({'error': 'Продукт не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)




class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductPostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Добавьте логику для сохранения изображений перед вызовом super().create()
        self.save_images(serializer)

        # Сохраните объект и получите ответ
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def save_images(self, serializer):
        for characteristic_data in serializer.validated_data.get('characteristics', []):
            for image_data in characteristic_data.get('images', []):
                image_instance = image_data.get('image')
                image_instance.save()
