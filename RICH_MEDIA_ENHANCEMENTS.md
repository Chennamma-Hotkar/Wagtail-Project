# Rich Media Library Enhancements for Wagtail CMS

## Overview

This project extends Wagtail CMS with comprehensive rich media management capabilities, including custom image and document models, categorization, tagging, and a beautiful frontend gallery.

## Features

### 1. Custom Media Models

#### CustomImage
- **Copyright Management**: Track copyright holders and licensors
- **Source Attribution**: Store original source URLs
- **Categorization**: Organize images with multiple categories
- **Alt Text Override**: Custom alt text for accessibility
- **Tagging**: Flexible tagging system using django-taggit

#### CustomDocument
- **Version Control**: Track document versions
- **Expiry Dates**: Set expiration dates for time-sensitive documents
- **Department Organization**: Assign documents to departments
- **Tagging**: Same flexible tagging as images

#### Category System
- **Hierarchical Organization**: Organize media with categories
- **Translatable**: Built-in translation support
- **Snippet Integration**: Managed through Wagtail's snippet system

### 2. Frontend Gallery

A beautiful, responsive media gallery with:
- Grid layout for images
- Card layout for documents
- Search functionality
- Category filtering
- Pagination
- Detailed view pages
- Download capabilities
- Responsive design with Bootstrap 5

### 3. REST API

Full-featured REST API with:
- Image endpoints
- Document endpoints
- Category endpoints
- Filtering and search
- Pagination
- Custom actions (recent, related, expiring soon)

### 4. Wagtail Admin Integration

- Custom menu item for Media Gallery
- Enhanced admin interface
- Custom hooks for logging
- Visual indicators for custom fields

### 5. Management Commands

#### generate_sample_media
Generate sample images and categories for testing:
```bash
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

#### cleanup_expired_documents
Clean up expired documents:
```bash
# Dry run (preview)
python manage.py cleanup_expired_documents --dry-run --settings=my_cms_project.settings.dev

# Actual cleanup
python manage.py cleanup_expired_documents --settings=my_cms_project.settings.dev
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate --settings=my_cms_project.settings.dev
```

### 3. Create Superuser

```bash
python manage.py createsuperuser --settings=my_cms_project.settings.dev
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput --settings=my_cms_project.settings.dev
```

### 5. Run Development Server

```bash
python manage.py runserver --settings=my_cms_project.settings.dev
```

## URLs

### Frontend URLs
- **Gallery**: `/media/gallery/`
- **Image Detail**: `/media/image/<id>/`
- **Document Detail**: `/media/document/<id>/`
- **Category Media**: `/media/category/<slug>/`
- **Stats API**: `/media/api/stats/`

### REST API URLs
- **Images**: `/api/media/images/`
- **Documents**: `/api/media/documents/`
- **Categories**: `/api/media/categories/`

### API Examples

#### Get All Images
```bash
GET /api/media/images/
```

#### Search Images
```bash
GET /api/media/images/?search=nature
```

#### Filter by Category
```bash
GET /api/media/images/?categories__slug=technology
```

#### Get Recent Images
```bash
GET /api/media/images/recent/
```

#### Get Related Images
```bash
GET /api/media/images/<id>/related/
```

#### Get Expiring Documents
```bash
GET /api/media/documents/expiring_soon/
```

## Admin Interface

Access the Wagtail admin at `/admin/` to:
- Upload images and documents
- Manage categories
- Edit media metadata
- Organize collections
- Access the Media Gallery (new menu item)

## File Structure

```
media_enhancements/
├── __init__.py
├── admin.py
├── apps.py
├── models.py              # Custom Image, Document, Category models
├── views.py               # Frontend views
├── api_views.py           # REST API viewsets
├── serializers.py         # DRF serializers
├── urls.py                # Frontend URL configuration
├── api_urls.py            # API URL configuration
├── wagtail_hooks.py       # Wagtail admin customizations
├── management/
│   └── commands/
│       ├── generate_sample_media.py
│       └── cleanup_expired_documents.py
├── migrations/
│   └── 0001_initial.py
└── templates/
    └── media_enhancements/
        ├── base.html
        ├── gallery.html
        ├── image_detail.html
        ├── document_detail.html
        └── category_media.html
```

## Configuration

### Settings (base.py)

```python
# Custom Wagtail Models
WAGTAIL_IMAGES_MODEL = "media_enhancements.CustomImage"
WAGTAIL_DOCUMENTS_MODEL = "media_enhancements.CustomDocument"

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## Usage Examples

### Upload an Image via Admin
1. Go to `/admin/images/`
2. Click "Add an image"
3. Fill in:
   - Title
   - Upload file
   - Copyright holder
   - Source URL
   - Categories
   - Tags
   - Alt text override
4. Save

### Create a Category
1. Go to `/admin/snippets/media_enhancements/category/`
2. Click "Add category"
3. Fill in name, slug, and description
4. Save

### View Gallery
1. Navigate to `/media/gallery/`
2. Browse images and documents
3. Use search and filters
4. Click on items for details

### Use the API
```python
import requests

# Get all images
response = requests.get('http://localhost:8000/api/media/images/')
images = response.json()

# Search for images
response = requests.get('http://localhost:8000/api/media/images/?search=nature')
nature_images = response.json()

# Get recent uploads
response = requests.get('http://localhost:8000/api/media/images/recent/')
recent = response.json()
```

## Customization

### Add Custom Fields
Edit `media_enhancements/models.py` to add fields to CustomImage or CustomDocument:

```python
class CustomImage(AbstractImage):
    # Add your custom field
    photographer = models.CharField(max_length=255, blank=True)
    
    admin_form_fields = (
        'title',
        'file',
        'collection',
        'photographer',  # Add to admin form
        # ... other fields
    )
```

### Customize Templates
Templates are in `media_enhancements/templates/media_enhancements/`. Modify them to match your design.

### Add Custom API Endpoints
Edit `media_enhancements/api_views.py` to add custom actions:

```python
@action(detail=False, methods=['get'])
def my_custom_endpoint(self, request):
    # Your logic here
    return Response(data)
```

## Testing

### Generate Sample Data
```bash
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

### Test the Gallery
1. Visit `/media/gallery/`
2. Test search functionality
3. Test category filtering
4. Test pagination
5. View image and document details

### Test the API
```bash
# Using curl
curl http://localhost:8000/api/media/images/

# Using httpie
http GET http://localhost:8000/api/media/images/
```

## Production Deployment

### Environment Variables
Set these in production:
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `AWS_ACCESS_KEY_ID`: AWS access key (if using S3)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key (if using S3)
- `AWS_STORAGE_BUCKET_NAME`: S3 bucket name (if using S3)

### Static Files
```bash
python manage.py collectstatic --noinput --settings=my_cms_project.settings.production
```

### Database Migration
```bash
python manage.py migrate --settings=my_cms_project.settings.production
```

## Troubleshooting

### Images Not Displaying
- Check `MEDIA_URL` and `MEDIA_ROOT` settings
- Ensure media files are being served correctly
- In development, ensure `DEBUG=True` or configure media serving

### API Returns 404
- Verify URL configuration in `urls.py`
- Check that `rest_framework` is in `INSTALLED_APPS`
- Ensure migrations are applied

### Categories Not Showing
- Run migrations: `python manage.py migrate`
- Create categories via admin or management command
- Check that `Category` is registered as a snippet

## Support

For issues or questions:
1. Check the Wagtail documentation: https://docs.wagtail.org/
2. Review Django REST Framework docs: https://www.django-rest-framework.org/
3. Check the code comments and docstrings

## License

This project follows the same license as your main Wagtail project.

## Credits

Built with:
- Wagtail CMS
- Django
- Django REST Framework
- Bootstrap 5
- Font Awesome
