from django.core.management.base import BaseCommand
from media_enhancements.models import Category, PredefinedTag


class Command(BaseCommand):
    help = 'Set up default categories and predefined tags'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up categories and tags...'))
        
        # Create default categories (simplified)
        categories_data = [
            {'name': 'Graphics', 'slug': 'graphics', 'description': 'Graphic designs and illustrations'},
            {'name': 'Photos', 'slug': 'photos', 'description': 'Photography and photo content'},
            {'name': 'Icons', 'slug': 'icons', 'description': 'Icons and small graphics'},
            {'name': 'Logos', 'slug': 'logos', 'description': 'Brand logos and identity'},
            {'name': 'Banners', 'slug': 'banners', 'description': 'Banner images and headers'},
            {'name': 'Videos', 'slug': 'videos', 'description': 'Video content'},
            {'name': 'Audio', 'slug': 'audio', 'description': 'Audio files and music'},
            {'name': 'Documents', 'slug': 'documents', 'description': 'PDF and document files'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'  Category already exists: {category.name}')
        
        # Create predefined tags
        tags_data = [
            {'name': 'hero-image', 'slug': 'hero-image', 'tag_type': 'usage'},
            {'name': 'promo-video', 'slug': 'promo-video', 'tag_type': 'usage'},
            {'name': 'logo', 'slug': 'logo', 'tag_type': 'usage'},
            {'name': 'banner', 'slug': 'banner', 'tag_type': 'usage'},
            {'name': 'icon', 'slug': 'icon', 'tag_type': 'usage'},
            {'name': 'thumbnail', 'slug': 'thumbnail', 'tag_type': 'usage'},
            {'name': 'modern', 'slug': 'modern', 'tag_type': 'style'},
            {'name': 'vintage', 'slug': 'vintage', 'tag_type': 'status'},
            {'name': 'minimalist', 'slug': 'minimalist', 'tag_type': 'style'},
            {'name': 'colorful', 'slug': 'colorful', 'tag_type': 'style'},
            {'name': 'high-resolution', 'slug': 'high-resolution', 'tag_type': 'technical'},
            {'name': 'hd', 'slug': 'hd', 'tag_type': 'technical'},
            {'name': '4k', 'slug': '4k', 'tag_type': 'technical'},
            {'name': 'approved', 'slug': 'approved', 'tag_type': 'status'},
            {'name': 'draft', 'slug': 'draft', 'tag_type': 'status'},
            {'name': 'archived', 'slug': 'archived', 'tag_type': 'status'},
        ]
        
        for tag_data in tags_data:
            tag, created = PredefinedTag.objects.get_or_create(
                slug=tag_data['slug'],
                defaults=tag_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created tag: {tag.name}'))
            else:
                self.stdout.write(f'  Tag already exists: {tag.name}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Categories and tags setup complete!'))
