import unittest
from unittest.mock import patch, MagicMock

from src.repository.app_repo import AppRepository


class test_AppRepository(unittest.TestCase):
    @patch('src.model.application.ApplicationDecoder')
    @patch('src.model.application.ApplicationEncoder')
    def setUp(self, mock_encoder, mock_decoder):
        # ApplicationInstaller code to do setup
        self.repo = AppRepository(encoder=mock_encoder, decoder=mock_decoder, repo_name=':memory:')

    def test_load_app(self):
        with patch('src.repository.app_repo.sqlite3') as sqlite3:
            #given
            conn = sqlite3.Connection(':memory:')
            conn.row_factory = None
            sqlite3.connect = MagicMock(return_value=conn)
            conn.execute.return_value = ''
            #when
            self.repo.load_app('1')
            #then
            sqlite3.connect.assert_called_once_with(':memory:')
            conn.execute.assert_called_once_with('SELECT ID, NAME, SOURCE_URL, SYSTEM, INSTALLED FROM APPS WHERE ID = ?', ('1',))
            conn.close.assert_called_once()

            #cleanup
            conn.close()

    def test_load_apps(self):
        with patch('src.repository.app_repo.sqlite3') as sqlite3:
            #given
            conn = sqlite3.Connection(':memory:')
            conn.row_factory = None
            sqlite3.connect = MagicMock(return_value=conn)
            conn.execute.return_value = ''
            #when
            self.repo.load_apps()
            #then
            sqlite3.connect.assert_called_once_with(':memory:')
            conn.execute.assert_called_once_with('SELECT ID, NAME, SOURCE_URL, SYSTEM, INSTALLED FROM APPS')
            conn.close.assert_called_once()

            #cleanup
            conn.close()
    
    def test_remove_app(self):
        with patch('src.repository.app_repo.sqlite3') as sqlite3:
            #given
            conn = sqlite3.Connection(':memory:')
            conn.row_factory = None
            sqlite3.connect = MagicMock(return_value=conn)
            conn.execute.return_value = ''
            #when
            self.repo.remove_app('1')
            #then
            sqlite3.connect.assert_called_once_with(':memory:')
            conn.execute.assert_called_once_with('DELETE FROM APPS WHERE ID = ?', '1')
            conn.close.assert_called_once()

            #cleanup
            conn.close()

    def test_remove_apps(self):
        with patch('src.repository.app_repo.sqlite3') as sqlite3:
            #given
            conn = sqlite3.Connection(':memory:')
            conn.row_factory = None
            sqlite3.connect = MagicMock(return_value=conn)
            conn.execute.return_value = ''
            #when
            self.repo.remove_apps()
            #then
            sqlite3.connect.assert_called_once_with(':memory:')
            conn.execute.assert_called_once_with('DELETE FROM APPS')
            conn.close.assert_called_once()

            #cleanup
            conn.close()


if __name__ == '__main__':
    unittest.main()
