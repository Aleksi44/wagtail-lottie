from django.conf import settings

WAGTAIL_LOTTIE_UPLOAD_FOLDER = getattr(settings, 'WAGTAIL_LOTTIE_UPLOAD_FOLDER', 'wagtail_lottie')
WAGTAIL_LOTTIE_UPLOAD_FOLDER_TMP = '%s/tmp' % WAGTAIL_LOTTIE_UPLOAD_FOLDER
