import os
from zipfile import BadZipFile, LargeZipFile
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.views import CreateView
from generic_chooser.views import ModelChooserViewSet

from .models import LottieAnimation, LottieAnimationImage
from .lottie_zip_file import LottieZipFile
from .exceptions import WagtailLottieException


class LottieAnimationChooserViewSet(ModelChooserViewSet):
    model = LottieAnimation
    icon = 'image'
    page_title = _("Choose lottie animation")
    per_page = 10


class CreateViewLottieAnimation(CreateView):

    def form_valid(self, form):
        response = super().form_valid(form)

        try:
            lottie_zip_file = LottieZipFile(form.instance.zip_file.path)
        except (WagtailLottieException, BadZipFile, LargeZipFile) as err:
            self._delete_django_messages()
            messages.error(self.request, str(err))
            self.instance.delete()
            return self.render_to_response(self.get_context_data(form=form))

        self.instance.uuid = lottie_zip_file.uuid
        self.instance.name = lottie_zip_file.name
        self.instance.width = lottie_zip_file.width
        self.instance.height = lottie_zip_file.height
        self.instance.version = lottie_zip_file.version

        self.instance.json_file.save(
            os.path.join(self.instance.uuid, 'body.json'),
            lottie_zip_file.open(lottie_zip_file.json_path)
        )

        for image in lottie_zip_file.images_path:
            lottie_animation = LottieAnimationImage.objects.create(animation_id=self.instance.id)
            lottie_animation.image.save(
                os.path.join(
                    self.instance.uuid,
                    "images",
                    lottie_zip_file.extract_filename(image)
                ),
                lottie_zip_file.open(image)
            )
        return response

    def _delete_django_messages(self):
        # Monkey patch - Clear django messages
        storage = messages.get_messages(self.request)
        for _ in storage:  # noqa: F402
            pass
        for _ in list(storage._loaded_messages):
            del storage._loaded_messages[0]
