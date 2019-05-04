from unittest.mock import MagicMock, Mock


def mock_files(os):
    # Mocks
    os.path = MagicMock()
    makedirs = Mock()

    def do_stuff(*args):
        makedirs(args[0])

    os.path.exists = MagicMock(return_value=False)
    os.makedirs = Mock(side_effect=do_stuff)

    return makedirs
