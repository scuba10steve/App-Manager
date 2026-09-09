import os
import shutil
import tempfile
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

        # when
        # Scoped, self-restoring — a bare `os.path.isfile = MagicMock(...)`
        # here would leak into every other test in the process.
        with patch('src.installer.app_downloader.os.path.isfile', return_value=True):
            result = downloader.download(url, app_name, 'exe')

        # then
        self.assertEqual(result, './working/cache/installers/foo.exe')

    def test_download_known_extension_does_not_double_append_and_caches(self):
        # given: a real temp cache dir, so this doesn't depend on (or leak
        # into) global filesystem/os.path state.
        cache_dir = tempfile.mkdtemp() + '/'
        with patch('src.installer.app_downloader.os.makedirs'):
            downloader = ApplicationDownloader()
        downloader.installer_cache = cache_dir

        fake_response = MagicMock()
        fake_response.iter_content.return_value = [b'package-bytes']

        try:
            with patch('src.installer.app_downloader.requests.get', return_value=fake_response) as mock_get:
                # when: first call actually downloads
                result = downloader.download('http://example.com/foo.zip', 'foo', 'zip')

                # then: written to the single-extension path, not foo.zip.zip
                self.assertEqual(result, cache_dir + 'foo.zip')
                self.assertTrue(os.path.isfile(cache_dir + 'foo.zip'))
                self.assertFalse(os.path.isfile(cache_dir + 'foo.zip.zip'))
                mock_get.assert_called_once()

                # when: a second call for the same app/extension
                second_result = downloader.download('http://example.com/foo.zip', 'foo', 'zip')

                # then: the cache actually gets hit this time — no re-download
                self.assertEqual(second_result, cache_dir + 'foo.zip')
                mock_get.assert_called_once()
        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
