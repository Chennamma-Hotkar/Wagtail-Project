"""
AI Auto-Tagging Module
Automatically suggests and applies tags to media files using AI
"""

import os
from PIL import Image
from io import BytesIO


class AIAutoTagger:
    """
    AI-powered auto-tagging for media files.
    Supports multiple AI backends: OpenAI, Hugging Face, or rule-based.
    """
    
    def __init__(self, backend='rule-based'):
        """
        Initialize auto-tagger with specified backend.
        
        Args:
            backend: 'openai', 'huggingface', or 'rule-based'
        """
        self.backend = backend
        self.api_key = None
        
        if backend == 'openai':
            from django.conf import settings
            self.api_key = getattr(settings, 'OPENAI_API_KEY', None)
    
    def tag_image(self, image_path, max_tags=5):
        """
        Generate tags for an image.
        
        Args:
            image_path: Path to image file
            max_tags: Maximum number of tags to return
        
        Returns:
            List of suggested tags
        """
        if self.backend == 'openai':
            return self._tag_image_openai(image_path, max_tags)
        elif self.backend == 'huggingface':
            return self._tag_image_huggingface(image_path, max_tags)
        else:
            return self._tag_image_rule_based(image_path, max_tags)
    
    def _tag_image_openai(self, image_path, max_tags=5):
        """Tag image using OpenAI Vision API."""
        try:
            import openai
            import base64
            
            if not self.api_key:
                return []
            
            openai.api_key = self.api_key
            
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Analyze this image and provide {max_tags} relevant tags or keywords that describe it. Return only the tags as a comma-separated list."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=100
            )
            
            # Parse response
            tags_text = response.choices[0].message.content
            tags = [tag.strip() for tag in tags_text.split(',')]
            
            return tags[:max_tags]
            
        except Exception as e:
            print(f"Error with OpenAI tagging: {e}")
            return []
    
    def _tag_image_huggingface(self, image_path, max_tags=5):
        """Tag image using Hugging Face models."""
        try:
            from transformers import pipeline
            from PIL import Image
            
            # Load image classification model
            classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
            
            # Load image
            image = Image.open(image_path)
            
            # Get predictions
            predictions = classifier(image, top_k=max_tags)
            
            # Extract labels
            tags = [pred['label'].replace('_', '-') for pred in predictions]
            
            return tags
            
        except Exception as e:
            print(f"Error with Hugging Face tagging: {e}")
            return []
    
    def _tag_image_rule_based(self, image_path, max_tags=5):
        """Tag image using rule-based analysis."""
        try:
            from PIL import Image
            import os
            
            tags = []
            
            # Open image
            img = Image.open(image_path)
            width, height = img.size
            
            # Aspect ratio tags
            aspect_ratio = width / height
            if 0.95 <= aspect_ratio <= 1.05:
                tags.append('square')
            elif aspect_ratio > 1.5:
                tags.append('landscape')
            elif aspect_ratio < 0.7:
                tags.append('portrait')
            
            # Size tags
            if width >= 3000 or height >= 3000:
                tags.append('high-resolution')
            elif width >= 1920 or height >= 1080:
                tags.append('hd')
            else:
                tags.append('standard')
            
            # Color analysis
            if img.mode == 'RGBA':
                tags.append('transparent')
            elif img.mode == 'L':
                tags.append('grayscale')
            else:
                # Analyze dominant colors
                img_small = img.resize((50, 50))
                pixels = list(img_small.getdata())
                
                # Calculate average brightness
                if img.mode == 'RGB':
                    avg_brightness = sum(sum(p) for p in pixels) / (len(pixels) * 3)
                    if avg_brightness > 200:
                        tags.append('bright')
                    elif avg_brightness < 80:
                        tags.append('dark')
            
            # File format
            format_lower = img.format.lower() if img.format else ''
            if format_lower in ['jpg', 'jpeg']:
                tags.append('photo')
            elif format_lower == 'png':
                tags.append('graphic')
            
            # Filename analysis
            filename = os.path.basename(image_path).lower()
            if 'logo' in filename:
                tags.append('logo')
            if 'banner' in filename:
                tags.append('banner')
            if 'icon' in filename:
                tags.append('icon')
            if 'hero' in filename:
                tags.append('hero-image')
            if 'thumb' in filename:
                tags.append('thumbnail')
            
            return tags[:max_tags]
            
        except Exception as e:
            print(f"Error with rule-based tagging: {e}")
            return []
    
    def tag_video(self, video_path, max_tags=5):
        """
        Generate tags for a video.
        
        Args:
            video_path: Path to video file
            max_tags: Maximum number of tags to return
        
        Returns:
            List of suggested tags
        """
        tags = []
        
        try:
            import os
            
            # Filename analysis
            filename = os.path.basename(video_path).lower()
            
            if 'promo' in filename:
                tags.append('promo-video')
            if 'tutorial' in filename:
                tags.append('tutorial')
            if 'demo' in filename:
                tags.append('demo')
            if 'intro' in filename:
                tags.append('intro')
            if 'outro' in filename:
                tags.append('outro')
            
            # Duration-based tags (if metadata available)
            # This would require video processing
            
            return tags[:max_tags]
            
        except Exception as e:
            print(f"Error tagging video: {e}")
            return []
    
    def tag_audio(self, audio_path, max_tags=5):
        """
        Generate tags for an audio file.
        
        Args:
            audio_path: Path to audio file
            max_tags: Maximum number of tags to return
        
        Returns:
            List of suggested tags
        """
        tags = []
        
        try:
            import os
            
            # Filename analysis
            filename = os.path.basename(audio_path).lower()
            
            if 'music' in filename:
                tags.append('music')
            if 'sfx' in filename or 'sound-effect' in filename:
                tags.append('sound-effect')
            if 'voice' in filename or 'vocal' in filename:
                tags.append('voice')
            if 'ambient' in filename:
                tags.append('ambient')
            if 'loop' in filename:
                tags.append('loop')
            
            # Genre detection from filename
            genres = ['rock', 'pop', 'jazz', 'classical', 'electronic', 'hip-hop']
            for genre in genres:
                if genre in filename:
                    tags.append(genre)
            
            return tags[:max_tags]
            
        except Exception as e:
            print(f"Error tagging audio: {e}")
            return []
    
    def tag_document(self, document_path, max_tags=5):
        """
        Generate tags for a document.
        
        Args:
            document_path: Path to document file
            max_tags: Maximum number of tags to return
        
        Returns:
            List of suggested tags
        """
        tags = []
        
        try:
            import os
            
            # File extension
            ext = os.path.splitext(document_path)[1].lower()
            
            if ext == '.pdf':
                tags.append('pdf')
            elif ext in ['.doc', '.docx']:
                tags.append('word-document')
            elif ext in ['.xls', '.xlsx']:
                tags.append('spreadsheet')
            elif ext in ['.ppt', '.pptx']:
                tags.append('presentation')
            
            # Filename analysis
            filename = os.path.basename(document_path).lower()
            
            if 'report' in filename:
                tags.append('report')
            if 'invoice' in filename:
                tags.append('invoice')
            if 'contract' in filename:
                tags.append('contract')
            if 'manual' in filename:
                tags.append('manual')
            if 'guide' in filename:
                tags.append('guide')
            
            return tags[:max_tags]
            
        except Exception as e:
            print(f"Error tagging document: {e}")
            return []
    
    def suggest_category(self, tags):
        """
        Suggest a category based on tags.
        
        Args:
            tags: List of tags
        
        Returns:
            Suggested category name
        """
        # Category mapping
        category_keywords = {
            'Graphics': ['graphic', 'design', 'illustration', 'vector'],
            'Photos': ['photo', 'photography', 'picture', 'image'],
            'Icons': ['icon', 'symbol', 'glyph'],
            'Logos': ['logo', 'brand', 'identity'],
            'Banners': ['banner', 'header', 'hero-image'],
            'Videos': ['video', 'promo-video', 'tutorial'],
            'Music': ['music', 'song', 'track'],
            'Sound Effects': ['sound-effect', 'sfx', 'audio'],
            'Documents': ['document', 'pdf', 'report'],
        }
        
        # Score each category
        scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for tag in tags if any(kw in tag.lower() for kw in keywords))
            if score > 0:
                scores[category] = score
        
        # Return highest scoring category
        if scores:
            return max(scores, key=scores.get)
        
        return None


class SmartTagSuggester:
    """
    Suggests tags based on existing media library patterns.
    """
    
    @staticmethod
    def get_popular_tags(limit=20):
        """Get most popular tags in the system."""
        from taggit.models import Tag
        from django.db.models import Count
        
        tags = Tag.objects.annotate(
            usage_count=Count('taggit_taggeditem_items')
        ).order_by('-usage_count')[:limit]
        
        return [tag.name for tag in tags]
    
    @staticmethod
    def get_related_tags(existing_tags, limit=10):
        """Get tags commonly used with the given tags."""
        from taggit.models import Tag, TaggedItem
        from django.db.models import Count
        
        if not existing_tags:
            return []
        
        # Find items with any of the existing tags
        tagged_items = TaggedItem.objects.filter(
            tag__name__in=existing_tags
        ).values_list('object_id', 'content_type_id')
        
        # Find other tags used on those items
        related_tags = Tag.objects.filter(
            taggit_taggeditem_items__object_id__in=[item[0] for item in tagged_items],
            taggit_taggeditem_items__content_type_id__in=[item[1] for item in tagged_items]
        ).exclude(
            name__in=existing_tags
        ).annotate(
            usage_count=Count('taggit_taggeditem_items')
        ).order_by('-usage_count')[:limit]
        
        return [tag.name for tag in related_tags]
    
    @staticmethod
    def get_predefined_tags_by_type(tag_type='general'):
        """Get predefined tags of a specific type."""
        from .models import PredefinedTag
        
        tags = PredefinedTag.objects.filter(
            tag_type=tag_type,
            is_active=True
        ).order_by('order', 'name')
        
        return [tag.name for tag in tags]


# Convenience functions

def auto_tag_media(media_instance, backend='rule-based', apply_tags=True):
    """
    Auto-tag a media instance.
    
    Args:
        media_instance: Media model instance (Image, Video, Audio, Document)
        backend: AI backend to use
        apply_tags: Whether to apply tags or just return suggestions
    
    Returns:
        List of suggested tags
    """
    tagger = AIAutoTagger(backend=backend)
    
    # Determine media type and tag accordingly
    media_type = media_instance.__class__.__name__.lower()
    
    if 'image' in media_type and hasattr(media_instance, 'file'):
        tags = tagger.tag_image(media_instance.file.path)
    elif 'video' in media_type and hasattr(media_instance, 'file'):
        tags = tagger.tag_video(media_instance.file.path)
    elif 'audio' in media_type and hasattr(media_instance, 'file'):
        tags = tagger.tag_audio(media_instance.file.path)
    elif 'document' in media_type and hasattr(media_instance, 'file'):
        tags = tagger.tag_document(media_instance.file.path)
    else:
        tags = []
    
    # Apply tags if requested
    if apply_tags and tags:
        for tag in tags:
            media_instance.tags.add(tag)
        media_instance.save()
    
    return tags


def create_default_predefined_tags():
    """Create a set of default predefined tags."""
    from .models import PredefinedTag
    
    default_tags = [
        # Usage Type
        {'name': 'hero-image', 'tag_type': 'usage', 'color': '#667eea', 'icon': 'fa-star'},
        {'name': 'promo-video', 'tag_type': 'usage', 'color': '#f5576c', 'icon': 'fa-video'},
        {'name': 'logo', 'tag_type': 'usage', 'color': '#4facfe', 'icon': 'fa-trademark'},
        {'name': 'banner', 'tag_type': 'usage', 'color': '#43e97b', 'icon': 'fa-rectangle-ad'},
        {'name': 'icon', 'tag_type': 'usage', 'color': '#fa709a', 'icon': 'fa-icons'},
        {'name': 'thumbnail', 'tag_type': 'usage', 'color': '#30cfd0', 'icon': 'fa-image'},
        
        # Style
        {'name': 'modern', 'tag_type': 'style', 'color': '#667eea'},
        {'name': 'vintage', 'tag_type': 'style', 'color': '#f5576c'},
        {'name': 'minimalist', 'tag_type': 'style', 'color': '#4facfe'},
        {'name': 'colorful', 'tag_type': 'style', 'color': '#43e97b'},
        
        # Quality
        {'name': 'high-resolution', 'tag_type': 'quality', 'color': '#28a745'},
        {'name': 'hd', 'tag_type': 'quality', 'color': '#28a745'},
        {'name': '4k', 'tag_type': 'quality', 'color': '#28a745'},
        
        # Status
        {'name': 'approved', 'tag_type': 'status', 'color': '#28a745', 'icon': 'fa-check'},
        {'name': 'draft', 'tag_type': 'status', 'color': '#ffc107', 'icon': 'fa-pencil'},
        {'name': 'archived', 'tag_type': 'status', 'color': '#6c757d', 'icon': 'fa-archive'},
        
        # Purpose
        {'name': 'marketing', 'tag_type': 'purpose', 'color': '#f5576c'},
        {'name': 'social-media', 'tag_type': 'purpose', 'color': '#4facfe'},
        {'name': 'website', 'tag_type': 'purpose', 'color': '#667eea'},
        {'name': 'print', 'tag_type': 'purpose', 'color': '#43e97b'},
    ]
    
    created_count = 0
    for tag_data in default_tags:
        tag, created = PredefinedTag.objects.get_or_create(
            name=tag_data['name'],
            defaults=tag_data
        )
        if created:
            created_count += 1
    
    return created_count
