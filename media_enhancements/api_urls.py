from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CustomImageViewSet, CustomDocumentViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'images', CustomImageViewSet, basename='image')
router.register(r'documents', CustomDocumentViewSet, basename='document')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
