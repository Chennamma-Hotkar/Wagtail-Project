# 🎨 Admin Icons Guide

## Overview

The Wagtail admin interface now has beautiful icons for all media-related sections, making navigation intuitive and visually appealing.

## Admin Menu Icons

### Main Navigation

| Menu Item | Icon | Description |
|-----------|------|-------------|
| **Dashboard** | 📊 `th-large` | Unified media dashboard |
| **Media Folders** | 📁 `folder-open-inverse` | Folder management |
| **Categories** | 🏷️ `tag` | Category management |
| **Predefined Tags** | 🏷️ `tag` | Tag management |
| **Videos** | 🎥 `media` | Video library |
| **Audio Files** | 🎵 `music` | Audio library |
| **Images** | 🖼️ `image` | Image library (Wagtail default) |
| **Documents** | 📄 `doc-full-inverse` | Document library (Wagtail default) |

## Icon Reference

### Available Wagtail Icons

The system uses Wagtail's built-in icon set. Here are the most commonly used icons:

**Media & Content:**
- `image` - Images
- `media` - Videos
- `music` - Audio files
- `doc-full-inverse` - Documents
- `folder-open-inverse` - Folders
- `folder-inverse` - Closed folders

**Organization:**
- `tag` - Tags and categories
- `list-ul` - Lists
- `th-large` - Grid/Dashboard
- `th` - Thumbnails

**Actions:**
- `plus` - Add/Create
- `edit` - Edit
- `bin` - Delete
- `download` - Download
- `upload` - Upload
- `search` - Search

**Navigation:**
- `arrow-left` - Back
- `arrow-right` - Forward
- `arrow-up` - Up
- `arrow-down` - Down
- `home` - Home

**Status:**
- `tick` - Success/Complete
- `cross` - Error/Cancel
- `warning` - Warning
- `help` - Help/Info

## Customization

### Changing Menu Icons

To change an icon for a menu item, edit `wagtail_snippet_viewsets.py`:

```python
class VideoViewSet(SnippetViewSet):
    model = Video
    icon = "media"  # Change this to any Wagtail icon name
    menu_label = "Videos"
    menu_order = 203
    # ...
```

### Adding New Menu Items

To add a new menu item with an icon, add to `wagtail_hooks.py`:

```python
@hooks.register('register_admin_menu_item')
def register_custom_menu_item():
    return MenuItem(
        'My Custom Section',
        reverse('my_custom_url'),
        icon_name='your-icon-name',
        order=300
    )
```

### Custom Icons

If you need custom icons not in Wagtail's set, you can:

1. **Use Font Awesome** (already included):
   - Add custom CSS in `wagtail_hooks.py`
   - Use Font Awesome classes

2. **Add SVG Icons**:
   - Place SVG files in `static/icons/`
   - Register them in Wagtail's icon registry

## Icon Best Practices

### Do's ✅

- Use icons that clearly represent the content
- Keep icons consistent across similar sections
- Use standard icons for common actions
- Test icon visibility in both light and dark themes

### Don'ts ❌

- Don't use too many different icon styles
- Don't use obscure icons that users won't understand
- Don't change icons frequently (confuses users)
- Don't use icons without labels

## Menu Organization

The admin menu is organized by order number:

```
100-150: Core Wagtail items (Pages, Images, Documents)
199: Dashboard (our unified dashboard)
200: Media Folders
201: Categories
202: Predefined Tags
203: Videos
204: Audio Files
300+: Other custom items
```

## Snippet ViewSets

All media snippets are configured with icons in `wagtail_snippet_viewsets.py`:

```python
class MediaFolderViewSet(SnippetViewSet):
    model = MediaFolder
    icon = "folder-open-inverse"
    menu_label = "Media Folders"
    menu_order = 200
    add_to_admin_menu = True
    list_display = ["name", "parent", "get_media_count", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["parent", "is_system_folder"]
```

### ViewSet Configuration Options

- `icon` - Icon name from Wagtail's icon set
- `menu_label` - Display name in menu
- `menu_order` - Position in menu (lower = higher)
- `add_to_admin_menu` - Show in main menu (True/False)
- `list_display` - Columns in list view
- `search_fields` - Searchable fields
- `list_filter` - Filterable fields

## Visual Enhancements

### Custom CSS

The system includes custom CSS for visual enhancements:

```css
.media-enhancement-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 11px;
}
```

### Custom JavaScript

Adds visual indicators for important fields:

```javascript
// Highlights copyright fields when filled
const copyrightFields = document.querySelectorAll('[name*="copyright"]');
copyrightFields.forEach(field => {
    if (field.value) {
        field.style.borderLeft = '3px solid #28a745';
    }
});
```

## Troubleshooting

### Icons Not Showing

**Problem:** Icons appear as text or don't show

**Solutions:**
1. Check icon name is correct (case-sensitive)
2. Verify Wagtail version supports the icon
3. Clear browser cache
4. Check for CSS conflicts

### Menu Items Missing

**Problem:** Menu items don't appear

**Solutions:**
1. Check `add_to_admin_menu = True` in ViewSet
2. Verify model is imported correctly
3. Check for registration errors in console
4. Restart development server

### Wrong Icon Displayed

**Problem:** Different icon shows than expected

**Solutions:**
1. Verify icon name spelling
2. Check for duplicate registrations
3. Clear Django cache
4. Check menu order conflicts

## Complete Icon List

Here's a reference of all icons used in the system:

```python
MEDIA_ICONS = {
    'dashboard': 'th-large',
    'folders': 'folder-open-inverse',
    'categories': 'tag',
    'tags': 'tag',
    'videos': 'media',
    'audio': 'music',
    'images': 'image',
    'documents': 'doc-full-inverse',
}
```

## Files Modified

- `wagtail_snippet_viewsets.py` - Snippet configurations with icons
- `wagtail_hooks.py` - Menu items and custom hooks
- `models.py` - Removed duplicate registrations

## Testing

To verify icons are working:

1. Visit http://localhost:8000/admin/
2. Check left sidebar menu
3. Verify all items have icons
4. Click each menu item to test navigation
5. Check snippet list pages for proper icons

## Future Enhancements

Potential improvements:
- Custom icon set
- Icon color customization
- Animated icons
- Icon badges (counts, notifications)
- Dark mode icon variants
- Icon tooltips

---

**For more information:**
- [Wagtail Icons Documentation](https://docs.wagtail.org/en/stable/advanced_topics/icons.html)
- [Wagtail Admin Customization](https://docs.wagtail.org/en/stable/advanced_topics/customisation/admin_templates.html)
