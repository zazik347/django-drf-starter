from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import ExampleItem
from .serializers import ExampleItemSerializer
from .permissions import IsAuthorOrReadOnly

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = ExampleItem.objects.all()
    serializer_class = ExampleItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExampleItem.objects.all()
    serializer_class = ExampleItemSerializer
    permission_classes = [IsAuthorOrReadOnly]
