import os
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from zipfile import BadZipFile, LargeZipFile
from django.core.files.base import ContentFile

from .lottie_zip_file import LottieZipFile
from .exceptions import WagtailLottieException
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
    PRESERVE_ASPECT_RATIO_DEFAULT = "xMidYMid meet"
    PRESERVE_ASPECT_RATIO_CHOICES = (
        (PRESERVE_ASPECT_RATIO_DEFAULT, "xMidYMid meet"),
        ("none", "None"),
        ("xMinYMin meet", "xMinYMin meet"),
        ("xMidYMin meet", "xMidYMin meet"),
        ("xMaxYMin meet", "xMaxYMin meet"),
        ("xMinYMid meet", "xMinYMid meet"),
        ("xMaxYMid meet", "xMaxYMid meet"),
        ("xMinYMax meet", "xMinYMax meet"),
        ("xMidYMax meet", "xMidYMax meet"),
        ("xMaxYMax meet", "xMaxYMax meet"),
        ("xMinYMin slice", "xMinYMin slice"),
        ("xMidYMin slice", "xMidYMin slice"),
        ("xMaxYMin slice", "xMaxYMin slice"),
        ("xMinYMid slice", "xMinYMid slice"),
        ("xMidYMid slice", "xMidYMid slice"),
        ("xMaxYMid slice", "xMaxYMid slice"),
        ("xMinYMax slice", "xMinYMax slice"),
        ("xMidYMax slice", "xMidYMax slice"),
        ("xMaxYMax slice", "xMaxYMax slice"),
    )
    title = models.CharField(default=None, null=True, max_length=100)
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
    preserve_aspect_ratio = models.CharField(
        choices=PRESERVE_ASPECT_RATIO_CHOICES,
        max_length=20,
        default=PRESERVE_ASPECT_RATIO_DEFAULT
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

    __original_zip_file = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_zip_file = self.zip_file

    def __str__(self):
        object_str = ""
        if self.title:
            object_str += self.title.title()
        if self.play_mode and self.prefers_color_scheme and self.renderer:
            object_str += " (%s %s %s %s %s)" % (
                self.name,
                self.play_mode,
                self.prefers_color_scheme,
                self.renderer,
                self.id
            )
        if object_str:
            return object_str
        return super().__str__()

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        zip_file_changed = self.zip_file != self.__original_zip_file
        lottie_zip_file = None

        if zip_file_changed:
            try:
                lottie_zip_file = LottieZipFile(self.zip_file)
            except (WagtailLottieException, BadZipFile, LargeZipFile) as err:
                raise ValidationError(str(err))
            self.uuid = lottie_zip_file.uuid
            self.name = lottie_zip_file.name
            self.width = lottie_zip_file.width
            self.height = lottie_zip_file.height
            self.version = lottie_zip_file.version
            self.json_file = ContentFile(
                lottie_zip_file.read(lottie_zip_file.json_path),
                name=os.path.join(self.uuid, 'body.json')
            )
        super().save(force_insert, force_update, *args, **kwargs)
        if zip_file_changed and lottie_zip_file:
            self.lottieanimationimage_set.all().delete()
            for image in lottie_zip_file.images_path:
                lottie_animation = LottieAnimationImage.objects.create(animation_id=self.id)
                lottie_animation.image = ContentFile(
                    lottie_zip_file.read(image),
                    name=os.path.join(self.uuid, "images", lottie_zip_file.extract_filename(image))
                )
                lottie_animation.save()
        self.__original_name = self.zip_file

    class Meta:
        ordering = ['-id']


class LottieAnimationImage(models.Model):
    animation = models.ForeignKey(LottieAnimation, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        upload_to=constants.WAGTAIL_LOTTIE_UPLOAD_FOLDER,
        verbose_name=_("Image file"),
        default=None,
        null=True
    )
