from src.installer.factory import ZipExtractor, SevenZipExtractor, CommandRunner, RarExtractor


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
            '7z': SevenZipExtractor(),
            'rar': RarExtractor()
        }

        return switch.get(self.extension, None)
