"""
Advanced Image Editing Tools
Provides crop, rotate, flip, resize, watermark, compression, and format conversion
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from io import BytesIO
from django.core.files.base import ContentFile
import os


class ImageEditor:
    """
    Advanced image editing toolkit using Pillow.
    """
    
    # Preset aspect ratios
    ASPECT_RATIOS = {
        'square': (1, 1),
        'instagram': (1, 1),
        'landscape': (16, 9),
        'portrait': (9, 16),
        'widescreen': (21, 9),
        'standard': (4, 3),
        'classic': (3, 2),
        'facebook_cover': (820, 312),
        'twitter_header': (1500, 500),
        'youtube_thumbnail': (1280, 720),
    }
    
    # Supported formats
    SUPPORTED_FORMATS = ['JPEG', 'PNG', 'WEBP', 'GIF', 'BMP', 'TIFF']
    
    def __init__(self, image_path_or_file):
        """
        Initialize with image path or file object.
        """
        if isinstance(image_path_or_file, str):
            self.image = Image.open(image_path_or_file)
        else:
            self.image = Image.open(image_path_or_file)
        
        # Convert RGBA to RGB if needed for JPEG
        if self.image.mode == 'RGBA':
            self.original_mode = 'RGBA'
        else:
            self.original_mode = self.image.mode
    
    def crop(self, left, top, right, bottom):
        """
        Crop image to specified coordinates.
        
        Args:
            left, top, right, bottom: Crop box coordinates
        """
        self.image = self.image.crop((left, top, right, bottom))
        return self
    
    def crop_to_aspect_ratio(self, aspect_ratio='square', position='center'):
        """
        Crop image to a preset aspect ratio.
        
        Args:
            aspect_ratio: Key from ASPECT_RATIOS or tuple (width, height)
            position: 'center', 'top', 'bottom', 'left', 'right'
        """
        if isinstance(aspect_ratio, str):
            if aspect_ratio not in self.ASPECT_RATIOS:
                raise ValueError(f"Unknown aspect ratio: {aspect_ratio}")
            target_ratio = self.ASPECT_RATIOS[aspect_ratio]
        else:
            target_ratio = aspect_ratio
        
        width, height = self.image.size
        current_ratio = width / height
        target_ratio_value = target_ratio[0] / target_ratio[1]
        
        if current_ratio > target_ratio_value:
            # Image is wider, crop width
            new_width = int(height * target_ratio_value)
            new_height = height
            
            if position == 'left':
                left = 0
            elif position == 'right':
                left = width - new_width
            else:  # center
                left = (width - new_width) // 2
            
            top = 0
            right = left + new_width
            bottom = height
        else:
            # Image is taller, crop height
            new_width = width
            new_height = int(width / target_ratio_value)
            
            if position == 'top':
                top = 0
            elif position == 'bottom':
                top = height - new_height
            else:  # center
                top = (height - new_height) // 2
            
            left = 0
            right = width
            bottom = top + new_height
        
        self.image = self.image.crop((left, top, right, bottom))
        return self
    
    def rotate(self, degrees, expand=True):
        """
        Rotate image by specified degrees.
        
        Args:
            degrees: Rotation angle (positive = counter-clockwise)
            expand: If True, expand image to fit rotated content
        """
        self.image = self.image.rotate(degrees, expand=expand, fillcolor='white')
        return self
    
    def flip_horizontal(self):
        """Flip image horizontally (mirror)."""
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        return self
    
    def flip_vertical(self):
        """Flip image vertically."""
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        return self
    
    def resize(self, width=None, height=None, maintain_aspect=True, quality='high'):
        """
        Resize image with quality preservation.
        
        Args:
            width: Target width (None to calculate from height)
            height: Target height (None to calculate from width)
            maintain_aspect: Keep aspect ratio
            quality: 'high', 'medium', 'low' (affects resampling filter)
        """
        if width is None and height is None:
            raise ValueError("Must specify at least width or height")
        
        current_width, current_height = self.image.size
        
        if maintain_aspect:
            if width and height:
                # Calculate which dimension to use
                width_ratio = width / current_width
                height_ratio = height / current_height
                ratio = min(width_ratio, height_ratio)
                new_width = int(current_width * ratio)
                new_height = int(current_height * ratio)
            elif width:
                ratio = width / current_width
                new_width = width
                new_height = int(current_height * ratio)
            else:  # height only
                ratio = height / current_height
                new_width = int(current_width * ratio)
                new_height = height
        else:
            new_width = width or current_width
            new_height = height or current_height
        
        # Choose resampling filter based on quality
        if quality == 'high':
            resample = Image.LANCZOS
        elif quality == 'medium':
            resample = Image.BILINEAR
        else:
            resample = Image.NEAREST
        
        self.image = self.image.resize((new_width, new_height), resample)
        return self
    
    def add_watermark(self, text, position='bottom-right', opacity=128, 
                     font_size=36, color='white'):
        """
        Add text watermark to image.
        
        Args:
            text: Watermark text
            position: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
            opacity: 0-255 (0=transparent, 255=opaque)
            font_size: Font size in pixels
            color: Text color
        """
        # Create a transparent overlay
        overlay = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        width, height = self.image.size
        margin = 20
        
        if position == 'top-left':
            x, y = margin, margin
        elif position == 'top-right':
            x, y = width - text_width - margin, margin
        elif position == 'bottom-left':
            x, y = margin, height - text_height - margin
        elif position == 'bottom-right':
            x, y = width - text_width - margin, height - text_height - margin
        else:  # center
            x, y = (width - text_width) // 2, (height - text_height) // 2
        
        # Convert color to RGBA
        if isinstance(color, str):
            if color == 'white':
                rgba_color = (255, 255, 255, opacity)
            elif color == 'black':
                rgba_color = (0, 0, 0, opacity)
            else:
                rgba_color = (255, 255, 255, opacity)
        else:
            rgba_color = (*color, opacity)
        
        # Draw text
        draw.text((x, y), text, font=font, fill=rgba_color)
        
        # Composite with original image
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')
        
        self.image = Image.alpha_composite(self.image, overlay)
        return self
    
    def compress(self, quality=85):
        """
        Compress image (mainly for JPEG).
        
        Args:
            quality: 1-100 (higher = better quality, larger file)
        """
        self.compression_quality = quality
        return self
    
    def auto_compress(self, target_size_kb=500):
        """
        Automatically compress to target file size.
        
        Args:
            target_size_kb: Target file size in kilobytes
        """
        quality = 95
        while quality > 10:
            output = BytesIO()
            self.save_to_buffer(output, format='JPEG', quality=quality)
            size_kb = len(output.getvalue()) / 1024
            
            if size_kb <= target_size_kb:
                break
            
            quality -= 5
        
        self.compression_quality = quality
        return self
    
    def convert_format(self, format='WEBP'):
        """
        Convert image to different format.
        
        Args:
            format: Target format (JPEG, PNG, WEBP, etc.)
        """
        format = format.upper()
        if format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}")
        
        self.target_format = format
        
        # Convert RGBA to RGB for JPEG
        if format == 'JPEG' and self.image.mode == 'RGBA':
            rgb_image = Image.new('RGB', self.image.size, (255, 255, 255))
            rgb_image.paste(self.image, mask=self.image.split()[3])
            self.image = rgb_image
        
        return self
    
    def enhance_brightness(self, factor=1.2):
        """Enhance image brightness (1.0 = original)."""
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def enhance_contrast(self, factor=1.2):
        """Enhance image contrast (1.0 = original)."""
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def enhance_color(self, factor=1.2):
        """Enhance image color saturation (1.0 = original)."""
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def enhance_sharpness(self, factor=1.5):
        """Enhance image sharpness (1.0 = original)."""
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def apply_filter(self, filter_name='sharpen'):
        """
        Apply image filter.
        
        Args:
            filter_name: 'blur', 'sharpen', 'smooth', 'edge_enhance', 'emboss'
        """
        filters = {
            'blur': ImageFilter.BLUR,
            'sharpen': ImageFilter.SHARPEN,
            'smooth': ImageFilter.SMOOTH,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'emboss': ImageFilter.EMBOSS,
            'contour': ImageFilter.CONTOUR,
            'detail': ImageFilter.DETAIL,
        }
        
        if filter_name in filters:
            self.image = self.image.filter(filters[filter_name])
        
        return self
    
    def grayscale(self):
        """Convert image to grayscale."""
        self.image = self.image.convert('L').convert('RGB')
        return self
    
    def save(self, output_path, format=None, quality=85):
        """
        Save edited image to file.
        
        Args:
            output_path: Output file path
            format: Image format (auto-detected from extension if None)
            quality: JPEG quality (1-100)
        """
        if format is None:
            format = os.path.splitext(output_path)[1][1:].upper()
        
        # Ensure RGB mode for JPEG
        if format == 'JPEG' and self.image.mode not in ('RGB', 'L'):
            self.image = self.image.convert('RGB')
        
        save_kwargs = {}
        if format in ('JPEG', 'WEBP'):
            save_kwargs['quality'] = getattr(self, 'compression_quality', quality)
            save_kwargs['optimize'] = True
        
        self.image.save(output_path, format=format, **save_kwargs)
        return output_path
    
    def save_to_buffer(self, buffer, format='JPEG', quality=85):
        """
        Save edited image to BytesIO buffer.
        
        Args:
            buffer: BytesIO object
            format: Image format
            quality: JPEG quality (1-100)
        """
        # Ensure RGB mode for JPEG
        if format == 'JPEG' and self.image.mode not in ('RGB', 'L'):
            self.image = self.image.convert('RGB')
        
        save_kwargs = {}
        if format in ('JPEG', 'WEBP'):
            save_kwargs['quality'] = getattr(self, 'compression_quality', quality)
            save_kwargs['optimize'] = True
        
        self.image.save(buffer, format=format, **save_kwargs)
        buffer.seek(0)
        return buffer
    
    def get_django_file(self, filename, format='JPEG', quality=85):
        """
        Get Django ContentFile for saving to model.
        
        Args:
            filename: Output filename
            format: Image format
            quality: JPEG quality
        
        Returns:
            ContentFile object
        """
        buffer = BytesIO()
        self.save_to_buffer(buffer, format=format, quality=quality)
        return ContentFile(buffer.getvalue(), name=filename)
    
    def get_image(self):
        """Get the PIL Image object."""
        return self.image
    
    def get_size(self):
        """Get image dimensions."""
        return self.image.size
    
    def get_info(self):
        """Get image information."""
        return {
            'size': self.image.size,
            'mode': self.image.mode,
            'format': self.image.format,
            'width': self.image.width,
            'height': self.image.height,
        }


# Convenience functions

def quick_resize(image_file, width=None, height=None, quality=85):
    """Quick resize function."""
    editor = ImageEditor(image_file)
    editor.resize(width=width, height=height)
    return editor.get_django_file(f'resized_{image_file.name}', quality=quality)


def quick_crop_square(image_file, size=1000):
    """Quick square crop function."""
    editor = ImageEditor(image_file)
    editor.crop_to_aspect_ratio('square').resize(width=size, height=size)
    return editor.get_django_file(f'square_{image_file.name}')


def quick_watermark(image_file, text, position='bottom-right'):
    """Quick watermark function."""
    editor = ImageEditor(image_file)
    editor.add_watermark(text, position=position)
    return editor.get_django_file(f'watermarked_{image_file.name}')


def quick_convert_to_webp(image_file, quality=85):
    """Quick WebP conversion."""
    editor = ImageEditor(image_file)
    editor.convert_format('WEBP')
    filename = os.path.splitext(image_file.name)[0] + '.webp'
    return editor.get_django_file(filename, format='WEBP', quality=quality)
