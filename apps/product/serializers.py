import os
from core import settings
from rest_framework import serializers
from apps.product.models import CartItem, Category, CharacteristicQuantity, ParentCategory,Product,ProductCharacteristic, CharacteristicImage
from apps.seller.models import Seller,SellerApplication
from apps.api.models import DocumentationSection
from apps.user.models import Favorites, Review, ReviewImage
from django.contrib.auth.models import User
from django.db.models import Avg

from apps.user.models import UserProfile
from PIL import Image
from io import BytesIO

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
    characteristics = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'is_published', 'updated_at', 'seller', 'category', 'characteristics', 'rating')

    def get_seller(self, obj):
        seller = obj.seller
        return {
            "id": seller.id,
            "store_name": seller.store_name,
            "premium_tariff": seller.premium_tariff,
        }

    def get_category(self, obj):
        category = obj.category
        return {
            "id": category.id,
            "name": category.name,
        }
    


    def get_characteristics(self, obj):
        characteristics = []
        for characteristic in obj.productcharacteristic_set.all():
            characteristic_data = self.get_characteristic_data(characteristic)
            characteristic_data['images'] = self.get_characteristic_images(characteristic.characteristic_images.all())
            characteristics.append(characteristic_data)
        return characteristics
    
    def get_resized_image_url(self, image_instance, resolution):
        def get_resized_url(image_path, resolution):
            base_url, extension = os.path.splitext(image_path)

            if resolution == 'middle':
                size = (200, 200)
            elif resolution == 'low':
                size = (100, 100)
            else:
                size = Image.open(image_path).size

            resized_image = Image.open(image_path).resize(size)
            output_buffer = BytesIO()
            resized_image.save(output_buffer, format='PNG')
            resized_url = settings.BASE_URL + image_instance.image.url.replace('original', resolution)

            return resized_url

        if image_instance:
            original_path = image_instance.image.path
            print(f"Original Image Path: {original_path}")  # Add this line for debugging

            if os.path.exists(original_path):
                return get_resized_url(original_path, resolution)
            else:
                print(f"Error: File does not exist at {original_path}")

        return None

    def get_characteristic_images(self, images):
        return [
            {
                'middle': self.get_resized_image_url(image, 'middle'),
            }
            for image in images
        ]
    
    def get_characteristic_images_data(self, images):
        return [
            {
                'original': self.get_resized_image_url(image, 'original'),
                'middle': self.get_resized_image_url(image, 'middle'),
                'low': self.get_resized_image_url(image, 'low'),
            }
            for image in images
        ]


    def get_characteristic_data(self, characteristic):
        return {
            'characteristic_id': characteristic.id,
            'name': characteristic.name,
            'value': characteristic.value,
            'price': characteristic.price,
            'discount_price': characteristic.discount_price,
            'images': self.get_characteristic_images_data(characteristic.characteristic_images.all())
        }


    def get_images_data(self, images):
        return [
            {
                'original': self.get_resized_image_url(image, 'original'),
                'middle': self.get_resized_image_url(image, 'middle'),
                'low': self.get_resized_image_url(image, 'low'),
            }
            for image in images
        ]
    



    def get_rating(self, obj):
        if obj.reviews.exists():
            average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(average_rating, 1)
        return None






        



class CharacteristicImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CharacteristicImage
        fields = ['image']

    def get_image(self, obj):
        return settings.BASE_URL + obj.image.url

    
class CharacteristicSerializer(serializers.ModelSerializer):
    images = CharacteristicImageSerializer(many=True, read_only=True)
    characteristic_id = serializers.CharField(source='id')

    class Meta:
        model = ProductCharacteristic
        fields = ['characteristic_id', 'images']

        
class CharacteristicDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    value = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductCharacteristic
        fields = ['characteristic_id', 'name', 'value', 'price', 'discount_price', 'image']

    def get_image(self, obj):
        return settings.BASE_URL + obj.images.first().image.url if obj.images.exists() else None




class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    is_published = serializers.BooleanField()
    updated_at = serializers.DateTimeField()
    seller = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()

    characteristics = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ['id', 'name', 'is_published', 'updated_at', 'seller', 'category', 'characteristics', 'reviews','total_rating']



    def get_seller(self, obj):
        seller = obj.seller
        return {'id': seller.id, 'store_name': seller.store_name, 'premium_tariff': seller.premium_tariff}
    
    def get_reviews(self, obj):
        reviews_data = self.get_reviews_data(obj.reviews.all())
        return reviews_data

    def get_review_images(self, images):
        return [
            {
                'original': settings.BASE_URL + image.image.url,
                'middle': self.get_resized_image_url(image, 'middle'),
                'low': self.get_resized_image_url(image, 'low'),
            }
            for image in images
        ]

    def get_reviews_data(self, product_reviews):
        reviews_data = []
        for review in product_reviews.all():
            review_data = {
                'review_id': review.id,
                'rating': review.rating,
                'info': review.info,
                'images': self.get_review_images(review.images.all()),  # Assuming Review has an 'images' field
            }
            reviews_data.append(review_data)
        return reviews_data



    def get_total_rating(self, obj):
        if obj.reviews.exists():
            average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(average_rating, 1)
        else:
            return None

    def get_category(self, obj):
        category = obj.category
        return {'id': category.id, 'name': category.name, }





    def get_characteristic_images(self, images):
        return [
            {
                'original': settings.BASE_URL + image.image.url,
                'middle': self.get_resized_image_url(image, 'middle'),
                'low': self.get_resized_image_url(image, 'low'),
            }
            for image in images
        ]


    def get_characteristics(self, obj):
        characteristics = []
        for characteristic in obj.productcharacteristic_set.all():
            characteristic_data = self.get_characteristic_data(characteristic)
            characteristic_data['images'] = self.get_characteristic_images(characteristic.characteristic_images.all())
            characteristics.append(characteristic_data)
        return characteristics

    def get_characteristic_data(self, characteristic):
        return {
            'characteristic_id': characteristic.id,
            'name': characteristic.name,
            'value': characteristic.value,
            'price': characteristic.price,
            'discount_price': characteristic.discount_price,
        }
    





    def get_resized_image_url(self, image_instance, resolution):
        if image_instance:
            original_image = Image.open(image_instance.image.path)

            if resolution == 'middle':
                size = (200, 200)  
            elif resolution == 'low':
                size = (100, 100)  
            else:
                size = original_image.size
            resized_image = original_image.resize(size)

            output_buffer = BytesIO()
            resized_image.save(output_buffer, format='PNG')

            resized_url = settings.BASE_URL + image_instance.image.url.replace('original', resolution)

            return resized_url

        return None
