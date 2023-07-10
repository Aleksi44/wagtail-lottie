from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail import blocks

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
    ], default=None, blank=True, use_json_field=True)

    content_panels = [
        FieldPanel('lottie_animation_foreign_key', widget=LottieAnimationChooser),
        FieldPanel('lottie_animation_stream_field')
    ]
