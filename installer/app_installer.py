# external
import os
import sys
from subprocess import run

# internal
from repository.app_repo import AppRepository
from installer.app_downloader import ApplicationDownloader


class ApplicationInstaller():
    def __init__(self, repo=None, runner=None, downloader=None):
        self.install_dir = './installation'
        if not repo:
            self.repo = AppRepository
        else:
            self.repo = repo

        if not runner:
            self.runner = CommandRunner()
        else:
            self.runner = runner

        if not downloader:
            self.downloader = ApplicationDownloader()
        else:
            self.downloader = downloader

    def install(self, app_id):
        app = self.repo.load_app(app_id)
        if not app:
            raise Exception("Unable to update app that doesn't exist yet")
        url = app.get_sourceUrl()
        app_name = app.get_name()
        install_dir = self.install_dir + '/' + app_name

        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        executable = self.downloader.download(url, app_name)

        self.runner.run(executable, install_dir)

        app.set_installed(True)
        self.repo.update_app(app)

    def uninstall(self, app_id):
        app = self.repo.load_app(app_id)
        app_name = app.get_name()
        install_dir = self.install_dir + '/' + app_name
        if app.is_installed():
            executable = install_dir + '/' + 'unins000.exe'
            self.runner.run(executable)
            app.set_installed(False)
            self.repo.update_app(app)


class CommandRunner():
    def __init__(self):
        self.dir = ''

    def run(self, installer, install_dir=None):
        if sys.platform == 'win32':
            default_params = [installer, '/VERYSILENT']
            if install_dir:
                default_params.append('/DIR=' + install_dir)
                run(default_params)
            else:
                run(default_params)
