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
                                    'class="{6}"' \
                                    '></div>'
            return format_html(
                lottie_animation_html,
                str(value),
                value.play_mode,
                value.prefers_color_scheme,
                value.loop,
                value.renderer,
                value.json_file.url,
                context.get('class', '') if context else ''
            )
        else:
            return ''

    class Meta:
        icon = 'image'
