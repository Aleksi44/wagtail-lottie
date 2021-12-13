from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from wagtail.tests.utils import WagtailTestUtils
from wagtail_lottie.models import LottieAnimation
from wagtail_lottie.blocks import LottieAnimationChooserBlock

from . import _constants


class TestLottieCreateView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    def get(self, params={}):
        return self.client.get(reverse('wagtail_lottie_lottieanimation_modeladmin_create'), params)

    def post(self, post_data={}):
        return self.client.post(reverse('wagtail_lottie_lottieanimation_modeladmin_create'), post_data)

    def test_get(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modeladmin/wagtail_lottie/lottieanimation/create.html')
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_create(self):
        with open(_constants.TEST_ZIP_FILE_PATH, 'rb') as zip_file:
            response = self.post({
                'title': 'test',
                'zip_file': SimpleUploadedFile('zip_file.zip', zip_file.read()),
                'play_mode': LottieAnimation.PLAY_MODE_AUTO,
                'loop': True,
                'renderer': LottieAnimation.RENDERER_SVG,
                'prefers_color_scheme': LottieAnimation.PREFERS_COLOR_SCHEME_NONE,
                'preserve_aspect_ratio': LottieAnimation.PRESERVE_ASPECT_RATIO_DEFAULT
            })

        # Should redirect back to index
        self.assertRedirects(response, reverse('wagtail_lottie_lottieanimation_modeladmin_index'))

        # Check that the animation was created
        animations = LottieAnimation.objects.filter(name="London")
        animation_london = animations.first()
        self.assertGreaterEqual(animations.count(), 1)

        # Check that images was created
        self.assertEqual(
            animation_london.lottieanimationimage_set.count(),
            49
        )

        animation_london_rendition = LottieAnimationChooserBlock().render(animation_london, {
            'animation_class': 'w-full',
            'container_class': 'h-full',
        })
        self.assertIn(
            'data-preserve-aspect-ratio="%s"' % LottieAnimation.PRESERVE_ASPECT_RATIO_DEFAULT,
            animation_london_rendition
        )
        self.assertIn('data-animation-class="w-full"', animation_london_rendition)
        self.assertIn('class="h-full"', animation_london_rendition)


class TestLottieEditView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()
        with open(_constants.TEST_ZIP_FILE_PATH, 'rb') as zip_file:
            self.animation = LottieAnimation.objects.create(
                zip_file=File(zip_file.read()),
                play_mode=LottieAnimation.PLAY_MODE_AUTO,
                loop=True,
                renderer=LottieAnimation.RENDERER_SVG,
                prefers_color_scheme=LottieAnimation.PREFERS_COLOR_SCHEME_NONE,
                preserve_aspect_ratio=LottieAnimation.PRESERVE_ASPECT_RATIO_DEFAULT
            )

    def get(self, params={}):
        return self.client.get(
            reverse('wagtail_lottie_lottieanimation_modeladmin_edit', args=(self.animation.id,)),
            params
        )

    def post(self, post_data={}):
        return self.client.post(
            reverse('wagtail_lottie_lottieanimation_modeladmin_edit', args=(self.animation.id,)),
            post_data
        )

    def test_get(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modeladmin/wagtail_lottie/lottieanimation/edit.html')
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_edit(self):
        with open(_constants.TEST_ZIP_FILE_PATH_2, 'rb') as zip_file:
            response = self.post({
                'title': 'test',
                'zip_file': SimpleUploadedFile('zip_file.zip', zip_file.read()),
                'play_mode': LottieAnimation.PLAY_MODE_AUTO,
                'loop': True,
                'renderer': LottieAnimation.RENDERER_SVG,
                'prefers_color_scheme': LottieAnimation.PREFERS_COLOR_SCHEME_NONE,
                'preserve_aspect_ratio': LottieAnimation.PRESERVE_ASPECT_RATIO_DEFAULT
            })
        self.assertRedirects(response, reverse('wagtail_lottie_lottieanimation_modeladmin_index'))
        animations = LottieAnimation.objects.filter(name="bloc-1-bulles-1")
        self.assertGreaterEqual(animations.count(), 1)
