# 📁 Folder System - Quick Start

## 🚀 Get Started in 3 Steps

### Step 1: Create Folders
```bash
python manage.py setup_folders
```

This creates:
- Banners
- Products  
- Campaigns (with "2024 Launch" subfolder)
- Social Media
- Logos
- Videos
- Audio
- Documents

### Step 2: Access Dashboard
Visit: http://localhost:8000/media/dashboard/

### Step 3: Start Organizing!
- Click folders to navigate
- Click "New Folder" to create more
- Upload media and assign to folders

## 📋 Common Tasks

### Create a New Folder
1. Click **"New Folder"** button
2. Enter name (e.g., "Summer Campaign")
3. Add description (optional)
4. Click **"Create Folder"**

### Create a Subfolder
1. Navigate into parent folder
2. Click **"New Folder"**
3. Enter name
4. Click **"Create Folder"**

### Move Media to Folder
**Option 1: During Upload**
1. Go to Wagtail admin
2. Upload new media
3. Select folder from dropdown
4. Save

**Option 2: Edit Existing**
1. Go to Wagtail admin
2. Edit media item
3. Change "Folder" field
4. Save

### Navigate Folders
- Click folder cards to open
- Use breadcrumbs to go back
- Click "Root" to return to top

### Rename a Folder
1. Navigate to the folder
2. Click **"Rename Folder"**
3. Enter new name
4. Click **"Rename"**

### Delete a Folder
1. Move or delete all media inside
2. Delete or move all subfolders
3. Click **"Delete Folder"**
4. Confirm deletion

**Note:** System folders (like "Logos") cannot be deleted.

## 🎯 Example Workflows

### Organize by Campaign
```
Campaigns
├── 2024 Spring Launch
├── 2024 Summer Sale
└── 2024 Holiday Campaign
```

### Organize by Product
```
Products
├── Electronics
│   ├── Phones
│   └── Laptops
└── Clothing
```

### Organize by Content Type
```
Marketing
├── Banners
├── Social Media
│   ├── Facebook
│   ├── Instagram
│   └── Twitter
└── Email Templates
```

## 💡 Tips

1. **Use descriptive names** - "2024 Spring Campaign" not "Folder 1"
2. **Keep it shallow** - 2-3 levels deep is usually enough
3. **Use colors** - Assign different colors to different types
4. **Add descriptions** - Help your team understand folder purpose
5. **Plan structure** - Think about how you'll organize before creating many folders

## 🔗 URLs

- Dashboard: `/media/dashboard/`
- Inside folder: `/media/dashboard/?folder=1`
- Filter by type: `/media/dashboard/?folder=1&type=image`

## 📚 More Information

- **Full Guide:** [FOLDER_SYSTEM_GUIDE.md](FOLDER_SYSTEM_GUIDE.md)
- **Implementation:** [FOLDER_SYSTEM_IMPLEMENTATION.md](FOLDER_SYSTEM_IMPLEMENTATION.md)
- **Dashboard Guide:** [UNIFIED_DASHBOARD_GUIDE.md](UNIFIED_DASHBOARD_GUIDE.md)

## ❓ Troubleshooting

**Can't delete folder?**
- Make sure it's empty (no media files)
- Make sure it has no subfolders
- Check if it's a system folder

**Folder not showing?**
- Refresh the page
- Check if you're in the right parent folder

**Media not in folder?**
- Refresh the page
- Check if filters are applied
- Verify the media was saved

## 🎉 You're Ready!

Start organizing your media library with folders today!

Visit: http://localhost:8000/media/dashboard/
