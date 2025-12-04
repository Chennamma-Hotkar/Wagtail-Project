# 🎨 Wagtail Rich Media Library

A comprehensive rich media management system for Wagtail CMS with advanced features for organizing, categorizing, and serving images and documents.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2+-green.svg)
![Wagtail](https://img.shields.io/badge/wagtail-latest-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 🖼️ Custom Media Models
- **Enhanced Images**: Copyright tracking, source attribution, categories, custom alt text
- **Smart Documents**: Version control, expiry dates, department organization
- **Videos & Audio**: Full support for video and audio files with metadata
- **Flexible Tagging**: Tag-based organization using django-taggit
- **Category System**: Hierarchical categorization with translation support
- **Folder System**: Hierarchical folder organization with breadcrumb navigation

### 🎨 Unified Dashboard
- **Clean Light Pink Theme**: White background with white boxes, black text, and light pink hover effects
- **All Media Types**: Images, videos, audio, and documents in one view
- **Folder Navigation**: Organize media in hierarchical folders
- **Breadcrumb Navigation**: Easy navigation through folder structure
- **Responsive Design**: Built with Bootstrap 5
- **Advanced Search**: Full-text search across all media
- **Smart Filtering**: Filter by type, categories, tags, and folders
- **Animated UI**: Smooth hover effects and transitions
- **Pagination**: Efficient browsing of large media libraries
- **Detail Views**: Rich detail pages for all media types

### 🔌 REST API
- **Full CRUD**: Complete API for images, documents, and categories
- **Advanced Filtering**: Filter, search, and order results
- **Custom Endpoints**: Recent uploads, related media, expiring documents
- **Pagination**: Built-in pagination support
- **DRF Integration**: Powered by Django REST Framework

### 🛠️ Admin Integration
- **Beautiful Icons**: All menu items have intuitive icons
- **Wagtail Admin**: Seamless integration with Wagtail's admin interface
- **Custom Menu Items**: Quick access to dashboard, folders, videos, audio
- **Enhanced UI**: Custom styling and JavaScript enhancements
- **Hooks**: Automatic logging of media uploads
- **Organized Menu**: Logical grouping with visual hierarchy

### 📊 Management Tools
- **Sample Data Generator**: Create test data instantly
- **Cleanup Commands**: Automated expired document removal
- **Statistics API**: Real-time media statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

#### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

#### Option 2: Manual Setup

1. **Clone or navigate to the project:**
```bash
cd wagtail-rich-media
```

2. **Create and activate virtual environment:**
```bash
# Linux/Mac
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate --settings=my_cms_project.settings.dev
```

5. **Create superuser:**
```bash
python manage.py createsuperuser --settings=my_cms_project.settings.dev
```

6. **Collect static files:**
```bash
python manage.py collectstatic --noinput --settings=my_cms_project.settings.dev
```

7. **Setup folder structure (optional):**
```bash
python manage.py setup_folders --settings=my_cms_project.settings.dev
```

8. **Generate sample data (optional):**
```bash
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

9. **Run development server:**
```bash
python manage.py runserver --settings=my_cms_project.settings.dev
```

### 🌐 Access Points

Once the server is running, visit:

- **Admin Panel**: http://localhost:8000/admin/
- **Unified Dashboard**: http://localhost:8000/media/dashboard/
- **Media Gallery**: http://localhost:8000/media/gallery/
- **REST API**: http://localhost:8000/api/media/
- **API Documentation**: http://localhost:8000/api/media/ (browsable API)

## 📖 Documentation

- **[Complete Documentation](RICH_MEDIA_ENHANCEMENTS.md)** - Full feature documentation
- **[Unified Dashboard Guide](UNIFIED_DASHBOARD_GUIDE.md)** - Dashboard usage guide
- **[Folder System Guide](FOLDER_SYSTEM_GUIDE.md)** - Folder organization guide
- **[Image Editor Guide](IMAGE_EDITOR_GUIDE.md)** - Image editing features
- **[GitHub Setup Guide](GITHUB_SETUP.md)** - Git and GitHub instructions
- **[File Structure](FILE_STRUCTURE.md)** - Complete project structure

## 🎯 Usage Examples

### Upload Media via Admin

1. Navigate to http://localhost:8000/admin/
2. Click "Images" or "Documents"
3. Click "Add an image" or "Add a document"
4. Fill in the form with:
   - Title
   - File upload
   - Copyright holder (for images)
   - Categories
   - Tags
   - Additional metadata
5. Save

### Organize with Folders

1. Visit http://localhost:8000/media/dashboard/
2. Click **"New Folder"** to create a folder
3. Navigate into folders by clicking on them
4. Use breadcrumbs to navigate back
5. When uploading media, select a folder in the admin
6. Move existing media by editing and changing the folder field

**Pre-configured folders:**
- Banners
- Products
- Campaigns → 2024 Launch
- Social Media
- Logos
- Videos
- Audio
- Documents

### Browse Gallery

1. Visit http://localhost:8000/media/dashboard/
2. Use the search box to find specific media
3. Filter by type, categories, or folders
4. Click on any item for detailed view
5. Download or share media

### Use the REST API

**Get all images:**
```bash
curl http://localhost:8000/api/media/images/
```

**Search images:**
```bash
curl http://localhost:8000/api/media/images/?search=nature
```

**Filter by category:**
```bash
curl http://localhost:8000/api/media/images/?categories__slug=technology
```

**Get recent uploads:**
```bash
curl http://localhost:8000/api/media/images/recent/
```

**Get expiring documents:**
```bash
curl http://localhost:8000/api/media/documents/expiring_soon/
```

### Python API Usage

```python
import requests

# Get all images
response = requests.get('http://localhost:8000/api/media/images/')
images = response.json()

# Search for specific images
response = requests.get(
    'http://localhost:8000/api/media/images/',
    params={'search': 'nature', 'categories__slug': 'photography'}
)
results = response.json()

# Get image details
image_id = 1
response = requests.get(f'http://localhost:8000/api/media/images/{image_id}/')
image_detail = response.json()
```

## 🏗️ Project Structure

```
wagtail-rich-media/
├── media_enhancements/          # Main app
│   ├── models.py               # Custom models
│   ├── views.py                # Frontend views
│   ├── api_views.py            # REST API
│   ├── serializers.py          # API serializers
│   ├── urls.py                 # Frontend URLs
│   ├── api_urls.py             # API URLs
│   ├── wagtail_hooks.py        # Admin customizations
│   ├── management/commands/    # Management commands
│   └── templates/              # HTML templates
├── my_cms_project/             # Project settings
│   ├── settings/               # Settings modules
│   └── urls.py                 # Main URL config
├── requirements.txt            # Dependencies
├── setup.sh                    # Linux/Mac setup
├── setup.bat                   # Windows setup
└── Documentation files
```

## 🔧 Configuration

### Custom Image Model

The project uses custom image and document models. These are configured in `settings/base.py`:

```python
WAGTAIL_IMAGES_MODEL = "media_enhancements.CustomImage"
WAGTAIL_DOCUMENTS_MODEL = "media_enhancements.CustomDocument"
```

### REST Framework Settings

API configuration in `settings/base.py`:

```python
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

## 🎨 Customization

### Add Custom Fields

Edit `media_enhancements/models.py`:

```python
class CustomImage(AbstractImage):
    # Add your custom field
    photographer = models.CharField(max_length=255, blank=True)
    
    admin_form_fields = (
        'title',
        'file',
        'photographer',  # Add to admin
        # ... other fields
    )
```

### Customize Templates

Templates are in `media_enhancements/templates/media_enhancements/`:
- `base.html` - Base template
- `gallery.html` - Main gallery
- `image_detail.html` - Image details
- `document_detail.html` - Document details

### Add API Endpoints

Edit `media_enhancements/api_views.py`:

```python
@action(detail=False, methods=['get'])
def my_custom_endpoint(self, request):
    # Your logic
    return Response(data)
```

## 🧪 Testing

### Generate Sample Data

```bash
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

This creates:
- 4 sample categories
- 5 sample images with different colors
- Tags and category assignments

### Cleanup Expired Documents

```bash
# Dry run (preview)
python manage.py cleanup_expired_documents --dry-run --settings=my_cms_project.settings.dev

# Actual cleanup
python manage.py cleanup_expired_documents --settings=my_cms_project.settings.dev
```

## 📦 Dependencies

- **Wagtail** - CMS framework
- **Django** - Web framework
- **Django REST Framework** - API framework
- **django-filter** - Filtering support
- **django-taggit** - Tagging system
- **Pillow** - Image processing
- **Bootstrap 5** - Frontend framework
- **Font Awesome** - Icons

## 🚢 Deployment

### Environment Variables

Set these for production:

```bash
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@host:port/dbname
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

### Production Setup

```bash
# Collect static files
python manage.py collectstatic --noinput --settings=my_cms_project.settings.production

# Run migrations
python manage.py migrate --settings=my_cms_project.settings.production

# Create superuser
python manage.py createsuperuser --settings=my_cms_project.settings.production
```

## 🐛 Troubleshooting

### Images Not Displaying
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings
- Ensure media files are being served (in dev, `DEBUG=True`)
- Verify file permissions

### API Returns 404
- Check URL configuration in `urls.py`
- Verify `rest_framework` is in `INSTALLED_APPS`
- Run migrations

### Import Errors
- Activate virtual environment
- Install all requirements: `pip install -r requirements.txt`
- Check Python version (3.8+)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Built with:
- [Wagtail CMS](https://wagtail.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)

## 📞 Support

For issues or questions:
1. Check the [documentation](RICH_MEDIA_ENHANCEMENTS.md)
2. Review [Wagtail docs](https://docs.wagtail.org/)
3. Check [DRF docs](https://www.django-rest-framework.org/)

## 🗺️ Roadmap

Future enhancements:
- [ ] Image editing capabilities
- [ ] Bulk upload functionality
- [ ] Advanced analytics dashboard
- [ ] Social media integration
- [ ] Video support
- [ ] AI-powered tagging
- [ ] CDN integration
- [ ] Multi-language support

---

**Made with ❤️ for the Wagtail community**
