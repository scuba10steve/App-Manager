import unittest

from src.installer.factory.installer_factory import InstallerFactory
from src.installer.factory.runner import CommandRunner, ChocoRunner, HomebrewRunner
from src.installer.factory.extractor import ZipExtractor, SevenZipExtractor, RarExtractor

class TestInstallerFactory(unittest.TestCase):
    def test_exe(self):
        #setup
        factory = InstallerFactory()
        factory.with_extension('exe')

        #when
        result = factory.find()

        #then
        assert type(result) is CommandRunner

    def test_zip(self):
        #setup
        factory = InstallerFactory()
        factory.with_extension('zip')

        #when
        result = factory.find()

        #then
        assert type(result) is ZipExtractor

    def test_7z(self):
        #setup
        factory = InstallerFactory()
        factory.with_extension('7z')

        #when
        result = factory.find()

        #then
        assert type(result) is SevenZipExtractor

    def test_rar(self):
        #setup
        factory = InstallerFactory()
        factory.with_extension('rar')

        #when
        result = factory.find()

        #then
        assert type(result) is RarExtractor

    def test_choco(self):
        #setup
        factory = InstallerFactory()
        factory.with_command('choco')

        #when
        result = factory.find()

        #then
        assert type(result) is ChocoRunner

    def test_homebrew(self):
        #setup
        factory = InstallerFactory()
        factory.with_command('brew')

        #when
        result = factory.find()

        #then
        assert type(result) is HomebrewRunner

if __name__ == '__main__':
    unittest.main()
