"""
Management command to create sample folder structure
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from media_enhancements.models import MediaFolder


class Command(BaseCommand):
    help = 'Creates sample folder structure for media organization'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample folder structure...')
        
        # Create root folders
        banners_folder, created = MediaFolder.objects.get_or_create(
            slug='banners',
            defaults={
                'name': 'Banners',
                'description': 'Marketing banners and promotional images',
                'icon': 'fa-flag',
                'color': '#f5576c',
                'order': 1,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {banners_folder.name}'))
        
        products_folder, created = MediaFolder.objects.get_or_create(
            slug='products',
            defaults={
                'name': 'Products',
                'description': 'Product images and media',
                'icon': 'fa-box',
                'color': '#4facfe',
                'order': 2,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {products_folder.name}'))
        
        campaigns_folder, created = MediaFolder.objects.get_or_create(
            slug='campaigns',
            defaults={
                'name': 'Campaigns',
                'description': 'Marketing campaign assets',
                'icon': 'fa-bullhorn',
                'color': '#43e97b',
                'order': 3,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {campaigns_folder.name}'))
        
        # Create subfolder: Campaigns > 2024 Launch
        launch_2024_folder, created = MediaFolder.objects.get_or_create(
            slug='2024-launch',
            parent=campaigns_folder,
            defaults={
                'name': '2024 Launch',
                'description': 'Assets for 2024 product launch campaign',
                'icon': 'fa-rocket',
                'color': '#667eea',
                'order': 1,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created subfolder: {launch_2024_folder.get_full_path()}'))
        
        # Create more useful folders
        social_media_folder, created = MediaFolder.objects.get_or_create(
            slug='social-media',
            defaults={
                'name': 'Social Media',
                'description': 'Social media posts and graphics',
                'icon': 'fa-share-alt',
                'color': '#764ba2',
                'order': 4,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {social_media_folder.name}'))
        
        logos_folder, created = MediaFolder.objects.get_or_create(
            slug='logos',
            defaults={
                'name': 'Logos',
                'description': 'Company and brand logos',
                'icon': 'fa-copyright',
                'color': '#f093fb',
                'order': 5,
                'is_system_folder': True,  # Protect from deletion
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {logos_folder.name}'))
        
        videos_folder, created = MediaFolder.objects.get_or_create(
            slug='videos',
            defaults={
                'name': 'Videos',
                'description': 'Video content and recordings',
                'icon': 'fa-video',
                'color': '#4facfe',
                'order': 6,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {videos_folder.name}'))
        
        audio_folder, created = MediaFolder.objects.get_or_create(
            slug='audio',
            defaults={
                'name': 'Audio',
                'description': 'Audio files and music',
                'icon': 'fa-music',
                'color': '#43e97b',
                'order': 7,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {audio_folder.name}'))
        
        documents_folder, created = MediaFolder.objects.get_or_create(
            slug='documents',
            defaults={
                'name': 'Documents',
                'description': 'PDFs and other documents',
                'icon': 'fa-file-alt',
                'color': '#f5576c',
                'order': 8,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created folder: {documents_folder.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Folder structure created successfully!'))
        self.stdout.write('\nFolder hierarchy:')
        self.stdout.write('├── Banners')
        self.stdout.write('├── Products')
        self.stdout.write('├── Campaigns')
        self.stdout.write('│   └── 2024 Launch')
        self.stdout.write('├── Social Media')
        self.stdout.write('├── Logos')
        self.stdout.write('├── Videos')
        self.stdout.write('├── Audio')
        self.stdout.write('└── Documents')
