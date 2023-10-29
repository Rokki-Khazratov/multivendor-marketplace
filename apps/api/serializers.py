from core import settings
from rest_framework import serializers
from apps.product.models import Cart, CartItem, Category,Product,ProductCharacteristic, CharacteristicImage
from apps.seller.models import Seller,SellerApplication
from .models import DocumentationSection
from apps.user.models import Favorites, Review
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.db.models import Avg




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

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
    # image = serializers.SerializerMethodField()
    # price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    # characteristics = ProductCharacteristicSerializer(many=True, read_only=True)  # Include 'characteristics' field

    class Meta:
        model = Product
        fields = ('id', 'name', 'seller', 'category',  'rating', 'characteristics')  # Include 'characteristics' field in 'fields'


    # def get_image(self, obj):
    #     image = None
    #     for characteristic in obj.productcharacteristic_set.all():
    #         images = characteristic.characteristicimage_set.all()
    #         if images:
    #             image = settings.BASE_URL + images[0].image.url
    #             break
    #     return image

    # def get_price(self, obj):
    #     main_price = None
    #     # main_discount_price = None
    #     for characteristic in obj.productcharacteristic_set.all():
    #         prices = characteristic.characteristicprice_set.all()
    #         if prices:
    #             main_price = prices[0].price
    #             main_discount_price = prices[0].discount_price
    #             break
    #     return  prices
    #     {
    #         'main_price': main_price,
    #         'main_discount_price': main_discount_price
    #     }


    def get_rating(self, obj):
        if obj.reviews.exists():
            average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(average_rating, 1)
        else:
            return None



        




class ProductDetailSerializer(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)  

    class Meta:
        model = Product
        fields ='__all__'

    def get_characteristics(self, obj):
        images = []
        for characteristic in obj.productcharacteristic_set.all():
            characteristic_data = {
                'name': characteristic.name,
                'value': characteristic.value,
                'price': characteristic.price,
                'discount_price': characteristic.discount_price,
                'images': []  # Создайте список для изображений внутри характеристики
            }
            for image in characteristic.characteristicimage_set.all():
                characteristic_data['images'].append(image.image.url)
            images.append(characteristic_data)
        return images

    def get_rating(self, obj):
        if obj.reviews.exists():
            average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(average_rating, 1) 
        else:
            return None








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

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


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