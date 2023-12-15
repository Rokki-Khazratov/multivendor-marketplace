from django.forms import ImageField
from core import settings
from rest_framework import serializers
from apps.product.models import CartItem, Category, ParentCategory,Product,ProductCharacteristic, CharacteristicImage
from apps.seller.models import Seller,SellerApplication
from .models import DocumentationSection
from apps.user.models import Favorites, Review, ReviewImage
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from apps.user.models import UserProfile
from django.db.models import Avg

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile  

from rest_framework import serializers
from PIL import Image
import os

# class ReviewSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     images = serializers.SerializerMethodField()

#     class Meta:
#         model = Review
#         fields = ['id', 'rating', 'info', 'created_at', 'user', 'product', 'images']

#     def get_user(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}"

#     def get_images(self, obj):
#         if obj.images.exists():
#             image_path = obj.images.first().image.path
#             low_resolution_path = self.get_low_resolution_path(image_path)
#             return low_resolution_path
#         return None

#     def get_low_resolution_path(self, original_path):
#         low_resolution_path = self.get_low_resolution_filename(original_path)

#         # Check if the low-resolution image already exists
#         if not os.path.exists(low_resolution_path):
#             img = Image.open(original_path)
#             img.thumbnail((100, 100))
#             img.save(low_resolution_path)

#         return low_resolution_path

#     def get_low_resolution_filename(self, original_path):
#         # Create a unique filename for the low-resolution image
#         base_name, extension = os.path.splitext(os.path.basename(original_path))
#         low_resolution_filename = f"low_resolution_{base_name}{extension}"
#         low_resolution_path = os.path.join("/storage/review_images/7/review_rokki_user", low_resolution_filename)
#         return low_resolution_path



class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'rating', 'info', 'created_at', 'user', 'product', 'images']

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_images(self, obj):
        if obj.images.exists():
            image_urls = [settings.BASE_URL + image.image.url for image in obj.images.all()]
            return image_urls
        return []


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['image']

class CharacteristicImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicImage
        fields = ("id","image")


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
    seller = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name','is_published','updated_at', 'seller', 'category', 'image', 'price', 'discount_price', 'rating')

    def get_seller(self, obj):
        seller = obj.seller
        return {
            "id": seller.id,
            "store_name": seller.store_name,
            # "created_at": seller.created_at,
            "premium_tariff": seller.premium_tariff,
        }

    def get_category(self, obj):
        category = obj.category
        return {
            "id": category.id,
            "name": category.name,
            "parent": category.parent.name,
        }


    def get_image(self, obj):
        # Use Subquery to get the first image URL directly in the query
        first_image_url = CharacteristicImage.objects.filter(
            characteristic__product=obj
        ).order_by('id').values('image').first()

        return settings.BASE_URL + 'storage/' + first_image_url['image'] if first_image_url else None

        
    def get_price(self, obj):
        if obj.productcharacteristic_set.exists():
            return obj.productcharacteristic_set.first().price
        return None

    def get_discount_price(self, obj):
        if obj.productcharacteristic_set.exists():
            return obj.productcharacteristic_set.first().discount_price
        return None

    def get_rating(self, obj):
        if obj.reviews.exists():
            average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(average_rating, 1)
        return None






        




class ProductDetailSerializer(serializers.ModelSerializer):
    characteristics = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    seller_name = serializers.SerializerMethodField()

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
                # 'images': self.get_resized_images(characteristic.characteristicimage_set.all()),
                'images': self.get_resized_images(characteristic.characteristic_images.all())

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

    def get_seller_name(self,obj):
        return obj.display_seller_name













class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

# class CartSerializer(serializers.ModelSerializer):
#     cart_items = CartItemSerializer(many=True, read_only=True)
#     total_price = serializers.DecimalField(source='get_total_price', max_digits=10, decimal_places=2, read_only=True)

#     class Meta:
#         model = Cart
#         fields = '__all__'





class AddToFavoritesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class RemoveFromFavoritesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['user', 'favorite_products']


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
    # def map_premium_tariff(self, obj):
    #     if obj.premium_tariff == 'basic':
    #         return 1
    #     elif obj.premium_tariff == 'standard':
    #         return 2
    #     elif obj.premium_tariff == 'premium':
    #         return 3
    #     return None

    # premium_tariff = serializers.SerializerMethodField(method_name='map_premium_tariff')

    class Meta:
        model = Seller
        fields = (
            'id', 'premium_tariff', 'store_name', 'address',
            'phone_number', 'created_at', 'updated_at', 'user','avatarka','background'
        )



class SellerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerApplication
        fields = '__all__'


class DocumentationSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentationSection
        fields = '__all__'







class UserAbstract(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone_number']


class UserSerializer(serializers.ModelSerializer):
    profile = UserAbstract(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile']
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

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)

        # Check if a UserProfile already exists for the user
        profile, created = UserProfile.objects.get_or_create(user=user, defaults=profile_data)

        # If the profile already existed, update its fields
        if not created:
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()

        return user









# class CharacteristicImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CharacteristicImage
#         fields = '__all__'


# class CharacteristicSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = ProductCharacteristic
#         fields = ['name', 'value', 'price', 'discount_price', 'image']

#     def get_image(self, obj):
#         first_image = obj.images.first()
#         return first_image.image.url if first_image else None


# class CartItemSerializer(serializers.ModelSerializer):
#     characteristics = CharacteristicSerializer(many=True, read_only=True, required=False)

#     class Meta:
#         model = CartItem
#         fields = ['id', 'quantity', 'product', 'characteristics']



# class UserProfileSerializer(serializers.ModelSerializer):
#     user_profile = UserSerializer(source='user')
#     cart_items = CartItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = '__all__'

#     def to_representation(self, instance):
#         ret = super().to_representation(instance)
#         for cart_item in ret['cart_items']:
#             cart_item_id = cart_item.get('id')
#             if cart_item_id:
#                 try:
#                     cart_item_obj = CartItem.objects.get(id=cart_item_id)
#                     characteristics = cart_item_obj.characteristics.all()
#                     if characteristics:
#                         cart_item['characteristics'] = CharacteristicSerializer(characteristics, many=True).data
#                 except CartItem.DoesNotExist:
#                     pass
#         return ret



class CharacteristicImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = CharacteristicImage
        fields = ['image']


class CharacteristicSerializer(serializers.ModelSerializer):
    # image = CharacteristicImageSerializer(source='images.first', read_only=True)

    class Meta:
        model = ProductCharacteristic
        fields = ['id','name', 'value', 'price', 'discount_price'
                #   , 'image'
                  ]
        
        
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    characteristics = CharacteristicSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product_name', 'characteristics']

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None





class UserProfileSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(source='user')
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for cart_item in ret['cart_items']:
            cart_item_id = cart_item.get('id')
            if cart_item_id:
                try:
                    cart_item_obj = CartItem.objects.get(id=cart_item_id)
                    characteristics = cart_item_obj.characteristics.all()
                    if characteristics:
                        cart_item['characteristics'] = CharacteristicSerializer(characteristics, many=True).data
                except CartItem.DoesNotExist:
                    pass
        return ret





