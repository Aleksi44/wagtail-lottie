from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import FileExtensionValidator

from . import constants


class LottieAnimation(models.Model):
    PLAY_MODE_AUTO = 'play_auto'
    PLAY_MODE_INTER = 'play_intersection'
    PLAY_MODE_MANUALLY = 'play_manual'
    PLAY_MODE_CHOICES = (
        (PLAY_MODE_AUTO, _('Start playing as soon as it is ready')),
        (PLAY_MODE_INTER, _('Start playing at intersection')),
        (PLAY_MODE_MANUALLY, _('Start playing when play() is called')),
    )
    RENDERER_SVG = 'svg'
    RENDERER_CANVAS = 'canvas'
    RENDERER_HTML = 'html'
    RENDERER_CHOICES = (
        (RENDERER_SVG, 'Svg'),
        (RENDERER_CANVAS, 'Canvas'),
        (RENDERER_HTML, 'Html')
    )
    PREFERS_COLOR_SCHEME_NONE = 'no_scheme'
    PREFERS_COLOR_SCHEME_LIGHT = 'scheme_light'
    PREFERS_COLOR_SCHEME_DARK = 'scheme_dark'
    PREFERS_COLOR_SCHEME_CHOICES = (
        (PREFERS_COLOR_SCHEME_NONE, _('No preference')),
        (PREFERS_COLOR_SCHEME_LIGHT, _('Light')),
        (PREFERS_COLOR_SCHEME_DARK, _('Dark')),
    )
    zip_file = models.FileField(
        upload_to=constants.WAGTAIL_LOTTIE_UPLOAD_FOLDER_TMP,
        verbose_name=_("ZIP file"),
        default=None,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['zip'])]
    )
    play_mode = models.CharField(choices=PLAY_MODE_CHOICES, max_length=20, default=PLAY_MODE_AUTO)
    loop = models.BooleanField(default=True)
    renderer = models.CharField(choices=RENDERER_CHOICES, max_length=20, default=RENDERER_SVG)
    prefers_color_scheme = models.CharField(
        choices=PREFERS_COLOR_SCHEME_CHOICES,
        max_length=20,
        default=PREFERS_COLOR_SCHEME_NONE
    )

    created = models.DateTimeField(auto_now_add=True, null=True)
    uuid = models.CharField(default=None, null=True, max_length=32)
    name = models.CharField(default=None, null=True, max_length=100)
    version = models.CharField(default=None, null=True, max_length=20)
    width = models.PositiveIntegerField(default=None, null=True)
    height = models.PositiveIntegerField(default=None, null=True)
    json_file = models.FileField(
        upload_to=constants.WAGTAIL_LOTTIE_UPLOAD_FOLDER,
        verbose_name=_("Json file"),
        default=None,
        null=True
    )

    def __str__(self):
        if self.name and self.play_mode and self.prefers_color_scheme and self.renderer:
            return "%s %s %s %s %s" % (
                self.name,
                self.play_mode,
                self.prefers_color_scheme,
                self.renderer,
                self.id
            )
        return super().__str__()


class LottieAnimationImage(models.Model):
    animation = models.ForeignKey(LottieAnimation, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        upload_to=constants.WAGTAIL_LOTTIE_UPLOAD_FOLDER,
        verbose_name=_("Image file"),
        default=None,
        null=True
    )
