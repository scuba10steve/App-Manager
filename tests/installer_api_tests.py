import unittest
from unittest.mock import patch, MagicMock, Mock

import os

from installer.installer_api import AppInstallAPI

class test_AppInstallAPI(unittest.TestCase):
    @patch('installer.app_installer.ApplicationInstaller')
    def setUp(self, mock_installer):
        # AppInstallAPI code to do setup
        self.mock_installer = mock_installer
        self.api = AppInstallAPI(installer=mock_installer)

    def test_AppInstallAPI_post(self):
        #given
        app_id = '1'

        #when
        result = self.api.post(app_id)

        #then
        self.assertEqual(result, (None, 204))
        self.mock_installer.install.assert_called_once_with(app_id)
    
    def test_AppInstallAPI_delete(self):
        #given
        app_id = '1'

        #when
        result = self.api.delete(app_id)

        #then
        self.assertEqual(result, (None, 204))
        self.mock_installer.uninstall.assert_called_once_with(app_id)


if __name__ == '__main__':
    unittest.main()