from rest_framework.generics import ListCreateAPIView,CreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.product.models import Cart,CartItem, CharacteristicQuantity, ProductCharacteristic
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from .models import *


class DocumentationSectionList(ListAPIView):
    serializer_class = DocumentationSectionSerializer

    def get_queryset(self):
        return DocumentationSection.objects.filter(parent_section__isnull=True)


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
        return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

    # Предположим, у вас есть конкретный идентификатор характеристики продукта
    characteristic_id = request.data.get('characteristic_id')

    try:
        characteristic = ProductCharacteristic.objects.get(pk=characteristic_id)
    except ProductCharacteristic.DoesNotExist:
        return Response({'error': 'Характеристика не найдена'}, status=status.HTTP_404_NOT_FOUND)

    # Проверьте, совпадает ли выбранное количество с доступным количеством в характеристике
    if characteristic.quantity < quantity:
        return Response({'error': f'Недостаточное количество на складе для характеристики: {characteristic.name}'}, status=status.HTTP_400_BAD_REQUEST)

    # Создайте CartItem и свяжите его с продуктом и характеристикой
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.characteristic_quantities.add(characteristic)
    cart_item.quantity += quantity
    cart_item.save()

    # Уменьшите количество в характеристике соответственно
    characteristic.quantity -= quantity
    characteristic.save()

    return Response({'message': 'Продукт успешно добавлен в корзину'}, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, pk):
    try:
        # Найти корзину, связанную с аутентифицированным пользователем
        cart = Cart.objects.get(user=request.user)

        # Найти элемент корзины, который нужно удалить на основе первичного ключа продукта
        cart_item = CartItem.objects.get(cart=cart, product__pk=pk)

        # Уменьшить количество элемента корзины на 1
        cart_item.quantity -= 1

        # Убедиться, что количество не становится меньше нуля
        if cart_item.quantity < 0:
            cart_item.quantity = 0

        # Найти продукт, связанный с элементом корзины
        product = cart_item.product

        # Удалить одну характеристику из корзины и вернуть ее к продукту
        product_characteristics = cart_item.characteristics.all()
        if product_characteristics:
            characteristic_to_return = product_characteristics.first()
            characteristic_to_return.quantity += 1
            characteristic_to_return.save()
            cart_item.characteristics.remove(characteristic_to_return)

        # Сохранить элемент корзины
        cart_item.save()

        # По желанию, можно также полностью удалить элемент корзины, если его количество становится равным нулю
        if cart_item.quantity == 0:
            cart_item.delete()

        return Response({'message': 'Продукт успешно удален из корзины'}, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({'error': 'Корзина не найдена'}, status=status.HTTP_404_NOT_FOUND)

    except CartItem.DoesNotExist:
        return Response({'error': 'Продукт не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)
























class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = Category.objects.all()  # Use .all() to avoid caching
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset    

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_characteristic_to_cart(request, cart_item_id, characteristic_id):
#     try:
#         cart_item = CartItem.objects.get(pk=cart_item_id)
#         characteristic = ProductCharacteristic.objects.get(pk=characteristic_id)
        
#         # Проверьте, есть ли уже запись CharacteristicQuantity для этой характеристики в этом CartItem
#         characteristic_quantity, created = CharacteristicQuantity.objects.get_or_create(
#             cart_item=cart_item,
#             characteristic=characteristic,
#         )

#         # Увеличьте количество в CharacteristicQuantity
#         characteristic_quantity.quantity += 1
#         characteristic_quantity.save()

#         return Response({'message': 'Характеристика успешно добавлена в корзину'}, status=status.HTTP_200_OK)
#     except CartItem.DoesNotExist:
#         return Response({'error': 'Элемент корзины не найден'}, status=status.HTTP_404_NOT_FOUND)
#     except ProductCharacteristic.DoesNotExist:
#         return Response({'error': 'Характеристика не найдена'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def remove_characteristic_from_cart(request, cart_item_id, characteristic_id):
#     try:
#         cart_item = CartItem.objects.get(pk=cart_item_id)
#         characteristic = ProductCharacteristic.objects.get(pk=characteristic_id)

#         try:
#             characteristic_quantity = CharacteristicQuantity.objects.get(
#                 cart_item=cart_item,
#                 characteristic=characteristic,
#             )

#             # Уменьшите количество в CharacteristicQuantity
#             if characteristic_quantity.quantity > 0:
#                 characteristic_quantity.quantity -= 1
#                 characteristic_quantity.save()
#             else:
#                 # Если количество стало меньше или равно 0, удалите запись CharacteristicQuantity
#                 characteristic_quantity.delete()

#             return Response({'message': 'Характеристика успешно удалена из корзины'}, status=status.HTTP_200_OK)
#         except CharacteristicQuantity.DoesNotExist:
#             return Response({'error': 'Характеристика не найдена в корзине'}, status=status.HTTP_404_NOT_FOUND)
#     except CartItem.DoesNotExist:
#         return Response({'error': 'Элемент корзины не найден'}, status=status.HTTP_404_NOT_FOUND)
#     except ProductCharacteristic.DoesNotExist:
#         return Response({'error': 'Характеристика не найдена'}, status=status.HTTP_404_NOT_FOUND)
