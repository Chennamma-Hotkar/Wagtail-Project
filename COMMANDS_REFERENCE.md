# Complete Commands Reference

## Quick Start Commands

### Setup (Automated)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Setup (Manual)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Linux/Mac)
source .venv/bin/activate

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --settings=my_cms_project.settings.dev

# Create superuser
python manage.py createsuperuser --settings=my_cms_project.settings.dev

# Collect static files
python manage.py collectstatic --noinput --settings=my_cms_project.settings.dev

# Generate sample data
python manage.py generate_sample_media --settings=my_cms_project.settings.dev

# Run server
python manage.py runserver --settings=my_cms_project.settings.dev
```

## Django Management Commands

### Database

```bash
# Create migrations
python manage.py makemigrations --settings=my_cms_project.settings.dev

# Apply migrations
python manage.py migrate --settings=my_cms_project.settings.dev

# Show migrations
python manage.py showmigrations --settings=my_cms_project.settings.dev

# SQL for migration
python manage.py sqlmigrate media_enhancements 0001 --settings=my_cms_project.settings.dev

# Reset database (SQLite only)
rm db.sqlite3
python manage.py migrate --settings=my_cms_project.settings.dev
```

### User Management

```bash
# Create superuser
python manage.py createsuperuser --settings=my_cms_project.settings.dev

# Change user password
python manage.py changepassword username --settings=my_cms_project.settings.dev
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic --settings=my_cms_project.settings.dev

# Collect without prompts
python manage.py collectstatic --noinput --settings=my_cms_project.settings.dev

# Clear collected static files
python manage.py collectstatic --clear --noinput --settings=my_cms_project.settings.dev
```

### Development Server

```bash
# Run development server
python manage.py runserver --settings=my_cms_project.settings.dev

# Run on specific port
python manage.py runserver 8080 --settings=my_cms_project.settings.dev

# Run on all interfaces
python manage.py runserver 0.0.0.0:8000 --settings=my_cms_project.settings.dev
```

### Shell

```bash
# Django shell
python manage.py shell --settings=my_cms_project.settings.dev

# Django shell with IPython
python manage.py shell -i ipython --settings=my_cms_project.settings.dev
```

## Custom Management Commands

### Generate Sample Media

```bash
# Generate sample images and categories
python manage.py generate_sample_media --settings=my_cms_project.settings.dev
```

### Cleanup Expired Documents

```bash
# Dry run (preview what would be deleted)
python manage.py cleanup_expired_documents --dry-run --settings=my_cms_project.settings.dev

# Actually delete expired documents
python manage.py cleanup_expired_documents --settings=my_cms_project.settings.dev
```

## Wagtail Commands

```bash
# Update search index
python manage.py update_index --settings=my_cms_project.settings.dev

# Rebuild search index
python manage.py rebuild_index --settings=my_cms_project.settings.dev

# Publish scheduled pages
python manage.py publish_scheduled_pages --settings=my_cms_project.settings.dev

# Move pages
python manage.py move_pages --settings=my_cms_project.settings.dev

# Import images
python manage.py import_images /path/to/images --settings=my_cms_project.settings.dev
```

## Git Commands

### Initial Setup

```bash
# Initialize repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Rich Media Library Enhancements"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/wagtail-rich-media.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Daily Workflow

```bash
# Check status
git status

# Add files
git add .
git add filename.py

# Commit changes
git commit -m "Description of changes"

# Push to remote
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# View changes
git diff
```

### Branching

```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
git checkout development

# List branches
git branch

# Merge branch
git checkout main
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature

# Push branch to remote
git push -u origin feature/new-feature
```

### Tagging

```bash
# Create tag
git tag -a v1.0.0 -m "Version 1.0.0"

# Push tag
git push origin v1.0.0

# Push all tags
git push --tags

# List tags
git tag

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## Python/Pip Commands

### Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Deactivate
deactivate
```

### Package Management

```bash
# Install requirements
pip install -r requirements.txt

# Install single package
pip install package-name

# Install specific version
pip install package-name==1.0.0

# Upgrade package
pip install --upgrade package-name

# Uninstall package
pip uninstall package-name

# List installed packages
pip list

# Show package info
pip show package-name

# Generate requirements
pip freeze > requirements.txt

# Check for outdated packages
pip list --outdated
```

## Testing Commands

### Django Tests

```bash
# Run all tests
python manage.py test --settings=my_cms_project.settings.dev

# Run specific app tests
python manage.py test media_enhancements --settings=my_cms_project.settings.dev

# Run specific test
python manage.py test media_enhancements.tests.TestClassName --settings=my_cms_project.settings.dev

# Run with verbosity
python manage.py test --verbosity=2 --settings=my_cms_project.settings.dev

# Keep test database
python manage.py test --keepdb --settings=my_cms_project.settings.dev
```

### Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test --settings=my_cms_project.settings.dev

# Generate report
coverage report

# Generate HTML report
coverage html

# View HTML report
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows
```

## API Testing Commands

### Using curl

```bash
# Get all images
curl http://localhost:8000/api/media/images/

# Get specific image
curl http://localhost:8000/api/media/images/1/

# Search images
curl "http://localhost:8000/api/media/images/?search=nature"

# Filter by category
curl "http://localhost:8000/api/media/images/?categories__slug=technology"

# Get recent images
curl http://localhost:8000/api/media/images/recent/

# Get all documents
curl http://localhost:8000/api/media/documents/

# Get expiring documents
curl http://localhost:8000/api/media/documents/expiring_soon/

# Get categories
curl http://localhost:8000/api/media/categories/

# With authentication
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/media/images/
```

### Using httpie

```bash
# Install httpie
pip install httpie

# Get all images
http GET http://localhost:8000/api/media/images/

# Search images
http GET http://localhost:8000/api/media/images/ search==nature

# Filter by category
http GET http://localhost:8000/api/media/images/ categories__slug==technology

# With authentication
http GET http://localhost:8000/api/media/images/ "Authorization: Token YOUR_TOKEN"
```

### Using Python requests

```python
import requests

# Get all images
response = requests.get('http://localhost:8000/api/media/images/')
print(response.json())

# Search images
response = requests.get(
    'http://localhost:8000/api/media/images/',
    params={'search': 'nature'}
)
print(response.json())

# With authentication
headers = {'Authorization': 'Token YOUR_TOKEN'}
response = requests.get(
    'http://localhost:8000/api/media/images/',
    headers=headers
)
print(response.json())
```

## Database Commands

### PostgreSQL

```bash
# Create database
createdb wagtail_media

# Drop database
dropdb wagtail_media

# Backup database
pg_dump wagtail_media > backup.sql

# Restore database
psql wagtail_media < backup.sql

# Connect to database
psql wagtail_media
```

### SQLite

```bash
# Open database
sqlite3 db.sqlite3

# Backup database
cp db.sqlite3 db.sqlite3.backup

# Restore database
cp db.sqlite3.backup db.sqlite3

# Export to SQL
sqlite3 db.sqlite3 .dump > backup.sql

# Import from SQL
sqlite3 db.sqlite3 < backup.sql
```

## Production Commands

### Deployment

```bash
# Set environment variables
export SECRET_KEY="your-secret-key"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
export DATABASE_URL="postgres://user:pass@host:port/dbname"

# Collect static files
python manage.py collectstatic --noinput --settings=my_cms_project.settings.production

# Run migrations
python manage.py migrate --settings=my_cms_project.settings.production

# Create superuser
python manage.py createsuperuser --settings=my_cms_project.settings.production

# Check deployment
python manage.py check --deploy --settings=my_cms_project.settings.production
```

### Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn my_cms_project.wsgi:application --bind 0.0.0.0:8000

# Run with workers
gunicorn my_cms_project.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Run as daemon
gunicorn my_cms_project.wsgi:application --bind 0.0.0.0:8000 --daemon
```

### Docker

```bash
# Build image
docker build -t wagtail-media .

# Run container
docker run -p 8000:8000 wagtail-media

# Run with environment variables
docker run -p 8000:8000 -e SECRET_KEY="key" wagtail-media

# Docker Compose
docker-compose up
docker-compose up -d  # Detached mode
docker-compose down
docker-compose logs
```

## Maintenance Commands

### Clear Cache

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Clear Django cache
python manage.py clear_cache --settings=my_cms_project.settings.dev
```

### Check for Issues

```bash
# Check for problems
python manage.py check --settings=my_cms_project.settings.dev

# Check deployment settings
python manage.py check --deploy --settings=my_cms_project.settings.production

# Validate templates
python manage.py validate_templates --settings=my_cms_project.settings.dev
```

### Database Optimization

```bash
# Optimize database (PostgreSQL)
python manage.py dbshell --settings=my_cms_project.settings.dev
VACUUM ANALYZE;

# SQLite optimize
sqlite3 db.sqlite3 "VACUUM;"
```

## Useful Shortcuts

### Create Alias (Linux/Mac)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias dj='python manage.py'
alias djrun='python manage.py runserver --settings=my_cms_project.settings.dev'
alias djmig='python manage.py migrate --settings=my_cms_project.settings.dev'
alias djmake='python manage.py makemigrations --settings=my_cms_project.settings.dev'
alias djshell='python manage.py shell --settings=my_cms_project.settings.dev'
alias djtest='python manage.py test --settings=my_cms_project.settings.dev'
```

Then use:
```bash
djrun  # Instead of python manage.py runserver --settings=...
djmig  # Instead of python manage.py migrate --settings=...
```

### Create Batch File (Windows)

Create `dj.bat`:

```batch
@echo off
python manage.py %* --settings=my_cms_project.settings.dev
```

Then use:
```cmd
dj runserver
dj migrate
dj makemigrations
```

## Environment Variables

### Set Environment Variables

**Linux/Mac:**
```bash
export DJANGO_SETTINGS_MODULE=my_cms_project.settings.dev
export SECRET_KEY="your-secret-key"
export DEBUG=True
```

**Windows:**
```cmd
set DJANGO_SETTINGS_MODULE=my_cms_project.settings.dev
set SECRET_KEY=your-secret-key
set DEBUG=True
```

**PowerShell:**
```powershell
$env:DJANGO_SETTINGS_MODULE="my_cms_project.settings.dev"
$env:SECRET_KEY="your-secret-key"
$env:DEBUG="True"
```

### Using .env File

Create `.env` file:
```
DJANGO_SETTINGS_MODULE=my_cms_project.settings.dev
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

Install python-decouple:
```bash
pip install python-decouple
```

Use in settings:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

## Quick Reference

### Most Used Commands

```bash
# Start development
source .venv/bin/activate  # or .venv\Scripts\activate
python manage.py runserver --settings=my_cms_project.settings.dev

# Make changes to models
python manage.py makemigrations --settings=my_cms_project.settings.dev
python manage.py migrate --settings=my_cms_project.settings.dev

# Create superuser
python manage.py createsuperuser --settings=my_cms_project.settings.dev

# Generate sample data
python manage.py generate_sample_media --settings=my_cms_project.settings.dev

# Git workflow
git add .
git commit -m "Description"
git push

# Install new package
pip install package-name
pip freeze > requirements.txt
```

## Troubleshooting Commands

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check Django version
python -m django --version

# Check installed packages
pip list

# Check for missing dependencies
pip check

# Verify virtual environment
which python  # Linux/Mac
where python  # Windows

# Check database connection
python manage.py dbshell --settings=my_cms_project.settings.dev

# Check migrations status
python manage.py showmigrations --settings=my_cms_project.settings.dev

# Validate models
python manage.py validate --settings=my_cms_project.settings.dev
```

---

**Tip**: Save this file for quick reference during development!
