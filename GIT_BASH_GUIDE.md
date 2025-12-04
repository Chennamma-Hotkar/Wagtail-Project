# Git Bash Quick Start Guide

## ✅ Now You Can Use Simple Commands!

The project is now configured to use development settings by default, so you can use simple commands in Git Bash.

## 🚀 Quick Start Commands

### 1. Navigate to Project
```bash
cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media"
```

### 2. Activate Virtual Environment
```bash
source .venv/Scripts/activate
```

### 3. Run Server (Simple Command!)
```bash
python manage.py runserver
```

That's it! No need to specify `--settings=my_cms_project.settings.dev` anymore!

## 📋 Common Commands (Simplified)

### Database
```bash
# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Show migrations
python manage.py showmigrations
```

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword username
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic

# Collect without prompts
python manage.py collectstatic --noinput
```

### Custom Commands
```bash
# Generate sample media
python manage.py generate_sample_media

# Cleanup expired documents
python manage.py cleanup_expired_documents --dry-run
python manage.py cleanup_expired_documents
```

### Django Shell
```bash
# Open Django shell
python manage.py shell
```

### Other Useful Commands
```bash
# Check for issues
python manage.py check

# Update search index
python manage.py update_index

# Show all available commands
python manage.py help
```

## 🌐 Access URLs

Once the server is running:

- **Admin**: http://localhost:8000/admin/
- **Gallery**: http://localhost:8000/media/gallery/
- **API**: http://localhost:8000/api/media/
- **Images API**: http://localhost:8000/api/media/images/
- **Documents API**: http://localhost:8000/api/media/documents/

## 🔧 Git Bash Tips

### Path Format
In Git Bash, use forward slashes:
```bash
cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media"
```

### Activate Virtual Environment
```bash
# Git Bash
source .venv/Scripts/activate

# You'll see (.venv) in your prompt when activated
```

### Check if Virtual Environment is Active
```bash
which python
# Should show: .venv/Scripts/python
```

### Deactivate Virtual Environment
```bash
deactivate
```

## 📦 Complete Workflow Example

```bash
# 1. Navigate to project
cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media"

# 2. Activate virtual environment
source .venv/Scripts/activate

# 3. Install/update dependencies (if needed)
pip install -r requirements.txt

# 4. Run migrations (if needed)
python manage.py migrate

# 5. Start server
python manage.py runserver

# Server is now running at http://localhost:8000/
```

## 🛑 Stop the Server

Press `Ctrl + C` in the terminal

## 🔄 Restart the Server

Just run again:
```bash
python manage.py runserver
```

## 🎯 First Time Setup

If this is your first time:

```bash
# 1. Navigate to project
cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media"

# 2. Create virtual environment (if not exists)
python -m venv .venv

# 3. Activate virtual environment
source .venv/Scripts/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Generate sample data (optional)
python manage.py generate_sample_media

# 8. Start server
python manage.py runserver
```

## 🐛 Troubleshooting

### "python: command not found"
Try:
```bash
python3 manage.py runserver
```

### "No module named django"
Make sure virtual environment is activated:
```bash
source .venv/Scripts/activate
pip install -r requirements.txt
```

### "Port already in use"
Use a different port:
```bash
python manage.py runserver 8080
```

### Virtual Environment Not Activating
Make sure you're in the project directory:
```bash
cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media"
source .venv/Scripts/activate
```

## 📝 Environment Variables (Optional)

If you want to use different settings:

```bash
# Use production settings
export DJANGO_SETTINGS_MODULE=my_cms_project.settings.production
python manage.py runserver

# Or specify directly
python manage.py runserver --settings=my_cms_project.settings.production
```

## 🎨 Useful Aliases (Optional)

Add to your `~/.bashrc` or `~/.bash_profile`:

```bash
# Django aliases
alias dj='python manage.py'
alias djrun='python manage.py runserver'
alias djmig='python manage.py migrate'
alias djmake='python manage.py makemigrations'
alias djshell='python manage.py shell'
alias djsu='python manage.py createsuperuser'

# Project alias
alias wagtail='cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media" && source .venv/Scripts/activate'
```

Then reload:
```bash
source ~/.bashrc
```

Now you can use:
```bash
wagtail      # Navigate to project and activate venv
djrun        # Run server
djmig        # Run migrations
```

## 🚀 Quick Daily Workflow

```bash
# Morning: Start working
cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media"
source .venv/Scripts/activate
python manage.py runserver

# Work on your project...

# Evening: Stop server
# Press Ctrl + C
deactivate
```

## 📚 More Help

- **Complete Documentation**: See `README.md`
- **All Commands**: See `COMMANDS_REFERENCE.md`
- **Quick Start**: See `QUICK_START.md`
- **GitHub Setup**: See `GITHUB_SETUP.md`

---

**Happy Coding! 🎉**
