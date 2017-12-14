import unittest
from unittest.mock import patch, MagicMock, Mock

import sys
import os
sys.path.append('../')

from installer.app_installer import ApplicationInstaller
from model.application import Application

class test_ApplicationInstaller(unittest.TestCase):
    @patch('repository.app_repo.AppRepository')
    @patch('installer.app_installer.CommandRunner')
    @patch('installer.app_downloader.ApplicationDownloader')
    def setUp(self, mock_repo, mock_runner, mock_downloader):
        ###  ApplicationInstaller code to do setup
        self.mock_repo = mock_repo
        self.mock_runner = mock_runner
        self.mock_downloader = mock_downloader
        self.installer = ApplicationInstaller(repo=mock_repo, runner=mock_runner, downloader=mock_downloader)
        pass
    
    def test_ApplicationInstallerCreatedCorrectly(self):
        self.assertEqual(self.installer.install_dir, './installation')
        self.assertTrue(self.mock_repo != None)
        self.assertTrue(self.mock_runner != None)


    def test_ApplicationInstaller_installsApplication(self):
        # Given
        # data
        app = Application('foo', 'http://foo', 'bar', '1')
        app.set_installed(True)
        install_dir = self.installer.install_dir + '/foo'

        #Mocks
        os.path = MagicMock()
        makedirs = Mock()

        def do_stuff(*args):
            makedirs(args[0])
        
        os.path.exists = MagicMock(return_value=False)
        os.makedirs = Mock(side_effect=do_stuff)

        self.mock_downloader.download.return_value = 'foo.exe'
        self.mock_repo.load_app.return_value = app
        
        # When
        self.installer.install('1')
        
        # Then
        makedirs.assert_called_once_with(install_dir)
        self.mock_repo.load_app.assert_called_once_with('1')
        self.mock_downloader.download.assert_called_once_with('http://foo', 'foo')
        self.mock_runner.run.assert_called_once_with('foo.exe', install_dir)
        self.mock_repo.update_app.assert_called_once_with(app)
    

    def test_ApplicationInstaller_uninstalls_application(self):
        #Given
        app = Application('foo', 'http://foo', 'bar', '1')
        app.set_installed(True)
        self.mock_repo.load_app.return_value = app

        cmd = self.installer.install_dir + '/foo/unins000.exe'

        #When
        self.installer.uninstall('1')

        #Then
        self.mock_runner.run.assert_called_once_with(cmd)
        app.set_installed(False)
        self.mock_repo.update_app.assert_called_once_with(app)
        

if __name__ == '__main__':
    unittest.main()
