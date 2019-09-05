import unittest
from unittest.mock import patch

from src.main.python.installer.installer_api import AppInstallAPI


class TestAppInstallAPI(unittest.TestCase):
    @patch('src.main.python.installer.app_installer.ApplicationInstaller')
    def setUp(self, mock_installer):
        # AppInstallAPI code to do setup
        self.mock_installer = mock_installer
        self.api = AppInstallAPI(installer=mock_installer)

    def test_install_api_post(self):
        # given
        app_id = '1'

        # when
        result = self.api.post(app_id)

        # then
        self.assertEqual(result, (None, 204))
        self.mock_installer.install.assert_called_once_with(app_id)
    
    def test_install_api_delete(self):
        # given
        app_id = '1'

        # when
        result = self.api.delete(app_id)

        # then
        self.assertEqual(result, (None, 204))
        self.mock_installer.uninstall.assert_called_once_with(app_id)


if __name__ == '__main__':
    unittest.main()