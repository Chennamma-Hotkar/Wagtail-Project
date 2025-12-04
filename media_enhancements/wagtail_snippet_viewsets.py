"""
Wagtail Snippet ViewSets with custom icons and configurations
"""

from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet

from .models import MediaFolder, Category, PredefinedTag, Video, Audio


class MediaFolderViewSet(SnippetViewSet):
    model = MediaFolder
    icon = "folder-open-inverse"
    menu_label = "Media Folders"
    menu_order = 200
    add_to_admin_menu = False  # Show in Snippets menu only
    add_to_settings_menu = False
    list_display = ["name", "parent", "get_media_count", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["parent", "is_system_folder"]


class CategoryViewSet(SnippetViewSet):
    model = Category
    icon = "tag"
    menu_label = "Categories"
    menu_order = 201
    add_to_admin_menu = False  # Show in Snippets menu only
    add_to_settings_menu = False
    list_display = ["name", "category_type", "applicable_to", "is_featured"]
    search_fields = ["name", "description"]
    list_filter = ["category_type", "applicable_to", "is_featured"]


class PredefinedTagViewSet(SnippetViewSet):
    model = PredefinedTag
    icon = "tag"
    menu_label = "Predefined Tags"
    menu_order = 202
    add_to_admin_menu = False  # Show in Snippets menu only
    add_to_settings_menu = False
    list_display = ["name", "tag_type", "is_active"]
    search_fields = ["name", "description"]
    list_filter = ["tag_type", "is_active"]


class VideoViewSet(SnippetViewSet):
    model = Video
    icon = "media"
    menu_label = "Videos"
    menu_order = 203
    add_to_admin_menu = True
    list_display = ["title", "video_type", "folder", "duration", "created_at"]
    search_fields = ["title", "description"]
    list_filter = ["video_type", "folder", "categories"]


class AudioViewSet(SnippetViewSet):
    model = Audio
    icon = "pick"
    menu_label = "Audio"
    menu_order = 204
    add_to_admin_menu = True
    list_display = ["title", "folder", "artist", "duration", "created_at"]
    search_fields = ["title", "artist", "album", "description"]
    list_filter = ["folder", "categories"]


# Register all viewsets
register_snippet(MediaFolderViewSet)
register_snippet(CategoryViewSet)
register_snippet(PredefinedTagViewSet)
register_snippet(VideoViewSet)
register_snippet(AudioViewSet)
