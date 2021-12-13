from django.utils.translation import gettext_lazy as _
from generic_chooser.views import ModelChooserViewSet

from .models import LottieAnimation


class LottieAnimationChooserViewSet(ModelChooserViewSet):
    model = LottieAnimation
    icon = 'image'
    page_title = _("Choose lottie animation")
    per_page = 50
