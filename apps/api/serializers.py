from core import settings
from rest_framework import serializers
from apps.product.models import Cart, CartItem, Category, ParentCategory,Product,ProductCharacteristic, CharacteristicImage
from apps.seller.models import Seller,SellerApplication
from .models import DocumentationSection
from apps.user.models import Favorites, Review
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.db.models import Avg




class ReviewSerializer(serializers.ModelSerializer):
    # user_name:
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
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'seller', 'category', 'image', 'price','discount_price', 'rating')

    def get_image(self, obj):
        image = None
        for characteristic in obj.productcharacteristic_set.all():
            images = characteristic.characteristicimage_set.all()
            if images:
                image = settings.BASE_URL + images[0].image.url
                break
        return image

    def get_price(self, obj):
        price = None
        for characteristic in obj.productcharacteristic_set.all():
            price = characteristic.price
            break
        return price

    def get_discount_price(self, obj):
        discount_price = None
        for characteristic in obj.productcharacteristic_set.all():
            discount_price = characteristic.discount_price
            break
        return discount_price

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
        fields = '__all__'

    def get_characteristics(self, obj):
        characteristics = []
        for characteristic in obj.productcharacteristic_set.all():
            characteristic_data = {
                'name': characteristic.name,
                'value': characteristic.value,
                'price': characteristic.price,
                'discount_price': characteristic.discount_price,
                'images': [settings.BASE_URL + image.image.url for image in characteristic.characteristicimage_set.all()]
            }
            characteristics.append(characteristic_data)
        return characteristics

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
    user = serializers.SerializerMethodField()  # Custom field for user data
    images = serializers.SerializerMethodField()  # Custom field for image URLs

    class Meta:
        model = Review
        fields = ['id', 'rating', 'info', 'created_at', 'user', 'product', 'images']

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_images(self, obj):
        # Assuming you have a related field 'images' on the Review model, adjust this accordingly
        image_urls = [settings.BASE_URL + image.image.url for image in obj.images.all()]  # Adjust for your image field
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