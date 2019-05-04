import os
import unittest
from unittest.mock import patch, MagicMock, Mock

from src.installer.app_installer import ApplicationInstaller
from src.model.application import Application
from tests import mock_files


class PseudoDirEntry:
    def __init__(self, name, path, is_dir, stat):
        self.name = name
        self.path = path
        self._is_dir = is_dir
        self._stat = stat

    def is_dir(self):
        return self._is_dir

    def stat(self):
        return self._stat


class TestApplicationInstaller(unittest.TestCase):
    @patch('src.repository.app_repo.AppRepository')
    @patch('src.installer.app_downloader.ApplicationDownloader')
    @patch('src.installer.factory.installer_factory.InstallerFactory')
    def setUp(self, mock_repo, mock_downloader, installer_factory):
        # ApplicationInstaller code to do setup
        self.mock_repo = mock_repo
        self.mock_downloader = mock_downloader
        self.installer_factory = installer_factory
        self.installer = ApplicationInstaller(repo=mock_repo, downloader=mock_downloader, factory=installer_factory)

    def test_installer_created_correctly(self):
        self.assertEqual(self.installer.install_dir, './working/installation')
        self.assertTrue(self.mock_repo is not None)

    def test_installer_installs_application(self):
        # Given
        # data
        app = Application('foo', 'http://somesite/foo.exe', 'bar', '1')
        app.set_installed(True)
        install_dir = self.installer.install_dir + '/foo'

        # Mocks
        makedirs = mock_files(os)

        self.mock_downloader.download.return_value = 'foo.exe'
        self.mock_repo.load_app.return_value = app

        # When
        self.installer.install('1')

        # Then
        makedirs.assert_called_once_with(install_dir)
        self.mock_repo.load_app.assert_called_once_with('1')
        self.mock_downloader.download.assert_called_once_with('http://somesite/foo.exe', 'foo', None)
        self.mock_repo.update_app.assert_called_once_with(app)

    def test_installer_uninstalls_application(self):
        # Given
        app = Application('foo', 'http://foo', 'bar', '1')
        app.set_installed(True)
        self.mock_repo.load_app.return_value = app
        self.installer_factory.find.return_value = ""

        cmd = self.installer.install_dir + '/foo/unins000.exe'

        def scandir(*args):
            return [PseudoDirEntry('unins000.exe', cmd, False, None)]

        os.path.exists = MagicMock(return_value=True)
        os.scandir = MagicMock(side_effect=scandir)

        # When
        self.installer.uninstall('1')

        # Then
        self.assertEqual(app.installed, False)
        self.mock_repo.update_app.assert_called_once_with(app)


if __name__ == '__main__':
    unittest.main()
