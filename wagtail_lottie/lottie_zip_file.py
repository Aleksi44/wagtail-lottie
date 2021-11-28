import ntpath
import zipfile
import json
import uuid
from . import exceptions


class LottieZipFile(zipfile.ZipFile):

    def __init__(self, zip_file_path):
        super().__init__(zip_file_path)
        self.uuid = uuid.uuid4().hex
        self.name = ''
        self.json_path = ''
        self.images_path = []
        self.clean_json_file = None
        self.width = None
        self.height = None
        self._extract_files_path()
        self._extract_attr_json_file()

    @staticmethod
    def extract_filename(filename_path):
        head, tail = ntpath.split(filename_path)
        return tail or ntpath.basename(head)

    def _extract_files_path(self):
        zip_files_list = self.namelist()
        for file_to_extract in zip_files_list:
            if file_to_extract.endswith('.png'):
                self.images_path.append(file_to_extract)
            if file_to_extract.endswith('.json'):
                if not self.json_path:
                    self.json_path = file_to_extract
                else:
                    raise exceptions.MultipleJsonFilesError()
        if not self.json_path:
            raise exceptions.JsonFileNotFoundError()

    def _extract_attr_json_file(self):
        with self.open(self.json_path) as json_file:
            original_json = json.loads(json_file.read())
        self.name = original_json.get('nm', None)
        self.width = original_json.get('w', None)
        self.height = original_json.get('h', None)
        self.version = original_json.get('v', None)
