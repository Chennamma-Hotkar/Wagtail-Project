"""
Views for Image Editor functionality
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import CustomImage
from .image_editor import ImageEditor
from io import BytesIO
import json


@login_required
def image_editor_view(request, image_id):
    """
    Main image editor interface.
    """
    image = get_object_or_404(CustomImage, id=image_id)
    
    context = {
        'image': image,
        'aspect_ratios': ImageEditor.ASPECT_RATIOS,
        'supported_formats': ImageEditor.SUPPORTED_FORMATS,
    }
    
    return render(request, 'media_enhancements/image_editor.html', context)


@login_required
@require_http_methods(["POST"])
def apply_edit(request, image_id):
    """
    Apply editing operations to an image.
    """
    image = get_object_or_404(CustomImage, id=image_id)
    
    try:
        # Get edit parameters
        data = json.loads(request.body)
        operation = data.get('operation')
        params = data.get('params', {})
        save_as_new = data.get('save_as_new', False)
        
        # Create editor instance
        editor = ImageEditor(image.file.path)
        
        # Apply operation
        if operation == 'crop':
            editor.crop(
                params['left'],
                params['top'],
                params['right'],
                params['bottom']
            )
        
        elif operation == 'crop_aspect':
            editor.crop_to_aspect_ratio(
                params.get('aspect_ratio', 'square'),
                params.get('position', 'center')
            )
        
        elif operation == 'rotate':
            editor.rotate(params.get('degrees', 90))
        
        elif operation == 'flip_horizontal':
            editor.flip_horizontal()
        
        elif operation == 'flip_vertical':
            editor.flip_vertical()
        
        elif operation == 'resize':
            editor.resize(
                width=params.get('width'),
                height=params.get('height'),
                maintain_aspect=params.get('maintain_aspect', True),
                quality=params.get('quality', 'high')
            )
        
        elif operation == 'watermark':
            editor.add_watermark(
                text=params.get('text', '© Copyright'),
                position=params.get('position', 'bottom-right'),
                opacity=params.get('opacity', 128),
                font_size=params.get('font_size', 36),
                color=params.get('color', 'white')
            )
        
        elif operation == 'compress':
            editor.compress(quality=params.get('quality', 85))
        
        elif operation == 'convert_format':
            editor.convert_format(params.get('format', 'WEBP'))
        
        elif operation == 'enhance_brightness':
            editor.enhance_brightness(params.get('factor', 1.2))
        
        elif operation == 'enhance_contrast':
            editor.enhance_contrast(params.get('factor', 1.2))
        
        elif operation == 'enhance_color':
            editor.enhance_color(params.get('factor', 1.2))
        
        elif operation == 'enhance_sharpness':
            editor.enhance_sharpness(params.get('factor', 1.5))
        
        elif operation == 'apply_filter':
            editor.apply_filter(params.get('filter_name', 'sharpen'))
        
        elif operation == 'grayscale':
            editor.grayscale()
        
        else:
            return JsonResponse({'error': 'Unknown operation'}, status=400)
        
        # Save the edited image
        if save_as_new:
            # Create new image instance
            new_image = CustomImage(
                title=f"{image.title} (Edited)",
                collection=image.collection,
                copyright_holder=image.copyright_holder,
                source_url=image.source_url,
                alt_text_override=image.alt_text_override,
            )
            
            # Save file
            format_ext = params.get('format', 'JPEG').lower()
            if format_ext == 'jpeg':
                format_ext = 'jpg'
            
            filename = f"edited_{image.file.name.split('/')[-1]}"
            filename = filename.rsplit('.', 1)[0] + f'.{format_ext}'
            
            django_file = editor.get_django_file(filename, format=params.get('format', 'JPEG'))
            new_image.file.save(filename, django_file, save=True)
            
            # Copy categories and tags
            new_image.categories.set(image.categories.all())
            for tag in image.tags.all():
                new_image.tags.add(tag)
            
            return JsonResponse({
                'success': True,
                'message': 'New edited image created',
                'image_id': new_image.id,
                'redirect_url': f'/media/image/{new_image.id}/'
            })
        else:
            # Update existing image
            filename = image.file.name.split('/')[-1]
            django_file = editor.get_django_file(filename)
            image.file.save(filename, django_file, save=True)
            
            return JsonResponse({
                'success': True,
                'message': 'Image updated successfully',
                'image_id': image.id
            })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def preview_edit(request, image_id):
    """
    Preview editing operation without saving.
    """
    image = get_object_or_404(CustomImage, id=image_id)
    
    try:
        # Get edit parameters from query string
        operation = request.GET.get('operation')
        
        # Create editor instance
        editor = ImageEditor(image.file.path)
        
        # Apply operation based on query parameters
        if operation == 'rotate':
            degrees = int(request.GET.get('degrees', 90))
            editor.rotate(degrees)
        
        elif operation == 'flip_horizontal':
            editor.flip_horizontal()
        
        elif operation == 'flip_vertical':
            editor.flip_vertical()
        
        elif operation == 'grayscale':
            editor.grayscale()
        
        elif operation == 'enhance_brightness':
            factor = float(request.GET.get('factor', 1.2))
            editor.enhance_brightness(factor)
        
        # Return image as HTTP response
        buffer = BytesIO()
        editor.save_to_buffer(buffer, format='JPEG', quality=85)
        
        return HttpResponse(buffer.getvalue(), content_type='image/jpeg')
    
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


@login_required
def batch_process(request):
    """
    Batch process multiple images.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_ids = data.get('image_ids', [])
            operation = data.get('operation')
            params = data.get('params', {})
            
            results = []
            
            for image_id in image_ids:
                try:
                    image = CustomImage.objects.get(id=image_id)
                    editor = ImageEditor(image.file.path)
                    
                    # Apply operation
                    if operation == 'resize':
                        editor.resize(
                            width=params.get('width'),
                            height=params.get('height')
                        )
                    elif operation == 'watermark':
                        editor.add_watermark(
                            text=params.get('text', '© Copyright'),
                            position=params.get('position', 'bottom-right')
                        )
                    elif operation == 'convert_format':
                        editor.convert_format(params.get('format', 'WEBP'))
                    elif operation == 'compress':
                        editor.compress(quality=params.get('quality', 85))
                    
                    # Save
                    filename = image.file.name.split('/')[-1]
                    django_file = editor.get_django_file(filename)
                    image.file.save(filename, django_file, save=True)
                    
                    results.append({
                        'image_id': image_id,
                        'success': True
                    })
                
                except Exception as e:
                    results.append({
                        'image_id': image_id,
                        'success': False,
                        'error': str(e)
                    })
            
            return JsonResponse({
                'success': True,
                'results': results
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET request - show batch processing interface
    images = CustomImage.objects.all()[:50]  # Limit for performance
    
    context = {
        'images': images,
    }
    
    return render(request, 'media_enhancements/batch_process.html', context)
