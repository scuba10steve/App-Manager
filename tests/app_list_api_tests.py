import unittest
from unittest.mock import patch

from src.model.application import Application
from src.manager.app_list_api import AppListAPI


class test_AppListAPI(unittest.TestCase):
    @patch('src.model.application.ApplicationEncoder')
    @patch('src.repository.app_repo.AppRepository')
    def setUp(self, mock_encoder, mock_repo):
        super().__init__()
        # AppListAPI code to do setup
        self.mock_encoder = mock_encoder
        self.mock_repo = mock_repo
        self.api = AppListAPI(encoder=mock_encoder, repo=mock_repo)

    def test_AppListAPI_post_no_results(self):
        #given
        self.mock_repo.load_apps.return_value = []

        #when
        result = self.api.get()

        #then
        self.assertEqual(result, ([], 200))
        self.mock_repo.load_apps.assert_called_once()
    
    def test_AppListAPI_post(self):
        #given
        app = Application("foo", 'http://foo.zip', 'some_system')
        self.mock_repo.load_apps.return_value = [app]
        self.mock_encoder.encode.return_value = app

        #when
        result = self.api.get()

        #then
        self.assertEqual(result, ([app], 200))
        self.mock_repo.load_apps.assert_called_once()

    def test_AppListAPI_delete(self):
        #given
        self.mock_repo.remove_apps.return_value = None

        #when
        result = self.api.delete()

        #then
        self.assertEqual((None, 204), result)
        self.mock_repo.remove_apps.assert_called_once()
    

    # def test_AppListAPI_delete(self):
    #     #given
    #     app_id = '1'

    #     #when
    #     result = self.api.delete(app_id)

    #     #then
    #     self.assertEqual(result, (None, 204))
    #     self.mock_encoder.uninstall.assert_called_once_with(app_id)


if __name__ == '__main__':
    unittest.main()
