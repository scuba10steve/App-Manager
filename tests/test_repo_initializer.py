import unittest
from unittest.mock import patch, MagicMock

from src.repository.repo_initializer import AppRepositoryInitializer


class TestAppRepositoryInitializer(unittest.TestCase):
    def setUp(self):
        self.repo = AppRepositoryInitializer(repo_name=':memory:')

    def test_init_app(self):
        with patch('src.repository.app_repo.sqlite3') as sqlite3:
            # given
            conn = sqlite3.Connection(':memory:')
            conn.row_factory = None
            sqlite3.connect = MagicMock(return_value=conn)
            conn.execute.return_value = ''

            # when
            self.repo.store_sys_metadata('win', '10', 'choco')

            # then
            sqlite3.connect.assert_called_once_with(':memory:')
            conn.execute.assert_called_once_with('SELECT 1 FROM SYSTEM_METADATA WHERE SYS_ID = ?', ('win',))
