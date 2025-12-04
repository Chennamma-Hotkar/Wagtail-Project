# 🚀 Quick Start Guide

Get your Rich Media Library up and running in 5 minutes!

## Prerequisites

- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ Command line access

## Option 1: Automated Setup (Recommended) ⚡

### Linux/Mac

```bash
chmod +x setup.sh
./setup.sh
```

### Windows

```cmd
setup.bat
```

That's it! The script will:
1. Create virtual environment
2. Install dependencies
3. Run migrations
4. Collect static files
5. Create superuser (you'll be prompted)
6. Generate sample data (optional)

## Option 2: Manual Setup (5 Steps) 📝

### Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 2: Activate Virtual Environment

**Linux/Mac:**
```bash
source .venv/bin/activate
```

**Windows:**
```cmd
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Database

```bash
python manage.py migrate --settings=my_cms_project.settings.dev
```

### Step 5: Create Admin User

```bash
python manage.py createsuperuser --settings=my_cms_project.settings.dev
```

## Start the Server 🎬

```bash
python manage.py runserver --settings=my_cms_project.settings.dev
```

## Access Your Application 🌐

Open your browser and visit:

### 1. Admin Panel
```
http://localhost:8000/admin/
```
Login with the superuser credentials you created.

### 2. Media Gallery
```
http://localhost:8000/media/gallery/
```
Beautiful frontend gallery for browsing media.

### 3. REST API
```
http://localhost:8000/api/media/
```
Browsable REST API interface.

## First Steps 👣

### 1. Upload Your First Image

1. Go to http://localhost:8000/admin/
2. Click "Images" in the sidebar
3. Click "Add an image"
4. Fill in:
   - **Title**: My First Image
   - **File**: Upload an image
   - **Copyright Holder**: Your Name
   - **Tags**: test, sample
5. Click "Save"

### 2. Create a Category

1. In admin, click "Snippets" → "Categories"
2. Click "Add category"
3. Fill in:
   - **Name**: Photography
   - **Slug**: photography (auto-filled)
   - **Description**: Photography images
4. Click "Save"

### 3. View in Gallery

1. Go to http://localhost:8000/media/gallery/
2. See your uploaded image
3. Click on it for details
4. Try the search and filters

### 4. Test the API

Open a new terminal and try:

```bash
# Get all images
curl http://localhost:8000/api/media/images/

# Or visit in browser
http://localhost:8000/api/media/images/
```

## Generate Sample Data 🎨

Want to see the gallery with sample data?

```bash
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

This creates:
- 4 sample categories
- 5 colored sample images
- Tags and category assignments

## Common Commands 📋

### Start Server
```bash
python manage.py runserver --settings=my_cms_project.settings.dev
```

### Create Superuser
```bash
python manage.py createsuperuser --settings=my_cms_project.settings.dev
```

### Generate Sample Data
```bash
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

### Run Migrations
```bash
python manage.py migrate --settings=my_cms_project.settings.dev
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput --settings=my_cms_project.settings.dev
```

## Troubleshooting 🔧

### "Command not found: python"

Try `python3` instead:
```bash
python3 -m venv .venv
python3 manage.py runserver --settings=my_cms_project.settings.dev
```

### "No module named django"

Make sure virtual environment is activated:
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

### "Port already in use"

Use a different port:
```bash
python manage.py runserver 8080 --settings=my_cms_project.settings.dev
```

### Images not displaying

Make sure you're running in DEBUG mode (dev settings) or configure media serving for production.

## What's Next? 🎯

### Explore Features

1. **Upload Documents**
   - Go to admin → Documents
   - Upload PDFs, Word docs, etc.
   - Set expiry dates and departments

2. **Organize with Categories**
   - Create more categories
   - Assign images to categories
   - Filter by category in gallery

3. **Use Tags**
   - Add tags to images and documents
   - Search by tags
   - Organize your media library

4. **Try the API**
   - Visit http://localhost:8000/api/media/
   - Test filtering: `?categories__slug=nature`
   - Test search: `?search=sample`
   - Get recent: `/api/media/images/recent/`

### Customize

1. **Add Custom Fields**
   - Edit `media_enhancements/models.py`
   - Add your fields
   - Run migrations

2. **Customize Templates**
   - Edit files in `media_enhancements/templates/`
   - Change colors, layout, etc.

3. **Extend API**
   - Edit `media_enhancements/api_views.py`
   - Add custom endpoints

### Deploy to Production

See `RICH_MEDIA_ENHANCEMENTS.md` for production deployment guide.

## Quick Reference 📚

### URLs
- Admin: http://localhost:8000/admin/
- Gallery: http://localhost:8000/media/gallery/
- API: http://localhost:8000/api/media/
- Images API: http://localhost:8000/api/media/images/
- Documents API: http://localhost:8000/api/media/documents/
- Categories API: http://localhost:8000/api/media/categories/

### Documentation Files
- `README.md` - Project overview
- `RICH_MEDIA_ENHANCEMENTS.md` - Complete documentation
- `GITHUB_SETUP.md` - Git and GitHub guide
- `FILE_STRUCTURE.md` - Project structure
- `COMMANDS_REFERENCE.md` - All commands
- `IMPLEMENTATION_SUMMARY.md` - What was built
- `QUICK_START.md` - This file

### Key Directories
- `media_enhancements/` - Main app
- `media_enhancements/templates/` - HTML templates
- `media_enhancements/management/commands/` - Custom commands
- `my_cms_project/settings/` - Settings files

## Need Help? 🆘

1. Check the documentation files
2. Review error messages carefully
3. Make sure virtual environment is activated
4. Verify all dependencies are installed
5. Check Python version (3.8+)

## Success! 🎉

If you can:
- ✅ Access the admin panel
- ✅ Upload an image
- ✅ View the gallery
- ✅ Access the API

**You're all set!** Start building your rich media library.

---

**Time to Complete**: ~5 minutes

**Difficulty**: Easy ⭐

**Next Steps**: Upload media, explore features, customize!

---

**Happy Building! 🚀**
