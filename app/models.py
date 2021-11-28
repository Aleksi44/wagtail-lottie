from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core import blocks

from wagtail_lottie.models import LottieAnimation
from wagtail_lottie.widgets import LottieAnimationChooser
from wagtail_lottie.blocks import LottieAnimationChooserBlock


class HomePage(Page):
    lottie_animation_foreign_key = models.ForeignKey(
        LottieAnimation, related_name='+',
        null=True, blank=True, on_delete=models.SET_NULL
    )
    lottie_animation_stream_field = StreamField([
        ('lottie_animation_block', LottieAnimationChooserBlock()),
        ('rich_text', blocks.RichTextBlock())
    ], default=None, blank=True)

    content_panels = [
        FieldPanel('lottie_animation_foreign_key', widget=LottieAnimationChooser),
        StreamFieldPanel('lottie_animation_stream_field')
    ]
