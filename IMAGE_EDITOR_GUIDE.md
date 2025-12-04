# 🎨 Advanced Image Editor Guide

## Overview

The **Advanced Image Editor** provides powerful image editing capabilities built with Pillow (PIL). Edit images directly in your browser with professional-grade tools.

## ✨ Features

### 1. **Transform Tools**
- ✅ Rotate (90°, -90°, custom angles)
- ✅ Flip Horizontal (Mirror)
- ✅ Flip Vertical
- ✅ Crop to custom coordinates
- ✅ Crop to preset aspect ratios

### 2. **Aspect Ratios**
- Square (1:1) - Instagram, Profile Pictures
- Landscape (16:9) - YouTube, Widescreen
- Portrait (9:16) - Stories, Mobile
- Standard (4:3) - Classic TV
- Classic (3:2) - Photography
- Facebook Cover (820:312)
- Twitter Header (1500:500)
- YouTube Thumbnail (1280:720)

### 3. **Resize**
- Resize by width
- Resize by height
- Resize by both dimensions
- Maintain aspect ratio option
- Quality preservation (High/Medium/Low)

### 4. **Watermark**
- Add text watermarks
- Customizable position (9 positions)
- Adjustable opacity (0-255)
- Custom font size
- Color options (white/black)

### 5. **Compression**
- Manual quality control (1-100)
- Auto-compression to target file size
- Optimize for web

### 6. **Format Conversion**
- JPEG → PNG, WebP, GIF, BMP, TIFF
- PNG → JPEG, WebP, GIF, BMP, TIFF
- WebP → JPEG, PNG, GIF, BMP, TIFF
- Automatic format optimization

### 7. **Enhancements**
- Brightness adjustment
- Contrast enhancement
- Color saturation
- Sharpness control

### 8. **Filters**
- Grayscale
- Sharpen
- Blur
- Smooth
- Edge Enhance
- Emboss
- Contour
- Detail

## 🚀 How to Use

### Access the Editor

#### From Image Detail Page
1. Go to any image detail page
2. Click the **"Edit Image"** button
3. Editor opens with the image loaded

#### Direct URL
```
http://localhost:8000/media/editor/<image_id>/
```

### Editor Interface

The editor has 3 panels:

#### Left Panel - Tools
Quick access buttons for common operations:
- Transform tools (rotate, flip)
- Aspect ratio presets
- Filters

#### Center Panel - Canvas
- Displays the current image
- Shows loading indicator during processing
- Responsive to window size

#### Right Panel - Properties
- Image information
- Detailed controls for:
  - Resize
  - Watermark
  - Format conversion
  - Compression
- Save buttons

### Basic Workflow

1. **Select Operation**: Click a tool or adjust settings
2. **Preview** (optional): Some operations show instant preview
3. **Apply**: Click "Save Changes" or "Save as New"

### Save Options

**Save Changes**
- Overwrites the original image
- Updates the existing database record
- Preserves metadata

**Save as New**
- Creates a new image entry
- Original image remains unchanged
- Copies categories and tags
- Adds "(Edited)" to title

## 📝 Usage Examples

### Example 1: Create Instagram Square

```python
# Via Editor Interface:
1. Open image in editor
2. Click "Square 1:1" aspect ratio button
3. Image is cropped to square
4. Click "Save as New"
```

### Example 2: Add Watermark

```python
# Via Editor Interface:
1. Open image in editor
2. In right panel, enter watermark text: "© 2024 My Company"
3. Select position: "Bottom Right"
4. Adjust opacity: 128
5. Click "Add Watermark"
6. Click "Save Changes"
```

### Example 3: Convert to WebP

```python
# Via Editor Interface:
1. Open image in editor
2. In "Convert Format" section
3. Select "WebP" from dropdown
4. Adjust quality slider: 85
5. Click "Convert"
6. Click "Save as New"
```

### Example 4: Batch Resize

```python
# Via Batch Processing:
1. Go to /media/editor/batch/
2. Select multiple images
3. Choose "Resize" operation
4. Set width: 1920, height: 1080
5. Click "Process All"
```

## 🔧 Python API Usage

### Basic Usage

```python
from media_enhancements.image_editor import ImageEditor

# Load image
editor = ImageEditor('path/to/image.jpg')

# Apply operations
editor.rotate(90).resize(width=1920).add_watermark('© Copyright')

# Save
editor.save('output.jpg', quality=85)
```

### Chaining Operations

```python
editor = ImageEditor(image_file)
editor.crop_to_aspect_ratio('square') \
      .resize(width=1000, height=1000) \
      .enhance_sharpness(1.5) \
      .add_watermark('© 2024', position='bottom-right') \
      .compress(quality=85) \
      .save('output.jpg')
```

### Crop to Aspect Ratio

```python
# Preset ratios
editor.crop_to_aspect_ratio('square')  # 1:1
editor.crop_to_aspect_ratio('landscape')  # 16:9
editor.crop_to_aspect_ratio('portrait')  # 9:16

# Custom ratio
editor.crop_to_aspect_ratio((21, 9))  # Ultrawide

# With position
editor.crop_to_aspect_ratio('square', position='top')
```

### Resize with Quality

```python
# High quality (LANCZOS)
editor.resize(width=1920, height=1080, quality='high')

# Medium quality (BILINEAR)
editor.resize(width=1920, height=1080, quality='medium')

# Fast (NEAREST)
editor.resize(width=1920, height=1080, quality='low')
```

### Add Watermark

```python
editor.add_watermark(
    text='© 2024 Company Name',
    position='bottom-right',  # or 'top-left', 'center', etc.
    opacity=128,  # 0-255
    font_size=36,
    color='white'  # or 'black' or RGB tuple
)
```

### Compress Image

```python
# Manual compression
editor.compress(quality=85)

# Auto-compress to target size
editor.auto_compress(target_size_kb=500)
```

### Convert Format

```python
# Convert to WebP
editor.convert_format('WEBP')
editor.save('output.webp', format='WEBP', quality=85)

# Convert to PNG
editor.convert_format('PNG')
editor.save('output.png', format='PNG')
```

### Apply Filters

```python
editor.apply_filter('sharpen')
editor.apply_filter('blur')
editor.apply_filter('emboss')
editor.grayscale()
```

### Enhancements

```python
editor.enhance_brightness(1.2)  # 20% brighter
editor.enhance_contrast(1.3)    # 30% more contrast
editor.enhance_color(1.1)       # 10% more saturation
editor.enhance_sharpness(1.5)   # 50% sharper
```

### Get Django File

```python
# For saving to Django model
django_file = editor.get_django_file('filename.jpg', format='JPEG', quality=85)

# Save to model
image_instance.file.save('filename.jpg', django_file, save=True)
```

## 🎯 Convenience Functions

### Quick Resize

```python
from media_enhancements.image_editor import quick_resize

resized_file = quick_resize(image_file, width=1920, height=1080, quality=85)
```

### Quick Square Crop

```python
from media_enhancements.image_editor import quick_crop_square

square_file = quick_crop_square(image_file, size=1000)
```

### Quick Watermark

```python
from media_enhancements.image_editor import quick_watermark

watermarked_file = quick_watermark(image_file, text='© Copyright', position='bottom-right')
```

### Quick WebP Conversion

```python
from media_enhancements.image_editor import quick_convert_to_webp

webp_file = quick_convert_to_webp(image_file, quality=85)
```

## 🔌 Integration Examples

### Auto-Watermark on Upload

```python
# In models.py or signals
from django.db.models.signals import post_save
from .image_editor import ImageEditor

@receiver(post_save, sender=CustomImage)
def auto_watermark(sender, instance, created, **kwargs):
    if created:
        editor = ImageEditor(instance.file.path)
        editor.add_watermark('© Company Name', position='bottom-right')
        editor.save(instance.file.path)
```

### Auto-Compression on Upload

```python
@receiver(post_save, sender=CustomImage)
def auto_compress(sender, instance, created, **kwargs):
    if created:
        editor = ImageEditor(instance.file.path)
        editor.auto_compress(target_size_kb=500)
        editor.save(instance.file.path)
```

### Generate Thumbnails

```python
def generate_thumbnails(image_instance):
    editor = ImageEditor(image_instance.file.path)
    
    # Small thumbnail
    editor.resize(width=300, height=300)
    small_file = editor.get_django_file('thumb_small.jpg')
    
    # Medium thumbnail
    editor.resize(width=800, height=800)
    medium_file = editor.get_django_file('thumb_medium.jpg')
    
    return small_file, medium_file
```

## 📊 Supported Formats

### Input Formats
- JPEG / JPG
- PNG
- GIF
- BMP
- TIFF
- WebP
- HEIF / HEIC (with pillow-heif)
- AVIF (with pillow-avif-plugin)

### Output Formats
- JPEG (best for photos)
- PNG (best for graphics with transparency)
- WebP (best for web, smaller file size)
- GIF (for animations)
- BMP (uncompressed)
- TIFF (for printing)

## 🎨 Best Practices

### 1. Quality Settings

**High Quality (85-95)**
- Use for: Final images, print, professional work
- File size: Larger
- Quality: Excellent

**Medium Quality (70-84)**
- Use for: Web images, general use
- File size: Moderate
- Quality: Good

**Low Quality (50-69)**
- Use for: Thumbnails, previews
- File size: Small
- Quality: Acceptable

### 2. Format Selection

**Use JPEG for:**
- Photographs
- Images with many colors
- When file size matters

**Use PNG for:**
- Graphics with transparency
- Screenshots
- Images with text
- When quality is critical

**Use WebP for:**
- Modern web applications
- Best compression with good quality
- Supports transparency

### 3. Watermarking

- Use subtle opacity (100-150) for professional look
- Position in corner to avoid covering important content
- Use contrasting color (white on dark, black on light)
- Keep text short and readable

### 4. Resizing

- Always maintain aspect ratio unless specific dimensions needed
- Use high quality resampling for final images
- Consider target display size
- Don't upscale images (quality loss)

## 🔒 Security Considerations

### File Size Limits

Set in Django settings:
```python
# settings.py
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
```

### Allowed Formats

Restrict in model:
```python
from django.core.validators import FileExtensionValidator

file = models.ImageField(
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
)
```

### User Permissions

Require login:
```python
@login_required
def image_editor_view(request, image_id):
    ...
```

## 🐛 Troubleshooting

### Issue: "Cannot identify image file"

**Solution**: File is corrupted or unsupported format
```python
# Verify file
from PIL import Image
try:
    img = Image.open(file_path)
    img.verify()
except Exception as e:
    print(f"Invalid image: {e}")
```

### Issue: "JPEG requires RGB mode"

**Solution**: Convert RGBA to RGB
```python
if image.mode == 'RGBA':
    rgb_image = Image.new('RGB', image.size, (255, 255, 255))
    rgb_image.paste(image, mask=image.split()[3])
    image = rgb_image
```

### Issue: Watermark not visible

**Solution**: Adjust opacity and color
```python
# Use higher opacity
editor.add_watermark(text='© Copyright', opacity=200, color='white')

# Or use contrasting color
editor.add_watermark(text='© Copyright', opacity=128, color='black')
```

### Issue: Large file sizes after editing

**Solution**: Apply compression
```python
editor.compress(quality=85)
# or
editor.auto_compress(target_size_kb=500)
```

## 📚 Related Documentation

- **UNIFIED_DASHBOARD_GUIDE.md** - Dashboard features
- **RICH_MEDIA_ENHANCEMENTS.md** - Complete features
- **README.md** - Project overview

## 🎉 Benefits

### For Content Editors
- ✅ Edit images without external software
- ✅ Quick aspect ratio adjustments
- ✅ Easy watermarking
- ✅ Format conversion

### For Developers
- ✅ Powerful Python API
- ✅ Chainable operations
- ✅ Django integration
- ✅ Batch processing

### For Site Performance
- ✅ Optimize images for web
- ✅ Convert to modern formats (WebP)
- ✅ Reduce file sizes
- ✅ Faster page loads

---

**Start editing images with professional tools!** 🎨

**Access the editor**: http://localhost:8000/media/editor/<image_id>/
