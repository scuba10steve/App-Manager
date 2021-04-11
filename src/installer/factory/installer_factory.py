from typing import Union

from src.installer.factory.extractor import ZipExtractor, SevenZipExtractor, RarExtractor
from src.installer.factory.runner import CommandRunner, ChocoRunner, HomebrewRunner


class InstallerFactory:
    def __init__(self):
        self.extractor = None
        self.cmd_runner = None
        self.extension: str = ''
        self.command: str = ''

    def with_extension(self, extension: str):
        self.extension = extension
        return self

    def with_command(self, command: str):
        self.command = command
        return self

    def find(self) -> Union[CommandRunner, ZipExtractor, SevenZipExtractor, RarExtractor, ChocoRunner, HomebrewRunner, None]:
        extensions = {
            'exe': CommandRunner(),
            'zip': ZipExtractor(),
            '7z': SevenZipExtractor(),
            'rar': RarExtractor()
        }

        commands = {
            'choco': ChocoRunner(),
            'brew': HomebrewRunner()
        }

        if self.extension:
            return extensions.get(self.extension, None)
        if self.command:
            return commands.get(self.command, None)

        return None
