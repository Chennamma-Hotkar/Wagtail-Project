from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import CustomImage, CustomDocument, Category


@login_required
def media_gallery(request):
    """
    Display a gallery view of all media (images and documents).
    """
    images = CustomImage.objects.all().order_by('-created_at')
    documents = CustomDocument.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        images = images.filter(categories__slug=category_slug)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        images = images.filter(
            Q(title__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Pagination
    image_paginator = Paginator(images, 12)
    doc_paginator = Paginator(documents, 12)
    
    image_page = request.GET.get('image_page', 1)
    doc_page = request.GET.get('doc_page', 1)
    
    images_page_obj = image_paginator.get_page(image_page)
    docs_page_obj = doc_paginator.get_page(doc_page)
    
    context = {
        'images': images_page_obj,
        'documents': docs_page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    
    return render(request, 'media_enhancements/gallery.html', context)


@login_required
def image_detail(request, image_id):
    """
    Display detailed information about a specific image.
    """
    image = get_object_or_404(CustomImage, id=image_id)
    
    context = {
        'image': image,
        'categories': image.categories.all(),
        'tags': image.tags.all(),
    }
    
    return render(request, 'media_enhancements/image_detail.html', context)


@login_required
def document_detail(request, document_id):
    """
    Display detailed information about a specific document.
    """
    document = get_object_or_404(CustomDocument, id=document_id)
    
    context = {
        'document': document,
        'tags': document.tags.all(),
    }
    
    return render(request, 'media_enhancements/document_detail.html', context)


@login_required
@require_http_methods(["GET"])
def media_stats_api(request):
    """
    API endpoint to get media statistics.
    """
    stats = {
        'total_images': CustomImage.objects.count(),
        'total_documents': CustomDocument.objects.count(),
        'total_categories': Category.objects.count(),
        'images_by_category': list(
            Category.objects.annotate(
                image_count=Count('customimage')
            ).values('name', 'image_count')
        ),
        'recent_uploads': {
            'images': list(
                CustomImage.objects.order_by('-created_at')[:5].values(
                    'id', 'title', 'created_at'
                )
            ),
            'documents': list(
                CustomDocument.objects.order_by('-created_at')[:5].values(
                    'id', 'title', 'created_at'
                )
            ),
        }
    }
    
    return JsonResponse(stats)


@login_required
def category_media(request, category_slug):
    """
    Display all media items for a specific category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    images = CustomImage.objects.filter(categories=category).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(images, 12)
    page = request.GET.get('page', 1)
    images_page_obj = paginator.get_page(page)
    
    context = {
        'category': category,
        'images': images_page_obj,
    }
    
    return render(request, 'media_enhancements/category_media.html', context)
