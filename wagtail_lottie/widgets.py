from django.utils.translation import gettext_lazy as _
from generic_chooser.widgets import AdminChooser
from .models import LottieAnimation


class LottieAnimationChooser(AdminChooser):
    icon = 'image'
    model = LottieAnimation
    page_title = _("Choose an animation")
    choose_modal_url_name = 'lottieanimation_chooser:choose'
