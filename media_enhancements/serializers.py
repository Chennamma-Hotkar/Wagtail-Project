from rest_framework import serializers
from .models import CustomImage, CustomDocument, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class CustomImageSerializer(serializers.ModelSerializer):
    """Serializer for CustomImage model."""
    
    categories = CategorySerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomImage
        fields = [
            'id', 'title', 'file_url', 'width', 'height',
            'created_at', 'copyright_holder', 'source_url',
            'categories', 'alt_text_override', 'tags'
        ]
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class CustomDocumentSerializer(serializers.ModelSerializer):
    """Serializer for CustomDocument model."""
    
    tags = serializers.StringRelatedField(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomDocument
        fields = [
            'id', 'title', 'file_url', 'file_size', 'created_at',
            'document_version', 'expiry_date', 'department', 'tags'
        ]
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def get_file_size(self, obj):
        if obj.file:
            return obj.file.size
        return None
