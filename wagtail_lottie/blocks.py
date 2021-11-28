from django.utils.functional import cached_property
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

    class Meta:
        icon = 'image'
        template = 'wagtail_lottie/lottie_animation.html'
