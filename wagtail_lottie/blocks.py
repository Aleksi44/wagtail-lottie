from django.utils.functional import cached_property
from django.utils.html import format_html
from wagtail.core.blocks import ChooserBlock


class LottieAnimationChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from .models import LottieAnimation
        return LottieAnimation

    @cached_property
    def widget(self):
        from wagtail_lottie.widgets import LottieAnimationChooser
        return LottieAnimationChooser()

    def get_form_state(self, value):
        return self.widget.get_value_data(value)

    def render_basic(self, value, context=None):
        if value:
            lottie_animation_html = '<div ' \
                                    'lottie-animation ' \
                                    'data-name="{0}" ' \
                                    'data-play-mode="{1}" ' \
                                    'data-prefers-color-scheme="{2}" ' \
                                    'data-loop="{3}" ' \
                                    'data-renderer="{4}" ' \
                                    'data-json="{5}" ' \
                                    'data-preserve-aspect-ratio="{6}" ' \
                                    'data-animation-class="{7}" ' \
                                    'class="{8}"' \
                                    '></div>'
            return format_html(
                lottie_animation_html,
                str(value),
                value.play_mode,
                value.prefers_color_scheme,
                value.loop,
                value.renderer,
                value.json_file.url,
                value.preserve_aspect_ratio,
                context.get('animation_class', '') if context else '',
                context.get('container_class', '') if context else ''
            )
        else:
            return ''

    class Meta:
        icon = 'image'
