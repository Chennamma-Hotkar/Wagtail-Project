from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.models import (
    Orderable,
    TranslatableMixin,
)
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail.documents.models import AbstractDocument

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.managers import TaggableManager


class CustomImage(AbstractImage):
    """
    Extends Wagtail's default image model with rich media features.
    """
    copyright_holder = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Copyright Holder/Licensor")
    )
    source_url = models.URLField(
        blank=True,
        verbose_name=_("Original Source URL")
    )
    categories = models.ManyToManyField(
        'Category',
        blank=True,
        verbose_name=_("Categorization")
    )
    alt_text_override = models.TextField(
        blank=True,
        help_text=_("Override default alt text for specific use cases.")
    )
    
    # Folder organization
    folder = models.ForeignKey(
        'MediaFolder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images',
        verbose_name=_("Folder")
    )

    # Use modelcluster tagging
    tags = ClusterTaggableManager(blank=True)

    # The administrative panel fields
    
    admin_form_fields = (
        'title',
        'file',
        'collection',
        'copyright_holder',
        'source_url',
        'categories',
        'alt_text_override',
        'tags',
    )

    class Meta(AbstractImage.Meta):
        verbose_name = _('Custom Image')
        verbose_name_plural = _('Custom Images')


class CustomRendition(AbstractRendition):
    """
    A custom rendition model. Required when overriding AbstractImage.
    """
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name='renditions'
    )

    class Meta:
        unique_together = (('image', 'filter_spec', 'focal_point_key'),)


CustomImage.original_image_model = CustomImage
CustomImage.renditions_model = CustomRendition


class CustomDocument(AbstractDocument):
    """
    Extends Wagtail's default document model.
    """
    # Custom Fields
    document_version = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Document Version")
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Expiry Date")
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Owning Department")
    )
    
    # Folder organization
    folder = models.ForeignKey(
        'MediaFolder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name=_("Folder")
    )

    # Use modelcluster tagging
    tags = ClusterTaggableManager(blank=True)

    # The administrative panel fields
    admin_form_fields = (
        'title',
        'file',
        'collection',
        'document_version',
        'expiry_date',
        'department',
        'tags',
    )

    class Meta(AbstractDocument.Meta):
        verbose_name = _('Custom Document')
        verbose_name_plural = _('Custom Documents')


# --- Taxonomy Model (Categories) ---

class Category(TranslatableMixin, ClusterableModel):
    """
    A repeatable Snippet model for categorizing media,
    allowing for hierarchical structure if extended later.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="A slug is a short label for the category, used in URLs"
    )
    description = models.TextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = 'Categories'
        ordering = ['name']

# Category is registered as a snippet in wagtail_snippet_viewsets.py


# --- Predefined Tags Model ---

class PredefinedTag(models.Model):
    """Predefined tags for consistent tagging."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    tag_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('general', 'General'),
            ('technical', 'Technical'),
            ('content', 'Content Type'),
            ('status', 'Status'),
        ]
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Predefined Tag'
        verbose_name_plural = 'Predefined Tags'
        ordering = ['name']


# --- Media Folder Model ---

class MediaFolder(models.Model):
    """Hierarchical folder system for organizing media files."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    icon = models.CharField(max_length=50, blank=True, default='fa-folder')
    color = models.CharField(max_length=7, blank=True, default='#3b82f6')
    order = models.IntegerField(default=0)
    is_system_folder = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_children(self):
        return self.children.all()
    
    def get_media_count(self):
        count = 0
        count += self.images.count() if hasattr(self, 'images') else 0
        count += self.videos.count() if hasattr(self, 'videos') else 0
        count += self.audio_files.count() if hasattr(self, 'audio_files') else 0
        count += self.documents.count() if hasattr(self, 'documents') else 0
        return count
    
    def get_breadcrumbs(self):
        breadcrumbs = []
        current = self
        while current:
            breadcrumbs.insert(0, current)
            current = current.parent
        return breadcrumbs
    
    def can_delete(self):
        return not self.is_system_folder and self.get_media_count() == 0 and not self.get_children().exists()
    
    class Meta:
        verbose_name = 'Media Folder'
        verbose_name_plural = 'Media Folders'
        ordering = ['order', 'name']


# --- Video Model ---

class Video(models.Model):
    """Video file model."""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True)
    duration = models.DurationField(blank=True, null=True)
    resolution = models.CharField(max_length=50, blank=True)
    video_type = models.CharField(max_length=50, blank=True)
    director = models.CharField(max_length=255, blank=True)
    producer = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(MediaFolder, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    categories = models.ManyToManyField(Category, blank=True, related_name='videos')
    tags = TaggableManager(blank=True)
    copyright_holder = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(blank=True)
    collection = models.ForeignKey('wagtailcore.Collection', on_delete=models.CASCADE, related_name='videos', default=1)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['-created_at']


# --- Audio Model ---

class Audio(models.Model):
    """Audio file model."""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='audio/')
    thumbnail = models.ImageField(upload_to='audio_thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True)
    duration = models.DurationField(blank=True, null=True)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(blank=True, null=True)
    folder = models.ForeignKey(MediaFolder, on_delete=models.SET_NULL, null=True, blank=True, related_name='audio_files')
    categories = models.ManyToManyField(Category, blank=True, related_name='audio_files')
    tags = TaggableManager(blank=True)
    copyright_holder = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(blank=True)
    collection = models.ForeignKey('wagtailcore.Collection', on_delete=models.CASCADE, related_name='audio_files', default=1)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audio Files'
        ordering = ['-created_at']
