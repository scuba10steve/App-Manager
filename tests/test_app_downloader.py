import os
import unittest
from unittest.mock import patch, MagicMock, Mock

from src.installer.app_downloader import ApplicationDownloader
from tests import mock_files


class TestApplicationDownloader(unittest.TestCase):
    @patch('src.installer.app_downloader.requests')
    def setUp(self, requests):
        self.requests = requests

    def test_downloader_returns_location(self):
        # given
        downloader = ApplicationDownloader()
        url = 'http://foo'
        app_name = 'foo'
        # Mocks
        os.path.isfile = MagicMock(return_value=True)

        # when
        result = downloader.download(url, app_name, 'exe')

        # then
        self.assertEqual(result, './working/cache/installers/foo.exe')

    def test_downloader_created(self):
        makedirs = mock_files(os)

        # create the downloader instance
        ApplicationDownloader()
        makedirs.assert_called_once_with('./working/cache/installers/')


if __name__ == '__main__':
    unittest.main()
