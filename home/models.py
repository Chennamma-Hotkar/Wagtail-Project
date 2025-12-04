from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
     # Add a body field to allow content entry via the Wagtail editor
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    # Max one child page
    max_count = 1 

    # We use a custom template name to keep it explicit
    template = "home/home_page.html"

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

