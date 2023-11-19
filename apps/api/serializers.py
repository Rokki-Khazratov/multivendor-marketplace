from django.forms import ImageField
from core import settings
from rest_framework import serializers
from apps.product.models import Cart, CartItem, Category, ParentCategory,Product,ProductCharacteristic, CharacteristicImage
from apps.seller.models import Seller,SellerApplication
from .models import DocumentationSection
from apps.user.models import Favorites, Review
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from apps.user.models import UserProfile
from django.db.models import Avg

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile  




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







# class ProductSerializer(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField()
#     price = serializers.SerializerMethodField()
#     discount_price = serializers.SerializerMethodField()
#     rating = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'seller', 'category', 'images', 'price', 'discount_price', 'rating')

#     # def get_images(self, obj):
#     #     if obj.productcharacteristic_set.exists():
#     #         first_characteristic = obj.productcharacteristic_set.first()
#     #         return [settings.BASE_URL + image.image.url for image in first_characteristic.images.all()]

#     def get_price(self, obj):
#         if obj.productcharacteristic_set.exists():
#             return obj.productcharacteristic_set.first().price
#         return None

#     def get_discount_price(self, obj):
#         if obj.productcharacteristic_set.exists():
#             return obj.productcharacteristic_set.first().discount_price
#         return None

#     def get_rating(self, obj):
#         if obj.reviews.exists():
#             average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
#             return round(average_rating, 1)
#         return None

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'seller', 'category', 'images', 'price', 'discount_price', 'rating')

    def get_images(self, obj):
        first_characteristic = obj.productcharacteristic_set.first()
        if first_characteristic:
            return [settings.BASE_URL + image.image.url for image in first_characteristic.images.all()]
        return []

    def get_price(self, obj):
        first_characteristic = obj.productcharacteristic_set.first()
        return first_characteristic.price if first_characteristic else None

    def get_discount_price(self, obj):
        first_characteristic = obj.productcharacteristic_set.first()
        return first_characteristic.discount_price if first_characteristic else None

    def get_rating(self, obj):
        if obj.reviews.exists():
            average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(average_rating, 1)
        return None







        




class ProductDetailSerializer(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_characteristics(self, obj):
        characteristics = []
        for characteristic in obj.productcharacteristic_set.all():
            characteristic_data = {
                'name': characteristic.name,
                'value': characteristic.value,
                'price': characteristic.price,
                'discount_price': characteristic.discount_price,
                'images': self.get_resized_images(characteristic.characteristicimage_set.all())
            }
            characteristics.append(characteristic_data)
        return characteristics

    def get_resized_images(self, images):
        resized_images = []
        for image in images:
            original_url = settings.BASE_URL + image.image.url

            middle_image = self.resize_image(image.image, 2)
            middle_url = self.save_resized_image(image, middle_image)

            low_image = self.resize_image(image.image, 4)
            low_url = self.save_resized_image(image, low_image)

            resized_images.append({
                'original': original_url,
                'middle': middle_url,
                'low': low_url
            })

        return resized_images

    def resize_image(self, original_image, factor):
        pil_image = Image.open(original_image.path)

        resized_image = pil_image.resize(
            (pil_image.width // factor, pil_image.height // factor)
        )

        output_io = BytesIO()
        resized_image.save(output_io, format='PNG')
        output_io.seek(0)
        return output_io

    def save_resized_image(self, image_instance, resized_io):
        image_instance.image.save(f'resized_{image_instance.image.name}', ContentFile(resized_io.read()), save=False)
        return settings.BASE_URL + image_instance.image.url

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
        fields = ['id', 'rating', 'info', 'created_at', 'user', 'product', 'images']

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_images(self, obj):
        return image_urls


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
    def map_premium_tariff(self, obj):
        if obj.premium_tariff == 'basic':
            return 1
        elif obj.premium_tariff == 'standard':
            return 2
        elif obj.premium_tariff == 'premium':
            return 3
        return None

    premium_tariff = serializers.SerializerMethodField(method_name='map_premium_tariff')

    class Meta:
        model = Seller
        fields = (
            'id', 'premium_tariff', 'store_name', 'address',
            'phone_number', 'created_at', 'updated_at', 'user'
        )



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

class UserProfileSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(source='user')
    class Meta:
        model = UserProfile
        fields = '__all__'