from rest_framework.generics import CreateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from apps.api.serializers import *
from .models import *


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


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddToFavoritesView(APIView):
    def post(self, request, format=None):
        serializer = AddToFavoritesSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            user = request.user
            try:
                favorites = Favorites.objects.get(user=user)
            except Favorites.DoesNotExist:
                favorites = Favorites(user=user)
                favorites.save()
            
            favorites.favorite_products.add(product_id)
            return Response({'message': 'Product added to favorites successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveFromFavoritesView(APIView):
    def post(self, request, format=None):
        serializer = RemoveFromFavoritesSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            user = request.user
            try:
                favorites = Favorites.objects.get(user=user)
                favorites.favorite_products.remove(product_id)
                return Response({'message': 'Product removed from favorites successfully.'}, status=status.HTTP_200_OK)
            except Favorites.DoesNotExist:
                return Response({'error': 'Favorites not found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset


class ReviewRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
