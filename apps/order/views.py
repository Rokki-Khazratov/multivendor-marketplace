# views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Order, OrderHistory
from .serializers import OrderSerializer, OrderHistorySerializer

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderHistoryListCreateView(ListCreateAPIView):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer

class OrderHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer
