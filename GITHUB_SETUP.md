# GitHub Setup Guide

## Step-by-Step GitHub Commands

### 1. Initialize Git Repository (if not already initialized)

```bash
cd wagtail-rich-media
git init
```

### 2. Create .gitignore File

```bash
# Create .gitignore if it doesn't exist
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Wagtail
/media/
*.pyc
EOF
```

### 3. Add All Files to Git

```bash
git add .
```

### 4. Create Initial Commit

```bash
git commit -m "Initial commit: Rich Media Library Enhancements for Wagtail CMS

Features:
- Custom Image and Document models with metadata
- Category and tagging system
- Frontend gallery with search and filtering
- REST API with full CRUD operations
- Wagtail admin integration
- Management commands for sample data and cleanup
- Responsive Bootstrap 5 templates
- Comprehensive documentation"
```

### 5. Create GitHub Repository

Go to GitHub (https://github.com) and:
1. Click the "+" icon in the top right
2. Select "New repository"
3. Name it: `wagtail-rich-media`
4. Add description: "Rich Media Library Enhancements for Wagtail CMS"
5. Choose Public or Private
6. **DO NOT** initialize with README, .gitignore, or license
7. Click "Create repository"

### 6. Add Remote Origin

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/wagtail-rich-media.git
```

### 7. Verify Remote

```bash
git remote -v
```

### 8. Push to GitHub

```bash
# For main branch
git branch -M main
git push -u origin main
```

Or if using master:

```bash
# For master branch
git branch -M master
git push -u origin master
```

### 9. Verify Upload

Visit your repository on GitHub:
```
https://github.com/YOUR_USERNAME/wagtail-rich-media
```

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Login to GitHub
gh auth login

# Create repository and push
gh repo create wagtail-rich-media --public --source=. --remote=origin --push
```

## Creating a README for GitHub

```bash
cat > README.md << 'EOF'
# Wagtail Rich Media Library

A comprehensive rich media management system for Wagtail CMS with advanced features for images and documents.

## Features

- 🖼️ Custom Image & Document Models
- 🏷️ Advanced Categorization & Tagging
- 🎨 Beautiful Frontend Gallery
- 🔌 REST API
- 📊 Media Statistics
- 🔍 Search & Filtering
- 📱 Responsive Design

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate --settings=my_cms_project.settings.dev
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser --settings=my_cms_project.settings.dev
   ```

4. Generate sample data:
   ```bash
   python manage.py generate_sample_media --settings=my_cms_project.settings.dev
   ```

5. Run server:
   ```bash
   python manage.py runserver --settings=my_cms_project.settings.dev
   ```

6. Visit:
   - Admin: http://localhost:8000/admin/
   - Gallery: http://localhost:8000/media/gallery/
   - API: http://localhost:8000/api/media/

## Documentation

See [RICH_MEDIA_ENHANCEMENTS.md](RICH_MEDIA_ENHANCEMENTS.md) for complete documentation.

## Tech Stack

- Wagtail CMS
- Django
- Django REST Framework
- Bootstrap 5
- Font Awesome

## License

MIT License
EOF

git add README.md
git commit -m "Add README.md"
git push
```

## Branching Strategy

### Create Development Branch

```bash
git checkout -b development
git push -u origin development
```

### Create Feature Branch

```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

### Merge Feature to Development

```bash
git checkout development
git merge feature/new-feature
git push
```

## Tagging Releases

```bash
# Create a tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"

# Push tag to GitHub
git push origin v1.0.0

# Push all tags
git push --tags
```

## Common Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# View changes
git diff

# Undo changes (before commit)
git checkout -- filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Pull latest changes
git pull origin main

# Create and switch to new branch
git checkout -b branch-name

# Switch branches
git checkout branch-name

# Delete branch locally
git branch -d branch-name

# Delete branch remotely
git push origin --delete branch-name
```

## GitHub Actions (Optional)

Create `.github/workflows/django.yml`:

```yaml
name: Django CI

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main, development ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run Migrations
      run: |
        python manage.py migrate --settings=my_cms_project.settings.dev
    
    - name: Run Tests
      run: |
        python manage.py test --settings=my_cms_project.settings.dev
```

## Troubleshooting

### Authentication Issues

If you have authentication issues:

```bash
# Use SSH instead of HTTPS
git remote set-url origin git@github.com:YOUR_USERNAME/wagtail-rich-media.git

# Or use personal access token
# Go to GitHub Settings > Developer settings > Personal access tokens
# Generate new token and use it as password
```

### Large Files

If you have large files:

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.mp4"

# Add .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

## Best Practices

1. **Commit Often**: Make small, focused commits
2. **Write Good Messages**: Use descriptive commit messages
3. **Use Branches**: Don't commit directly to main
4. **Pull Before Push**: Always pull latest changes before pushing
5. **Review Changes**: Use `git diff` before committing
6. **Ignore Sensitive Data**: Never commit secrets or credentials
7. **Tag Releases**: Use semantic versioning (v1.0.0, v1.1.0, etc.)

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitHub CLI](https://cli.github.com/)
