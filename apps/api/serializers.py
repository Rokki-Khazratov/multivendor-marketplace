from rest_framework import serializers
from apps.product.models import Category,Product
from apps.seller.models import Seller,SellerApplication
from .models import DocumentationSection
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
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
        fields = ('username', 'password')
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