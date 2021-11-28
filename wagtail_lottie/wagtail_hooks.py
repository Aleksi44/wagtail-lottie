from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from wagtail.core import hooks
from wagtail.admin.site_summary import SummaryItem
from .views import LottieAnimationChooserViewSet, CreateViewLottieAnimation
from .models import LottieAnimation


class LottieAnimationSummaryItem(SummaryItem):
    order = 410
    template = "wagtail_lottie/homepage/site_summary_lottie_animation.html"

    def get_context(self):
        return {
            "total_lottie_animation": LottieAnimation.objects.count(),
        }


@hooks.register("construct_homepage_summary_items")
def add_lottie_animation_summary_item(request, items):
    items.append(LottieAnimationSummaryItem(request))


@hooks.register('register_admin_viewset')
def register_site_chooser_viewset():
    return LottieAnimationChooserViewSet('lottieanimation_chooser', url_prefix='lottieanimation-chooser')


class LottieAnimationModelAdmin(ModelAdmin):
    model = LottieAnimation
    menu_label = 'Lottie'
    menu_icon = 'image'
    menu_order = 410
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('__str__',)
    search_fields = ('name',)
    create_view_class = CreateViewLottieAnimation
    form_fields_exclude = ['name', 'json_file', 'uuid', 'version', 'width', 'height']


modeladmin_register(LottieAnimationModelAdmin)
