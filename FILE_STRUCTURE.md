# Complete File Structure

## Project Overview

```
wagtail-rich-media/
│
├── .git/                           # Git repository
├── .venv/                          # Virtual environment (created during setup)
├── db.sqlite3                      # SQLite database
├── manage.py                       # Django management script
│
├── requirements.txt                # Python dependencies
├── setup.sh                        # Linux/Mac setup script
├── setup.bat                       # Windows setup script
├── RICH_MEDIA_ENHANCEMENTS.md     # Complete documentation
├── GITHUB_SETUP.md                # GitHub setup guide
├── FILE_STRUCTURE.md              # This file
├── README.md                       # Project README (to be created)
├── .gitignore                      # Git ignore file (to be created)
│
├── home/                           # Home app
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── migrations/
│   ├── static/
│   └── templates/
│
├── search/                         # Search app
│   ├── __init__.py
│   ├── views.py
│   ├── templates/
│   └── __pycache__/
│
├── media_enhancements/             # ⭐ Main Rich Media App
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py
│   ├── models.py                   # CustomImage, CustomDocument, Category
│   ├── views.py                    # Frontend views
│   ├── api_views.py                # REST API viewsets
│   ├── serializers.py              # DRF serializers
│   ├── urls.py                     # Frontend URLs
│   ├── api_urls.py                 # API URLs
│   ├── wagtail_hooks.py            # Wagtail admin customizations
│   ├── tests.py
│   │
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py         # Initial migration
│   │
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── generate_sample_media.py
│   │       └── cleanup_expired_documents.py
│   │
│   └── templates/
│       └── media_enhancements/
│           ├── base.html           # Base template
│           ├── gallery.html        # Main gallery view
│           ├── image_detail.html   # Image detail page
│           ├── document_detail.html # Document detail page
│           └── category_media.html  # Category filtered view
│
├── my_cms_project/                 # Project settings
│   ├── __init__.py
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py
│   │
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                 # Base settings
│   │   ├── dev.py                  # Development settings
│   │   ├── local.py                # Local overrides
│   │   └── production.py           # Production settings
│   │
│   ├── static/                     # Project static files
│   └── templates/                  # Project templates
│
├── staticfiles/                    # Collected static files
│   ├── admin/
│   ├── css/
│   ├── js/
│   ├── wagtailadmin/
│   ├── wagtaildocs/
│   ├── wagtailembeds/
│   ├── wagtailimages/
│   └── wagtailsnippets/
│
└── media/                          # User uploaded files (created at runtime)
    ├── images/
    ├── documents/
    └── original_images/
```

## Key Files Explained

### Core Application Files

#### `media_enhancements/models.py`
Defines the custom models:
- `CustomImage`: Extended image model with copyright, source URL, categories, alt text
- `CustomRendition`: Required for custom image model
- `CustomDocument`: Extended document model with version, expiry date, department
- `Category`: Snippet model for categorizing media

#### `media_enhancements/views.py`
Frontend views:
- `media_gallery`: Main gallery view with search and filtering
- `image_detail`: Detailed image view
- `document_detail`: Detailed document view
- `category_media`: Category-filtered media view
- `media_stats_api`: Statistics API endpoint

#### `media_enhancements/api_views.py`
REST API viewsets:
- `CategoryViewSet`: Category API
- `CustomImageViewSet`: Image API with filtering, search, recent, related
- `CustomDocumentViewSet`: Document API with filtering, search, expiring soon

#### `media_enhancements/serializers.py`
DRF serializers for API responses:
- `CategorySerializer`
- `CustomImageSerializer`
- `CustomDocumentSerializer`

#### `media_enhancements/wagtail_hooks.py`
Wagtail admin customizations:
- Menu item for Media Gallery
- Custom CSS and JavaScript
- Hooks for image/document creation logging

### URL Configuration

#### `my_cms_project/urls.py`
Main URL configuration including:
- Django admin
- Wagtail admin
- Media enhancements frontend
- Media enhancements API
- Wagtail pages

#### `media_enhancements/urls.py`
Frontend URLs:
- `/media/gallery/` - Main gallery
- `/media/image/<id>/` - Image detail
- `/media/document/<id>/` - Document detail
- `/media/category/<slug>/` - Category media
- `/media/api/stats/` - Statistics

#### `media_enhancements/api_urls.py`
REST API URLs:
- `/api/media/images/` - Images API
- `/api/media/documents/` - Documents API
- `/api/media/categories/` - Categories API

### Templates

#### `media_enhancements/templates/media_enhancements/base.html`
Base template with:
- Bootstrap 5 integration
- Font Awesome icons
- Custom CSS styling
- Navigation bar
- Footer

#### `media_enhancements/templates/media_enhancements/gallery.html`
Main gallery template with:
- Search functionality
- Category filters
- Statistics cards
- Image grid
- Document cards
- Pagination

#### `media_enhancements/templates/media_enhancements/image_detail.html`
Image detail template with:
- Full-size image display
- Metadata table
- Categories and tags
- Download button
- Edit link

#### `media_enhancements/templates/media_enhancements/document_detail.html`
Document detail template with:
- Document information
- Download and open buttons
- Metadata table
- Tags
- Quick actions (copy URL, share)

### Management Commands

#### `generate_sample_media.py`
Creates sample data:
- 4 categories (Nature, Technology, Business, Education)
- 5 colored sample images
- Assigns categories and tags

Usage:
```bash
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

#### `cleanup_expired_documents.py`
Removes expired documents:
- Finds documents past expiry date
- Supports dry-run mode
- Logs deletions

Usage:
```bash
python manage.py cleanup_expired_documents --dry-run --settings=my_cms_project.settings.dev
```

### Settings Files

#### `my_cms_project/settings/base.py`
Base settings including:
- Installed apps (with media_enhancements, rest_framework, django_filters)
- Middleware
- Templates
- Database
- Static/media files
- Wagtail configuration
- REST Framework configuration

#### `my_cms_project/settings/dev.py`
Development settings:
- DEBUG = True
- Development SECRET_KEY
- ALLOWED_HOSTS = ["*"]
- Console email backend

#### `my_cms_project/settings/production.py`
Production settings:
- DEBUG = False
- Manifest static files storage
- Security settings (to be configured)

### Setup Scripts

#### `setup.sh` (Linux/Mac)
Automated setup script:
1. Checks Python installation
2. Creates virtual environment
3. Installs dependencies
4. Runs migrations
5. Collects static files
6. Creates superuser
7. Generates sample media (optional)

#### `setup.bat` (Windows)
Windows version of setup script with same functionality.

### Documentation Files

#### `RICH_MEDIA_ENHANCEMENTS.md`
Complete documentation including:
- Feature overview
- Installation instructions
- URL reference
- API examples
- Configuration guide
- Usage examples
- Customization guide
- Troubleshooting

#### `GITHUB_SETUP.md`
GitHub setup guide including:
- Git initialization
- Repository creation
- Push commands
- Branching strategy
- Tagging releases
- GitHub Actions (optional)

#### `FILE_STRUCTURE.md`
This file - complete project structure documentation.

## Dependencies (requirements.txt)

```
wagtail                    # Wagtail CMS
Django>=4.2               # Django framework
psycopg2-binary           # PostgreSQL adapter
pillow                    # Image processing
django-taggit             # Tagging support
django-modelcluster       # Wagtail model clustering
dj-database-url           # Database URL parsing
django-storages[boto3]    # Cloud storage (S3)
boto3                     # AWS SDK
whitenoise                # Static file serving
django-model-utils        # Model utilities
djangorestframework       # REST API
django-filter             # API filtering
```

## Database Schema

### CustomImage Table
- id (PK)
- title
- file
- width, height
- created_at, uploaded_by_user
- copyright_holder
- source_url
- alt_text_override
- collection_id (FK)

### CustomImage_categories (M2M)
- customimage_id (FK)
- category_id (FK)

### CustomImage_tags (M2M via taggit)
- customimage_id (FK)
- tag_id (FK)

### CustomDocument Table
- id (PK)
- title
- file
- created_at, uploaded_by_user
- document_version
- expiry_date
- department
- collection_id (FK)

### CustomDocument_tags (M2M via taggit)
- customdocument_id (FK)
- tag_id (FK)

### Category Table
- id (PK)
- name
- slug (unique)
- description
- locale_id (FK for translations)

## API Endpoints

### Images
- `GET /api/media/images/` - List all images
- `GET /api/media/images/<id>/` - Get image detail
- `GET /api/media/images/recent/` - Get recent images
- `GET /api/media/images/<id>/related/` - Get related images
- `GET /api/media/images/?search=<query>` - Search images
- `GET /api/media/images/?categories__slug=<slug>` - Filter by category

### Documents
- `GET /api/media/documents/` - List all documents
- `GET /api/media/documents/<id>/` - Get document detail
- `GET /api/media/documents/recent/` - Get recent documents
- `GET /api/media/documents/expiring_soon/` - Get expiring documents
- `GET /api/media/documents/?search=<query>` - Search documents
- `GET /api/media/documents/?department=<dept>` - Filter by department

### Categories
- `GET /api/media/categories/` - List all categories
- `GET /api/media/categories/<slug>/` - Get category detail

## Frontend URLs

- `/media/gallery/` - Main media gallery
- `/media/image/<id>/` - Image detail page
- `/media/document/<id>/` - Document detail page
- `/media/category/<slug>/` - Category filtered view
- `/media/api/stats/` - Media statistics JSON

## Admin URLs

- `/admin/` - Wagtail admin dashboard
- `/admin/images/` - Image management
- `/admin/documents/` - Document management
- `/admin/snippets/media_enhancements/category/` - Category management
- `/django-admin/` - Django admin (if needed)

## Static Files

### CSS
- Bootstrap 5 (CDN)
- Custom styles in base.html

### JavaScript
- Bootstrap 5 Bundle (CDN)
- Custom JS in templates

### Icons
- Font Awesome 6 (CDN)

## Media Files

### Images
Stored in: `media/images/`
- Original images
- Renditions (generated on-demand)

### Documents
Stored in: `media/documents/`
- PDF, DOCX, XLSX, etc.

## Environment Variables

### Development
- `DJANGO_SETTINGS_MODULE=my_cms_project.settings.dev`

### Production
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Comma-separated hosts
- `DATABASE_URL` - Database connection string
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_STORAGE_BUCKET_NAME` - S3 bucket name
- `AWS_S3_REGION_NAME` - AWS region

## Git Files

### .gitignore
Should include:
- `__pycache__/`
- `*.pyc`
- `.venv/`
- `db.sqlite3`
- `/media/`
- `/staticfiles/`
- `.env`
- `.DS_Store`

### .git/
Git repository data (created by `git init`)

## Next Steps

1. Run setup script: `./setup.sh` or `setup.bat`
2. Start server: `python manage.py runserver --settings=my_cms_project.settings.dev`
3. Visit admin: http://localhost:8000/admin/
4. Visit gallery: http://localhost:8000/media/gallery/
5. Test API: http://localhost:8000/api/media/
6. Upload media through admin
7. View in gallery
8. Test API endpoints
9. Customize as needed
10. Deploy to production

## Support Files

All documentation files are in the root directory:
- `RICH_MEDIA_ENHANCEMENTS.md` - Complete feature documentation
- `GITHUB_SETUP.md` - Git and GitHub guide
- `FILE_STRUCTURE.md` - This file
- `README.md` - Quick start guide (to be created)
