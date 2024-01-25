import os
from apps.product.serializers import CharacteristicSerializer
from core import settings
from rest_framework import serializers
from apps.product.models import CartItem, Category, CharacteristicQuantity, ParentCategory,Product,ProductCharacteristic, CharacteristicImage
from apps.seller.models import Seller,SellerApplication
from .models import DocumentationSection
from apps.user.models import Favorites, Review, ReviewImage
from django.contrib.auth.models import User
from django.db.models import Avg

from apps.user.models import UserProfile
from PIL import Image
from io import BytesIO




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




class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
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
        fields = ['id', 'name']

class ParentCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ParentCategory
        fields = ['id', 'name', 'categories']



class SellerSerializer(serializers.ModelSerializer):

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

        profile, created = UserProfile.objects.get_or_create(user=user, defaults=profile_data)

        if not created:
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()

        return user


class CharacteristicImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = CharacteristicImage
        fields = ['image']



class CharacteristicQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicQuantity
        fields = ['id', 'characteristic', 'quantity']

class CartItemSerializer(serializers.ModelSerializer):
    cart_item_product_name = serializers.SerializerMethodField()
    characteristics = CharacteristicQuantitySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'cart_item_product_name', 'characteristics']

    def get_cart_item_product_name(self, obj):
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
                    if hasattr(cart_item_obj, 'characteristics'):
                        characteristics = cart_item_obj.characteristics.all()
                        if characteristics:
                            cart_item['characteristics'] = CharacteristicSerializer(characteristics, many=True).data
                except CartItem.DoesNotExist:
                    pass
        return ret