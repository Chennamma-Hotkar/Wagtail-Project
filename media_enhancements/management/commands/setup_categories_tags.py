from django.core.management.base import BaseCommand
from media_enhancements.models import Category, PredefinedTag


class Command(BaseCommand):
    help = 'Set up default categories and predefined tags'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up categories and tags...'))
        
        # Create default categories
        categories_data = [
            {
                'name': 'Graphics',
                'slug': 'graphics',
                'description': 'Graphic designs, illustrations, and visual content',
                'category_type': 'graphics',
                'applicable_to': 'image',
                'icon': 'fa-palette',
                'color': '#667eea',
                'order': 1
            },
            {
                'name': 'Photos',
                'slug': 'photos',
                'description': 'Photography and photo content',
                'category_type': 'photos',
                'applicable_to': 'image',
                'icon': 'fa-camera',
                'color': '#f5576c',
                'order': 2
            },
            {
                'name': 'Icons',
                'slug': 'icons',
                'description': 'Icons and small graphics',
                'category_type': 'icons',
                'applicable_to': 'image',
                'icon': 'fa-icons',
                'color': '#4facfe',
                'order': 3
            },
            {
                'name': 'Logos',
                'slug': 'logos',
                'description': 'Brand logos and identity',
                'category_type': 'logos',
                'applicable_to': 'image',
                'icon': 'fa-trademark',
                'color': '#43e97b',
                'order': 4
            },
            {
                'name': 'Banners',
                'slug': 'banners',
                'description': 'Banner images and headers',
                'category_type': 'banners',
                'applicable_to': 'image',
                'icon': 'fa-rectangle-ad',
                'color': '#fa709a',
                'order': 5
            },
            {
                'name': 'Videos',
                'slug': 'videos',
                'description': 'Video content',
                'category_type': 'videos',
                'applicable_to': 'video',
                'icon': 'fa-video',
                'color': '#30cfd0',
                'order': 6
            },
            {
                'name': 'Music',
                'slug': 'music',
                'description': 'Music and songs',
                'category_type': 'music',
                'applicable_to': 'audio',
                'icon': 'fa-music',
                'color': '#a8edea',
                'order': 7
            },
            {
                'name': 'Sound Effects',
                'slug': 'sound-effects',
                'description': 'Sound effects and audio clips',
                'category_type': 'sfx',
                'applicable_to': 'audio',
                'icon': 'fa-volume-up',
                'color': '#fed6e3',
                'order': 8
            },
            {
                'name': 'Documents',
                'slug': 'documents',
                'description': 'PDF and document files',
                'category_type': 'docs',
                'applicable_to': 'document',
                'icon': 'fa-file-alt',
                'color': '#c471f5',
                'order': 9
            },
        ]
        
        cat_count = 0
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                cat_count += 1
                self.stdout.write(f'  ✓ Created category: {category.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {cat_count} categories'))
        
        # Create predefined tags
        tags_data = [
            # Usage Type
            {'name': 'hero-image', 'slug': 'hero-image', 'tag_type': 'usage', 'color': '#667eea', 'icon': 'fa-star', 'order': 1},
            {'name': 'promo-video', 'slug': 'promo-video', 'tag_type': 'usage', 'color': '#f5576c', 'icon': 'fa-video', 'order': 2},
            {'name': 'logo', 'slug': 'logo', 'tag_type': 'usage', 'color': '#4facfe', 'icon': 'fa-trademark', 'order': 3},
            {'name': 'banner', 'slug': 'banner', 'tag_type': 'usage', 'color': '#43e97b', 'icon': 'fa-rectangle-ad', 'order': 4},
            {'name': 'icon', 'slug': 'icon', 'tag_type': 'usage', 'color': '#fa709a', 'icon': 'fa-icons', 'order': 5},
            {'name': 'thumbnail', 'slug': 'thumbnail', 'tag_type': 'usage', 'color': '#30cfd0', 'icon': 'fa-image', 'order': 6},
            
            # Style
            {'name': 'modern', 'slug': 'modern', 'tag_type': 'style', 'color': '#667eea', 'order': 10},
            {'name': 'vintage', 'slug': 'vintage', 'tag_type': 'style', 'color': '#f5576c', 'order': 11},
            {'name': 'minimalist', 'slug': 'minimalist', 'tag_type': 'style', 'color': '#4facfe', 'order': 12},
            {'name': 'colorful', 'slug': 'colorful', 'tag_type': 'style', 'color': '#43e97b', 'order': 13},
            
            # Quality
            {'name': 'high-resolution', 'slug': 'high-resolution', 'tag_type': 'quality', 'color': '#28a745', 'order': 20},
            {'name': 'hd', 'slug': 'hd', 'tag_type': 'quality', 'color': '#28a745', 'order': 21},
            {'name': '4k', 'slug': '4k', 'tag_type': 'quality', 'color': '#28a745', 'order': 22},
            
            # Status
            {'name': 'approved', 'slug': 'approved', 'tag_type': 'status', 'color': '#28a745', 'icon': 'fa-check', 'order': 30},
            {'name': 'draft', 'slug': 'draft', 'tag_type': 'status', 'color': '#ffc107', 'icon': 'fa-pencil', 'order': 31},
            {'name': 'archived', 'slug': 'archived', 'tag_type': 'status', 'color': '#6c757d', 'icon': 'fa-archive', 'order': 32},
            
            # Purpose
            {'name': 'marketing', 'slug': 'marketing', 'tag_type': 'purpose', 'color': '#f5576c', 'order': 40},
            {'name': 'social-media', 'slug': 'social-media', 'tag_type': 'purpose', 'color': '#4facfe', 'order': 41},
            {'name': 'website', 'slug': 'website', 'tag_type': 'purpose', 'color': '#667eea', 'order': 42},
            {'name': 'print', 'slug': 'print', 'tag_type': 'purpose', 'color': '#43e97b', 'order': 43},
        ]
        
        tag_count = 0
        for tag_data in tags_data:
            tag, created = PredefinedTag.objects.get_or_create(
                slug=tag_data['slug'],
                defaults=tag_data
            )
            if created:
                tag_count += 1
                self.stdout.write(f'  ✓ Created tag: {tag.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {tag_count} predefined tags'))
        self.stdout.write(self.style.SUCCESS('\n✅ Setup complete!'))
        self.stdout.write(self.style.SUCCESS('Visit /admin/snippets/ to manage categories and tags'))
