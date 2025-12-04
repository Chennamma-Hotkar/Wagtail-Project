from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomImage, CustomDocument, Category
from .serializers import (
    CustomImageSerializer,
    CustomDocumentSerializer,
    CategorySerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class CustomImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing images.
    Supports filtering, searching, and ordering.
    """
    queryset = CustomImage.objects.all()
    serializer_class = CustomImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories__slug']
    search_fields = ['title', 'tags__name', 'copyright_holder']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recently uploaded images."""
        recent_images = self.queryset.order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_images, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        """Get images related to this one (by category)."""
        image = self.get_object()
        related = CustomImage.objects.filter(
            categories__in=image.categories.all()
        ).exclude(id=image.id).distinct()[:5]
        serializer = self.get_serializer(related, many=True)
        return Response(serializer.data)


class CustomDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing documents.
    Supports filtering, searching, and ordering.
    """
    queryset = CustomDocument.objects.all()
    serializer_class = CustomDocumentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department']
    search_fields = ['title', 'tags__name', 'department']
    ordering_fields = ['created_at', 'title', 'expiry_date']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recently uploaded documents."""
        recent_docs = self.queryset.order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_docs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get documents expiring within 30 days."""
        from django.utils import timezone
        from datetime import timedelta
        
        thirty_days = timezone.now().date() + timedelta(days=30)
        expiring = self.queryset.filter(
            expiry_date__lte=thirty_days,
            expiry_date__gte=timezone.now().date()
        ).order_by('expiry_date')
        
        serializer = self.get_serializer(expiring, many=True)
        return Response(serializer.data)
