from django.core.management.base import BaseCommand
from django.utils import timezone
from media_enhancements.models import CustomDocument


class Command(BaseCommand):
    help = 'Clean up expired documents from the media library'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        today = timezone.now().date()
        expired_docs = CustomDocument.objects.filter(
            expiry_date__lt=today
        )
        
        count = expired_docs.count()
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would delete {count} expired documents')
            )
            for doc in expired_docs:
                self.stdout.write(f'  - {doc.title} (expired: {doc.expiry_date})')
        else:
            if count > 0:
                for doc in expired_docs:
                    self.stdout.write(f'Deleting: {doc.title}')
                    doc.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully deleted {count} expired documents')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('No expired documents found')
                )
