from django.utils.translation import gettext_lazy as _


class WagtailLottieException(Exception):
    pass


class MultipleJsonFilesError(WagtailLottieException):
    def __init__(self):
        super().__init__(_("Multiple json files found in zip archive"))


class JsonFileNotFoundError(WagtailLottieException):
    def __init__(self):
        super().__init__(_("Json file not found in zip archive"))
