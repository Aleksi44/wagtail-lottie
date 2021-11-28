from django.test import SimpleTestCase
from wagtail_lottie.lottie_zip_file import LottieZipFile

from . import _constants


class TestLottieZipFile(SimpleTestCase):
    def setUp(self):
        self.lottie_zip_file = LottieZipFile(_constants.TEST_ZIP_FILE_PATH)

    def test_attr(self):
        self.assertEqual(
            self.lottie_zip_file.extract_filename(self.lottie_zip_file.json_path),
            'body.json'
        )
        self.assertEqual(
            len(self.lottie_zip_file.images_path),
            49
        )
        self.assertEqual(
            self.lottie_zip_file.width,
            1000
        )
        self.assertEqual(
            self.lottie_zip_file.height,
            1000
        )
        self.assertEqual(
            self.lottie_zip_file.version,
            "5.7.4"
        )
