from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from media_enhancements.models import CustomImage, CustomDocument, Category
from PIL import Image
import io


class Command(BaseCommand):
    help = 'Generate sample media for testing the Rich Media Library'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Generating sample media...'))
        
        # Create sample categories
        categories_data = [
            {'name': 'Nature', 'slug': 'nature', 'description': 'Beautiful nature photography'},
            {'name': 'Technology', 'slug': 'technology', 'description': 'Tech-related images'},
            {'name': 'Business', 'slug': 'business', 'description': 'Business and corporate images'},
            {'name': 'Education', 'slug': 'education', 'description': 'Educational content'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        
        # Generate sample images
        colors = [
            ('Red', (255, 0, 0)),
            ('Green', (0, 255, 0)),
            ('Blue', (0, 0, 255)),
            ('Yellow', (255, 255, 0)),
            ('Purple', (128, 0, 128)),
        ]
        
        for i, (color_name, color_rgb) in enumerate(colors):
            # Create a simple colored image
            img = Image.new('RGB', (800, 600), color=color_rgb)
            img_io = io.BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)
            
            # Create CustomImage instance
            custom_image = CustomImage(
                title=f'Sample {color_name} Image',
                copyright_holder='Sample Copyright Holder',
                source_url='https://example.com',
                alt_text_override=f'A {color_name.lower()} colored sample image'
            )
            custom_image.file.save(
                f'sample_{color_name.lower()}.png',
                ContentFile(img_io.read()),
                save=True
            )
            
            # Add categories
            custom_image.categories.add(categories[i % len(categories)])
            
            # Add tags
            custom_image.tags.add(color_name.lower(), 'sample', 'test')
            
            self.stdout.write(self.style.SUCCESS(f'Created image: {custom_image.title}'))
        
        self.stdout.write(self.style.SUCCESS('Sample media generation complete!'))
