# ✅ Simplified Commands - No More Long Settings!

## 🎉 Good News!

The project is now configured to use **development settings by default**, so you can use simple commands!

## Before vs After

### ❌ Before (Long Commands)
```bash
python manage.py runserver --settings=my_cms_project.settings.dev
python manage.py migrate --settings=my_cms_project.settings.dev
python manage.py createsuperuser --settings=my_cms_project.settings.dev
```

### ✅ After (Simple Commands)
```bash
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
```

**Much easier!** 🚀

## 🔧 What Changed?

The `manage.py` file now defaults to `my_cms_project.settings.dev`, so you don't need to specify it every time.

## 📋 All Simplified Commands

### Server
```bash
python manage.py runserver
python manage.py runserver 8080  # Different port
```

### Database
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py showmigrations
```

### Users
```bash
python manage.py createsuperuser
python manage.py changepassword username
```

### Static Files
```bash
python manage.py collectstatic
python manage.py collectstatic --noinput
```

### Custom Commands
```bash
python manage.py setup_folders                    # Create sample folder structure
python manage.py generate_sample_media            # Generate sample media
python manage.py cleanup_expired_documents        # Clean up expired docs
python manage.py cleanup_expired_documents --dry-run  # Preview cleanup
```

### Other
```bash
python manage.py shell
python manage.py check
python manage.py help
```

## 🌐 For Git Bash Users

See **GIT_BASH_GUIDE.md** for complete Git Bash instructions!

Quick start:
```bash
cd "C:/Users/chann/OneDrive/Apps/Desktop/Rich Media/wagtail-rich-media"
source .venv/Scripts/activate
python manage.py runserver
```

## 🎯 Production Settings

If you need to use production settings, you can still specify:

```bash
python manage.py runserver --settings=my_cms_project.settings.production
```

Or set environment variable:
```bash
export DJANGO_SETTINGS_MODULE=my_cms_project.settings.production
python manage.py runserver
```

## 📚 Documentation Updated

All documentation files still show the full commands for clarity, but you can now use the simplified versions!

---

**Enjoy the simpler commands! 🎉**
