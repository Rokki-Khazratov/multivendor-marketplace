from rest_framework import serializers
from apps.product.models import Cart, CartItem, Category,Product,ProductCharacteristic, CharacteristicImage
from apps.seller.models import Seller,SellerApplication
from .models import DocumentationSection
from apps.user.models import Favorites
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError





class CharacteristicImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicImage
        fields = '__all__'


class OneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicImage
        fields = ('image',)

class ProductCharacteristicSerializer(serializers.ModelSerializer):
    images = OneImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCharacteristic
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'seller','rating', 'category', 'main_image', 'prices')

    def get_main_image(self, obj):
        main_image = None
        for characteristic in obj.productcharacteristic_set.all():
            images = characteristic.characteristicimage_set.all()
            if images:
                main_image = images[0].image.url
                break
        return main_image

    def get_prices(self, obj):
        characteristics = []
        for characteristic in obj.productcharacteristic_set.all():
            characteristics.append({
                # 'name': characteristic.name,
                # 'value': characteristic.value,
                'price': characteristic.price,
                'discount_price': characteristic.discount_price,
            })
        return characteristics







class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(source='get_total_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'





class AddToFavoritesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class RemoveFromFavoritesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['user', 'favorite_products']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class SellerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerApplication
        fields = '__all__'


class DocumentationSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentationSection
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')

        if len(password) < 8:
            raise ValidationError('Пароль должен содержать более 8 символов.')


        return data