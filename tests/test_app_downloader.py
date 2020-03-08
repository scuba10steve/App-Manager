import os
import unittest
from unittest.mock import patch, MagicMock

from src.installer.app_downloader import ApplicationDownloader


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


if __name__ == '__main__':
    unittest.main()
