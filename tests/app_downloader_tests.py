import unittest
from unittest.mock import patch, MagicMock, Mock

import os

from src.installer.app_downloader import ApplicationDownloader


class test_ApplicationDownloader(unittest.TestCase):
    @patch('src.installer.app_downloader.requests')
    def setUp(self, requests):
        self.requests = requests

    # TODO: Update when mock works
    # def test_ApplicationDownloader_downloads(self):
    #     #given
    #     downloader = ApplicationDownloader()
    #     url = 'http://foo'
    #     app_name = 'foo'
    #     # Mocks
    #     os.path = MagicMock()
    #     get = Mock()
    #     f_open = Mock()
    #     resp = requests.Response()

    #     def do_stuff(*args, stream):
    #         get(args[0])

    #     def fake_open(location, mode):
    #         f_open(args)

    #     requests.get = Mock(side_effect=do_stuff, return_value=resp)

    #     os.path.isfile = MagicMock(return_value=False)

    #     open = Mock(side_effect=fake_open)

    #     #when
    #     result = downloader.download(url, app_name)

    #     #then
    #     self.requests.get.assert_called_once_with(url, stream=True)
    #     self.assertEqual(result, './installers/foo.exe')


    def test_ApplicationDownloader_returns_location(self):
        #given
        downloader = ApplicationDownloader()
        url = 'http://foo'
        app_name = 'foo'
        # Mocks
        os.path = MagicMock()

        os.path.isfile = MagicMock(return_value=True)

        #when
        result = downloader.download(url, app_name)

        #then
        self.assertEqual(result, './installers/foo.exe')

    def test_ApplicationDownloader_created(self):
        # Mocks
        os.path = MagicMock()
        makedirs = Mock()

        def do_stuff(*args):
            makedirs(args[0])

        os.path.exists = MagicMock(return_value=False)
        os.makedirs = Mock(side_effect=do_stuff)

        #create the downloader instance
        self.downloader = ApplicationDownloader()
        makedirs.assert_called_once_with('./installers/')



if __name__ == '__main__':
    unittest.main()
