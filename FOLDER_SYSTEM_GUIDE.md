# 📁 Folder System Guide

## Overview

The folder system provides hierarchical organization for all media types (Images, Videos, Audio, Documents) in your Wagtail CMS. This makes it easy to keep your media library clean and organized.

## Features

### ✨ Key Features

1. **Hierarchical Structure** - Create folders within folders for deep organization
2. **Breadcrumb Navigation** - Easy navigation through folder hierarchy
3. **Move Media** - Drag and drop or move media between folders
4. **Folder Management** - Create, rename, and delete folders
5. **Visual Organization** - Custom icons and colors for folders
6. **Media Count** - See how many items are in each folder
7. **System Folders** - Protected folders that cannot be deleted

## Pre-configured Folders

The system comes with these sample folders:

```
Root
├── Banners (Marketing banners and promotional images)
├── Products (Product images and media)
├── Campaigns (Marketing campaign assets)
│   └── 2024 Launch (Assets for 2024 product launch campaign)
├── Social Media (Social media posts and graphics)
├── Logos (Company and brand logos) [Protected]
├── Videos (Video content and recordings)
├── Audio (Audio files and music)
└── Documents (PDFs and other documents)
```

## Using the Folder System

### Accessing the Dashboard

1. Log into Wagtail admin
2. Click on **"Dashboard"** in the main navigation
3. You'll see folders at the top, followed by media files

### Creating a New Folder

1. Click the **"New Folder"** button
2. Enter folder name and optional description
3. Click **"Create Folder"**
4. The folder will be created in your current location

**Creating Subfolders:**
- Navigate into a folder first
- Click "New Folder" to create a subfolder inside it

### Navigating Folders

**Breadcrumb Navigation:**
- Use the breadcrumb trail at the top to navigate back
- Click "Root" to go to the top level
- Click any folder name in the breadcrumb to jump to that level

**Folder Cards:**
- Click on any folder card to open it
- Folder cards show:
  - Number of media items inside
  - Number of subfolders
  - Folder description

### Moving Media to Folders

**Method 1: During Upload**
1. When uploading media in Wagtail admin
2. Select the "Folder" field
3. Choose the destination folder

**Method 2: Move Existing Media**
1. Go to the media item's edit page in Wagtail admin
2. Change the "Folder" field
3. Save the changes

**Method 3: Bulk Move (Future Enhancement)**
- Select multiple items
- Click "Move to Folder"
- Choose destination

### Renaming a Folder

1. Navigate to the folder you want to rename
2. Click **"Rename Folder"** button
3. Enter the new name
4. Click **"Rename"**

### Deleting a Folder

**Requirements:**
- Folder must be empty (no media files)
- Folder must not be a system folder
- All subfolders must also be empty

**Steps:**
1. Navigate to the folder
2. Click **"Delete Folder"** button
3. Confirm the deletion

**Note:** Move or delete all media and subfolders before deleting a folder.

## Folder Properties

### Standard Properties

- **Name** - Display name of the folder
- **Slug** - URL-friendly identifier
- **Description** - Optional description
- **Icon** - Font Awesome icon (e.g., 'fa-folder', 'fa-box')
- **Color** - Hex color code for visual identification
- **Order** - Display order (lower numbers appear first)

### Special Properties

- **Parent** - Parent folder for hierarchy
- **System Folder** - Protected from deletion
- **Created By** - User who created the folder
- **Created At** - Creation timestamp

## Management Commands

### Setup Sample Folders

Create the default folder structure:

```bash
python manage.py setup_folders
```

This creates:
- Banners
- Products
- Campaigns (with "2024 Launch" subfolder)
- Social Media
- Logos (protected)
- Videos
- Audio
- Documents

## Best Practices

### Organization Tips

1. **Use Descriptive Names** - Make folder names clear and specific
2. **Limit Depth** - Try to keep hierarchy to 2-3 levels maximum
3. **Group by Purpose** - Organize by campaign, project, or content type
4. **Use Colors** - Assign different colors to different types of folders
5. **Add Descriptions** - Help team members understand folder purpose

### Naming Conventions

**Good Examples:**
- `2024 Spring Campaign`
- `Product Photos - Electronics`
- `Social Media - Instagram`
- `Banners - Homepage`

**Avoid:**
- Generic names like "Folder 1", "Misc", "Stuff"
- Special characters that might cause URL issues
- Extremely long names

### Folder Structure Examples

**By Campaign:**
```
Campaigns
├── 2024 Spring Launch
├── 2024 Summer Sale
└── 2024 Holiday Campaign
```

**By Product Line:**
```
Products
├── Electronics
│   ├── Phones
│   └── Laptops
├── Clothing
└── Accessories
```

**By Content Type:**
```
Marketing Assets
├── Banners
├── Social Media
│   ├── Facebook
│   ├── Instagram
│   └── Twitter
└── Email Templates
```

## Technical Details

### Database Model

The `MediaFolder` model includes:
- Hierarchical structure using self-referencing foreign key
- Soft delete protection for system folders
- Automatic slug generation
- Media count methods
- Breadcrumb generation

### Media Models Integration

All media models have a `folder` field:
- `CustomImage.folder`
- `CustomDocument.folder`
- `Video.folder`
- `Audio.folder`

### URL Structure

```
/media/dashboard/                    # Root level
/media/dashboard/?folder=1           # Inside folder with ID 1
/media/dashboard/?folder=1&type=image # Filter by type in folder
```

### API Endpoints

- `POST /media/folder/create/` - Create new folder
- `POST /media/folder/<id>/rename/` - Rename folder
- `DELETE /media/folder/<id>/delete/` - Delete folder
- `POST /media/media/move/` - Move media to folder

## Troubleshooting

### Cannot Delete Folder

**Problem:** "Cannot delete folder" error

**Solutions:**
1. Check if folder contains media files - move or delete them first
2. Check if folder has subfolders - delete or move them first
3. Check if it's a system folder - these cannot be deleted

### Folder Not Showing

**Problem:** Created folder doesn't appear

**Solutions:**
1. Refresh the page
2. Check if you're in the correct parent folder
3. Check folder order - it might be sorted differently

### Media Not in Folder

**Problem:** Moved media doesn't appear in folder

**Solutions:**
1. Refresh the page
2. Check if filters are applied
3. Verify the media was saved after changing folder

## Future Enhancements

Planned features:
- Drag and drop media between folders
- Bulk move operations
- Folder permissions and access control
- Folder templates
- Smart folders (auto-organize by rules)
- Folder sharing and collaboration
- Folder statistics and analytics

## Support

For issues or questions:
1. Check this guide first
2. Review the Django admin logs
3. Check browser console for JavaScript errors
4. Verify database migrations are applied

## Related Documentation

- [Unified Dashboard Guide](UNIFIED_DASHBOARD_GUIDE.md)
- [Image Editor Guide](IMAGE_EDITOR_GUIDE.md)
- [Rich Media Enhancements](RICH_MEDIA_ENHANCEMENTS.md)
