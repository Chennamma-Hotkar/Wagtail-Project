# 🎯 Unified Dashboard Guide

## Overview

The **Unified Dashboard** is a powerful feature that displays all media types (Images, Videos, Audio, and Documents) in a single, beautiful interface. It provides a standardized view of all your media with advanced filtering, searching, and sorting capabilities.

## ✨ Features

### 1. **All Media Types in One View**
- ✅ Images
- ✅ Videos  
- ✅ Audio Files
- ✅ Documents

### 2. **Standardized Media Object**
All media types are converted to a unified format with:
- Media type identification
- Thumbnail display
- File information
- Metadata
- Categories and tags
- Detail page links

### 3. **Advanced Filtering**
- Filter by media type (All, Images, Videos, Audio, Documents)
- Filter by category
- Search by title or tags
- Sort by date or title

### 4. **Beautiful UI**
- Responsive grid layout
- Color-coded media types
- Hover effects and animations
- Statistics cards
- Empty state handling

## 🚀 Access the Dashboard

### URL
```
http://localhost:8000/media/dashboard/
```

### From Wagtail Admin
1. Login to `/admin/`
2. Click "Unified Dashboard" in the sidebar menu

### From Homepage
Click the "Unified Dashboard" link in the navigation

## 📊 Dashboard Components

### 1. Statistics Cards
Shows counts for:
- Total Media (all types combined)
- Images
- Videos
- Audio Files
- Documents

Click any card to filter by that media type.

### 2. Filters Section
- **Search Box**: Search by title or tags
- **Sort Dropdown**: Sort by newest, oldest, title A-Z, or Z-A
- **Category Chips**: Filter by category

### 3. Media Grid
Displays all media in a responsive grid with:
- Thumbnail or icon
- Media type badge (color-coded)
- Title
- Upload date
- File size
- Metadata (resolution, duration, etc.)
- Tags
- Action buttons (View Details, Download)

### 4. Pagination
Navigate through large media libraries with page numbers.

## 🎨 Media Type Colors

Each media type has a unique color:
- **Images**: Purple (#667eea)
- **Documents**: Pink (#f5576c)
- **Videos**: Blue (#4facfe)
- **Audio**: Green (#43e97b)

## 📁 File Structure

### New Files Created

1. **Models** (`media_enhancements/models.py`)
   - `Video` model with metadata
   - `Audio` model with metadata
   - File validators for extensions

2. **Dashboard Logic** (`media_enhancements/unified_dashboard.py`)
   - `UnifiedMediaItem` class - Standardizes all media types
   - `unified_dashboard` view - Main dashboard view
   - `video_detail` view - Video detail page
   - `audio_detail` view - Audio detail page

3. **Templates**
   - `unified_dashboard.html` - Main dashboard template
   - `video_detail.html` - Video detail page
   - `audio_detail.html` - Audio detail page

4. **URLs** (`media_enhancements/urls.py`)
   - `/media/dashboard/` - Unified dashboard
   - `/media/video/<id>/` - Video detail
   - `/media/audio/<id>/` - Audio detail

5. **Admin Integration** (`wagtail_hooks.py`)
   - Menu item for Unified Dashboard

## 🔧 How It Works

### UnifiedMediaItem Class

This class standardizes all media types into a common format:

```python
class UnifiedMediaItem:
    def __init__(self, obj):
        self.media_type = 'image' | 'video' | 'audio' | 'document'
        self.id = obj.id
        self.title = obj.title
        self.created_at = obj.created_at
        self.file_url = obj.file.url
        self.thumbnail_url = ...
        self.file_size = ...
        self.categories = ...
        self.tags = ...
        self.metadata = {...}  # Type-specific metadata
        self.detail_url = ...
        self.icon = 'fa-image' | 'fa-video' | 'fa-music' | 'fa-file-alt'
        self.color = '#667eea' | '#4facfe' | '#43e97b' | '#f5576c'
```

### Metadata by Type

**Images:**
- Dimensions (width × height)
- Copyright holder

**Documents:**
- Version
- Department
- Expiry date

**Videos:**
- Duration
- Resolution
- Director

**Audio:**
- Duration
- Artist
- Album
- Genre

## 📝 Usage Examples

### Upload Media

#### Images
1. Go to `/admin/images/`
2. Click "Add an image"
3. Upload and fill metadata
4. View in dashboard

#### Videos
1. Go to `/admin/snippets/media_enhancements/video/`
2. Click "Add video"
3. Upload video file (MP4, AVI, MOV, etc.)
4. Add metadata (duration, resolution, director)
5. View in dashboard

#### Audio
1. Go to `/admin/snippets/media_enhancements/audio/`
2. Click "Add audio"
3. Upload audio file (MP3, WAV, OGG, etc.)
4. Add metadata (artist, album, genre)
5. View in dashboard

#### Documents
1. Go to `/admin/documents/`
2. Click "Add a document"
3. Upload and fill metadata
4. View in dashboard

### Filter Media

**By Type:**
- Click statistics cards at the top
- Or use URL: `?type=video`

**By Category:**
- Click category chips
- Or use URL: `?category=music`

**By Search:**
- Type in search box
- Searches title and tags

**Combined:**
```
/media/dashboard/?type=video&category=tutorials&q=python
```

### Sort Media

- **Newest First**: Default, shows recent uploads
- **Oldest First**: Shows oldest uploads first
- **Title A-Z**: Alphabetical order
- **Title Z-A**: Reverse alphabetical

## 🎯 API Integration

The unified dashboard can be extended with API endpoints:

```python
# In api_views.py
class UnifiedMediaViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for unified media."""
    
    def list(self, request):
        # Fetch all media types
        # Convert to unified format
        # Return JSON
        pass
```

## 🔌 Extending the Dashboard

### Add New Media Type

1. **Create Model** (e.g., `Podcast`)
```python
class Podcast(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='podcasts/')
    # ... other fields
```

2. **Update UnifiedMediaItem**
```python
def _get_media_type(self, obj):
    if obj.__class__.__name__ == 'Podcast':
        return 'podcast'
    # ... existing types
```

3. **Add to Dashboard View**
```python
podcasts = Podcast.objects.all()
all_media = list(chain(images, documents, videos, audio_files, podcasts))
```

4. **Update Template**
Add podcast icon and color.

### Customize Metadata Display

Edit `_get_metadata()` in `UnifiedMediaItem`:

```python
def _get_metadata(self, obj):
    metadata = {}
    
    if self.media_type == 'your_type':
        metadata['custom_field'] = getattr(obj, 'custom_field', None)
    
    return metadata
```

### Add Bulk Actions

```python
@login_required
def bulk_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('media_ids')
        # Delete selected media
        pass
```

## 🎨 Customization

### Change Colors

Edit `unified_dashboard.html`:

```css
.stat-card {
    background: your-color;
}
```

### Change Grid Layout

```css
.media-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
}
```

### Add Custom Filters

```python
# In unified_dashboard.py
collection_filter = request.GET.get('collection')
if collection_filter:
    images = images.filter(collection__name=collection_filter)
```

## 📊 Statistics

The dashboard automatically calculates:
- Total media count
- Count by type
- File sizes
- Upload dates

## 🔒 Permissions

The dashboard requires login:
```python
@login_required
def unified_dashboard(request):
    ...
```

To add role-based permissions:
```python
from django.contrib.auth.decorators import permission_required

@permission_required('media_enhancements.view_video')
def unified_dashboard(request):
    ...
```

## 🐛 Troubleshooting

### Media Not Showing

1. Check if migrations are applied:
```bash
python manage.py migrate
```

2. Verify media is uploaded:
```bash
python manage.py shell
>>> from media_enhancements.models import Video
>>> Video.objects.count()
```

3. Check file permissions for media directory

### Thumbnails Not Displaying

1. Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured
2. Check if files exist in media directory
3. Verify DEBUG=True or media serving is configured

### Filters Not Working

1. Check URL parameters
2. Verify category slugs match
3. Check search query syntax

## 📚 Related Documentation

- **README.md** - Project overview
- **RICH_MEDIA_ENHANCEMENTS.md** - Complete features
- **FILE_STRUCTURE.md** - Project structure
- **COMMANDS_REFERENCE.md** - All commands

## 🎉 Benefits

### For Content Editors
- ✅ See all media in one place
- ✅ Easy filtering and search
- ✅ Quick access to details
- ✅ Visual organization

### For Developers
- ✅ Standardized media handling
- ✅ Easy to extend
- ✅ Clean code structure
- ✅ Reusable components

### For Administrators
- ✅ Overview of all media
- ✅ Statistics at a glance
- ✅ Efficient management
- ✅ Better organization

## 🚀 Next Steps

1. **Upload Media**: Add videos and audio files
2. **Create Categories**: Organize your media
3. **Add Tags**: Improve searchability
4. **Customize**: Adjust colors and layout
5. **Extend**: Add new media types or features

## 💡 Pro Tips

1. **Use Categories**: Create meaningful categories early
2. **Tag Everything**: Makes search much better
3. **Add Metadata**: Fill in all fields for better organization
4. **Use Thumbnails**: Upload custom thumbnails for videos/audio
5. **Regular Cleanup**: Remove unused media periodically

---

**The Unified Dashboard is your central hub for all media management!** 🎯

**Access it at**: http://localhost:8000/media/dashboard/
