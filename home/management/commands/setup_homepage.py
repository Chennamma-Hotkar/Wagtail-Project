from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import HomePage


class Command(BaseCommand):
    help = 'Set up the homepage for the Rich Media Library'

    def handle(self, *args, **options):
        self.stdout.write('Setting up homepage...')
        
        # Get the root page
        root_page = Page.objects.get(id=1)
        
        # Check if HomePage already exists
        if HomePage.objects.exists():
            self.stdout.write(self.style.WARNING('HomePage already exists. Skipping creation.'))
            homepage = HomePage.objects.first()
        else:
            # Create HomePage
            homepage = HomePage(
                title='Rich Media Library',
                slug='home',
                body='<p>Welcome to the Rich Media Library - Your complete media management solution.</p>'
            )
            
            # Add it as a child of root
            root_page.add_child(instance=homepage)
            homepage.save_revision().publish()
            
            self.stdout.write(self.style.SUCCESS('✓ HomePage created'))
        
        # Set up the site to use this homepage
        try:
            site = Site.objects.get(is_default_site=True)
            site.root_page = homepage
            site.save()
            self.stdout.write(self.style.SUCCESS('✓ Site configured to use HomePage'))
        except Site.DoesNotExist:
            # Create a new site
            site = Site.objects.create(
                hostname='localhost',
                port=8000,
                site_name='Rich Media Library',
                root_page=homepage,
                is_default_site=True
            )
            self.stdout.write(self.style.SUCCESS('✓ New site created with HomePage'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Homepage setup complete!'))
        self.stdout.write(self.style.SUCCESS('Visit http://localhost:8000/ to see your beautiful homepage!'))
