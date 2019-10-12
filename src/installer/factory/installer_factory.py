from src.installer.factory.extractor import ZipExtractor, SevenZipExtractor
from src.installer.factory.runner import CommandRunner


class InstallerFactory:
    def __init__(self):
        self.extractor = None
        self.cmd_runner = None
        self.extension = ''

    def with_extension(self, extension):
        self.extension = extension
        return self

    def find(self):
        switch = {
            'exe': CommandRunner(),
            'zip': ZipExtractor(),
            '7z': SevenZipExtractor()
        }

        return switch.get(self.extension, None)
