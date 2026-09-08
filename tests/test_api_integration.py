"""Integration tests for App-Manager's Flask REST API.

Unlike the rest of tests/, these hit a real Flask app (test client), a real
AppRepository against a temp SQLite file, and a real ApplicationInstaller —
only the true external boundaries (network download, subprocess execution)
are stubbed. This gives HTTP-level coverage of the same surface
postman_collection.json used to exercise manually.

These tests assert ACTUAL, documented behavior — including known bugs (see
docs/user/api-reference.md) — not the originally-intended behavior. A test
named/commented as pinning a known bug is expected to start failing the day
that bug is fixed; that failure means "update this test", not "regression".
"""
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from flask import Flask
from flask_restful import Api

from src.installer.app_downloader import ApplicationDownloader
from src.installer.app_installer import ApplicationInstaller
from src.installer.factory.extractor import Extractor
from src.installer.installer_api import AppInstallAPI
from src.manager.app_api import AppAPI, AppRegisterAPI
from src.manager.app_list_api import AppListAPI
from src.model.application import ApplicationDecoder, ApplicationEncoder
from src.repository.app_repo import AppRepository
from src.repository.repo_initializer import AppRepositoryInitializer


class TestAppManagerApiIntegration(unittest.TestCase):
    def setUp(self):
        # Real, temp-file SQLite DB. AppRepository.connect() opens a new
        # connection per call, so ':memory:' would not survive across calls.
        db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        os.close(db_fd)

        encoder = ApplicationEncoder()
        decoder = ApplicationDecoder()

        AppRepositoryInitializer(encoder, decoder, repo_name=self.db_path).initialize()
        self.repo = AppRepository(encoder, decoder, repo_name=self.db_path)

        # Redirect the installer's/downloader's real filesystem side effects
        # (./working/installation, ./working/cache/installers) into temp dirs
        # instead of the repo checkout.
        self.install_root = tempfile.mkdtemp()
        self.cache_root = tempfile.mkdtemp()

        with patch('src.installer.app_downloader.os.makedirs'):
            self.downloader = ApplicationDownloader()
        self.downloader.installer_cache = self.cache_root + '/'

        self.installer = ApplicationInstaller(repo=self.repo, downloader=self.downloader, app_initializer=None)
        self.installer.install_dir = self.install_root

        # InstallerFactory.find() eagerly constructs every handler type
        # (CommandRunner, ZipExtractor, SevenZipExtractor, RarExtractor) on
        # every call regardless of which extension is requested, and
        # Extractor.__init__ unconditionally creates a real
        # ./working/cache/extracted — so this fires on *every* install or
        # uninstall call, even a plain .exe one. Redirect it to a temp dir
        # by replacing Extractor.__init__ outright, rather than patching
        # os.makedirs globally — os.makedirs is the same shared function
        # ApplicationInstaller.install() itself calls to create the (real,
        # intentional) install_dir, so a global patch would silently break
        # that too.
        self.extractor_root = tempfile.mkdtemp()
        self.extractor_init_patcher = patch.object(
            Extractor, '__init__',
            lambda extractor_self: setattr(extractor_self, 'working_dir', self.extractor_root))
        self.extractor_init_patcher.start()

        app = Flask(__name__)
        # Explicit, rather than relying on TESTING's default: makes the
        # documented 500s assertable as real responses instead of exceptions
        # propagating into the test process.
        app.config['PROPAGATE_EXCEPTIONS'] = False
        app.json_encoder = ApplicationEncoder

        api = Api(app)
        api.add_resource(AppInstallAPI, '/app/<int:app_id>/install', endpoint='app_install',
                          resource_class_kwargs={'installer': self.installer})
        api.add_resource(AppAPI, '/app/<int:app_id>', endpoint='app_inquiry_update_delete',
                          resource_class_kwargs={'repo': self.repo})
        api.add_resource(AppRegisterAPI, '/app', '/app/<int:app_id>', endpoint='app_registration',
                          resource_class_kwargs={'repo': self.repo})
        api.add_resource(AppListAPI, '/apps', endpoint='app_query', resource_class_kwargs={'repo': self.repo})

        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        self.extractor_init_patcher.stop()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        shutil.rmtree(self.install_root, ignore_errors=True)
        shutil.rmtree(self.cache_root, ignore_errors=True)
        shutil.rmtree(self.extractor_root, ignore_errors=True)

    # -- helpers -----------------------------------------------------------

    def _register_app(self, name='foo', source_url='http://example.com/foo.exe', system='windows'):
        resp = self.client.post('/app', json={
            'name': name, 'source_url': source_url, 'system': system, 'is_package': False,
        })
        return resp.get_json()['resource_uri'].rsplit('/', 1)[-1]

    def _register_package(self, name='git', system='linux'):
        resp = self.client.post('/app', json={'name': name, 'system': system, 'is_package': True})
        return resp.get_json()['resource_uri'].rsplit('/', 1)[-1]

    # -- GET/DELETE /apps ----------------------------------------------------

    def test_get_apps_empty(self):
        resp = self.client.get('/apps')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    def test_get_apps_always_reports_is_package_false_known_bug(self):
        self._register_package(name='git', system='linux')
        self._register_app(name='foo', source_url='http://example.com/foo.exe', system='windows')

        apps = self.client.get('/apps').get_json()
        self.assertEqual(len(apps), 2)
        # Known bug: load_apps() doesn't even SELECT the PACKAGE column, so
        # is_package defaults to False for every row, including the package.
        for app in apps:
            self.assertFalse(app['is_package'])

    def test_delete_apps_removes_everything(self):
        self._register_app()
        self._register_app(name='bar')

        resp = self.client.delete('/apps')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.client.get('/apps').get_json(), [])

    # -- POST /app (register app / register package) -----------------------

    def test_post_app_registers_and_returns_resource_uri(self):
        resp = self.client.post('/app', json={
            'name': 'foo', 'source_url': 'http://example.com/foo.exe', 'system': 'windows', 'is_package': False,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_json()['resource_uri'], r'^/app/\d+$')

    def test_post_app_upsert_by_identity_returns_same_id_no_duplicate(self):
        payload = {'name': 'foo', 'source_url': 'http://example.com/foo.exe', 'system': 'windows', 'is_package': False}

        first = self.client.post('/app', json=payload).get_json()
        second = self.client.post('/app', json=payload).get_json()

        self.assertEqual(first['resource_uri'], second['resource_uri'])
        self.assertEqual(len(self.client.get('/apps').get_json()), 1)

    def test_post_app_invalid_source_url_returns_500(self):
        # Validator.validate_url raises a bare Exception with no
        # abort()/HTTPException handling — under PROPAGATE_EXCEPTIONS=False
        # that surfaces as a 500, not a clean 4xx rejection.
        resp = self.client.post('/app', json={
            'name': 'foo', 'source_url': 'not-a-url', 'system': 'windows', 'is_package': False,
        })
        self.assertEqual(resp.status_code, 500)

    def test_post_app_register_package_does_not_require_source_url(self):
        resp = self.client.post('/app', json={'name': 'git', 'system': 'linux', 'is_package': True})
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_json()['resource_uri'], r'^/app/\d+$')

    # -- GET /app/<id> -------------------------------------------------------

    def test_get_app_by_id(self):
        app_id = self._register_app(name='foo')
        resp = self.client.get('/app/{}'.format(app_id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['name'], 'foo')

    def test_get_app_by_id_missing_returns_404(self):
        resp = self.client.get('/app/999')
        self.assertEqual(resp.status_code, 404)

    # -- PUT /app/<id> --------------------------------------------------------

    def test_put_app_does_not_persist_known_bug(self):
        app_id = self._register_app(name='foo', source_url='http://example.com/foo.exe', system='windows')

        resp = self.client.put('/app/{}'.format(app_id), json={
            'name': 'renamed', 'source_url': 'http://example.com/bar.exe', 'system': 'linux',
        })
        self.assertEqual(resp.status_code, 200)
        # The response looks like the edit succeeded...
        self.assertEqual(resp.get_json()['name'], 'renamed')

        # ...but AppAPI.put() never calls repo.update_app(), so a follow-up
        # GET shows the old values.
        fetched = self.client.get('/app/{}'.format(app_id)).get_json()
        self.assertEqual(fetched['name'], 'foo')

    # -- DELETE /app/<id> -----------------------------------------------------

    def test_delete_app_missing_returns_404(self):
        resp = self.client.delete('/app/999')
        self.assertEqual(resp.status_code, 404)

    def test_delete_app_installed_returns_409(self):
        app_id = self._register_app(name='foo', source_url='http://example.com/foo.exe', system='windows')
        fake_exe = os.path.join(self.install_root, 'foo.exe')
        with patch.object(self.downloader, 'download', return_value=fake_exe), \
                patch('src.installer.factory.runner.CommandRunner.run'):
            self.client.post('/app/{}/install'.format(app_id))

        resp = self.client.delete('/app/{}'.format(app_id))
        self.assertEqual(resp.status_code, 409)

    def test_delete_app_removes_row(self):
        app_id = self._register_app(name='foo')
        resp = self.client.delete('/app/{}'.format(app_id))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.client.get('/app/{}'.format(app_id)).status_code, 404)

    # -- POST /app/<id>/install -----------------------------------------------

    def test_post_install_exe_flips_installed_true(self):
        app_id = self._register_app(name='foo', source_url='http://example.com/foo.exe', system='windows')
        fake_exe = os.path.join(self.install_root, 'foo.exe')

        # CommandRunner.run()'s body is `if sys.platform == 'win32':`, a
        # no-op on Linux CI — patch it explicitly so this test's outcome
        # doesn't depend on the host platform.
        with patch.object(self.downloader, 'download', return_value=fake_exe), \
                patch('src.installer.factory.runner.CommandRunner.run') as mock_run:
            resp = self.client.post('/app/{}/install'.format(app_id))

        self.assertEqual(resp.status_code, 204)
        mock_run.assert_called_once()
        self.assertTrue(self.client.get('/app/{}'.format(app_id)).get_json()['installed'])

    def test_post_install_archive_never_extracted_but_still_flips_installed_true(self):
        app_id = self._register_app(name='foo', source_url='http://example.com/foo.zip', system='windows')
        fake_zip = os.path.join(self.install_root, 'foo.zip')

        with patch.object(self.downloader, 'download', return_value=fake_zip):
            resp = self.client.post('/app/{}/install'.format(app_id))

        self.assertEqual(resp.status_code, 204)
        # Known bug: install() unconditionally sets installed=True after the
        # branching that would extract a .zip — which never happens.
        self.assertTrue(self.client.get('/app/{}'.format(app_id)).get_json()['installed'])
        app_install_dir = os.path.join(self.install_root, 'foo')
        self.assertEqual(os.listdir(app_install_dir), [])

    def test_post_install_unknown_app_id_returns_500(self):
        resp = self.client.post('/app/999/install')
        self.assertEqual(resp.status_code, 500)

    def test_post_install_registered_as_package_returns_500_known_bug(self):
        # PACKAGE round-trips through SQLite as an int (1/0), but
        # AppRepository.load_app() compares it against the string 'True',
        # so is_package always reconstructs False. That falls through to
        # the non-package branch with source_url=None. urlparse(None) and
        # os.path.basename() on its result both succeed; the TypeError
        # actually fires one line later, at
        # ApplicationInstaller.__discover_extension's `ext.split('.')`,
        # since you can't call bytes.split(str). Confirmed by direct
        # reproduction — it crashes before any network call.
        app_id = self._register_package(name='git', system='linux')

        with patch.object(self.downloader, 'download') as mock_download:
            resp = self.client.post('/app/{}/install'.format(app_id))
            mock_download.assert_not_called()

        self.assertEqual(resp.status_code, 500)

    def test_post_install_extensionless_url_hits_broken_content_disposition_fallback(self):
        # No extension in the URL path, so ApplicationDownloader.download()
        # falls back to reading Content-Disposition. That fallback is
        # broken: response.headers['content-disposition'] KeyErrors when
        # the header is absent (only the requests.get boundary is stubbed
        # here, not download() itself, so this exercises the real bug).
        app_id = self._register_app(name='foo', source_url='http://example.com/download', system='windows')

        fake_response = MagicMock()
        fake_response.headers = {}
        fake_response.iter_content.return_value = [b'data']

        with patch('src.installer.app_downloader.requests.get', return_value=fake_response):
            resp = self.client.post('/app/{}/install'.format(app_id))

        self.assertEqual(resp.status_code, 500)

    # -- DELETE /app/<id>/install ---------------------------------------------

    def test_delete_install_always_204_and_never_flips_installed_back_known_bug(self):
        app_id = self._register_app(name='foo', source_url='http://example.com/foo.exe', system='windows')
        fake_exe = os.path.join(self.install_root, 'foo.exe')
        with patch.object(self.downloader, 'download', return_value=fake_exe), \
                patch('src.installer.factory.runner.CommandRunner.run'):
            self.client.post('/app/{}/install'.format(app_id))

        resp = self.client.delete('/app/{}/install'.format(app_id))
        self.assertEqual(resp.status_code, 204)

        # Known bug: a tuple-truthiness bug in __discover_uninstaller makes
        # the runner lookup always fail, so uninstall() is a permanent no-op.
        self.assertTrue(self.client.get('/app/{}'.format(app_id)).get_json()['installed'])

    def test_delete_install_unknown_app_id_returns_500(self):
        # Unlike install(), uninstall() has no explicit check-and-raise —
        # this 500s via an unguarded app.get_name() call on None.
        resp = self.client.delete('/app/999/install')
        self.assertEqual(resp.status_code, 500)


if __name__ == '__main__':
    unittest.main()
