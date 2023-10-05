from rest_framework import generics,permissions
from .models import SellerApplication,Seller
from apps.api.serializers import SellerApplicationSerializer


class SellerApplicationCreateView(generics.CreateAPIView):
    queryset = SellerApplication.objects.all()
    serializer_class = SellerApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
     

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')


class SellerApplicationListView(generics.ListCreateAPIView):
    queryset = SellerApplication.objects.all()
    serializer_class = SellerApplicationSerializer
    permission_classes = [permissions.IsAdminUser]

class SellerApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SellerApplication.objects.all()
    serializer_class = SellerApplicationSerializer
    permission_classes = [permissions.IsAdminUser]