@echo off
REM Rich Media Library Setup Script for Windows
REM This script sets up the Wagtail Rich Media Library

echo =========================================
echo Wagtail Rich Media Library Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo + Python found
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo + Virtual environment created
) else (
    echo + Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo + Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo + Dependencies installed
echo.

REM Run migrations
echo Running database migrations...
python manage.py migrate --settings=my_cms_project.settings.dev
echo + Migrations complete
echo.

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput --settings=my_cms_project.settings.dev
echo + Static files collected
echo.

REM Create superuser prompt
echo Create a superuser account
echo (Press Ctrl+C to skip)
python manage.py createsuperuser --settings=my_cms_project.settings.dev
echo.

REM Generate sample media
set /p response="Generate sample media? (y/n): "
if /i "%response%"=="y" (
    echo Generating sample media...
    python manage.py generate_sample_media --settings=my_cms_project.settings.dev
    echo + Sample media generated
)
echo.

echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To start the development server, run:
echo   python manage.py runserver --settings=my_cms_project.settings.dev
echo.
echo Then visit:
echo   Admin:   http://localhost:8000/admin/
echo   Gallery: http://localhost:8000/media/gallery/
echo   API:     http://localhost:8000/api/media/
echo.
echo =========================================
pause
