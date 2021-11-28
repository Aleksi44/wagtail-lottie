from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from wagtail.tests.utils import WagtailTestUtils
from wagtail_lottie.models import LottieAnimation

from . import _constants


class TestImageCreateView(TestCase, WagtailTestUtils):
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
                'zip_file': SimpleUploadedFile('zip_file.zip', zip_file.read()),
                'play_mode': LottieAnimation.PLAY_MODE_AUTO,
                'loop': True,
                'renderer': LottieAnimation.RENDERER_SVG,
                'prefers_color_scheme': LottieAnimation.PREFERS_COLOR_SCHEME_NONE
            })

        # Should redirect back to index
        self.assertRedirects(response, reverse('wagtail_lottie_lottieanimation_modeladmin_index'))

        # Check that the animation was created
        animations = LottieAnimation.objects.filter(name="London")
        self.assertEqual(animations.count(), 1)

        # Check that images was created
        self.assertEqual(
            animations.first().lottieanimationimage_set.count(),
            49
        )
