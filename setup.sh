#!/bin/bash

# Rich Media Library Setup Script
# This script sets up the Wagtail Rich Media Library

echo "========================================="
echo "Wagtail Rich Media Library Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate || source .venv/Scripts/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --settings=my_cms_project.settings.dev
echo "✓ Migrations complete"
echo ""

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=my_cms_project.settings.dev
echo "✓ Static files collected"
echo ""

# Create superuser prompt
echo "👤 Create a superuser account"
echo "   (Press Ctrl+C to skip)"
python manage.py createsuperuser --settings=my_cms_project.settings.dev || echo "Skipped superuser creation"
echo ""

# Generate sample media
echo "🎨 Generate sample media? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Generating sample media..."
    python manage.py generate_sample_media --settings=my_cms_project.settings.dev
    echo "✓ Sample media generated"
fi
echo ""

echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver --settings=my_cms_project.settings.dev"
echo ""
echo "Then visit:"
echo "  Admin:   http://localhost:8000/admin/"
echo "  Gallery: http://localhost:8000/media/gallery/"
echo "  API:     http://localhost:8000/api/media/"
echo ""
echo "========================================="
