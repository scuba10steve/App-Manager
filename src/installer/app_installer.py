# external
import os
import re
from urllib.parse import urlparse

# internal
from src.installer.factory.installer_factory import InstallerFactory


class ApplicationInstaller:
    def __init__(self, repo=None, downloader=None, factory=None):
        self.install_dir = './working/installation'
        self.repo = repo
        self.downloader = downloader
        self.factory = factory
        self.exec_pattern = r'.+\.exe'

    def install(self, app_id):
        app = self.repo.load_app(app_id)
        if not app:
            raise Exception("Unable to update app that doesn't exist yet")
        url = app.get_source_url()
        app_name = app.get_name()
        install_dir = self.install_dir + '/' + app_name

        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        # find the app extenstion
        url_path = urlparse(url)
        ext = os.path.basename(url_path.path)

        splitted = ext.split('.')

        if not (ext and len(splitted) > 1):
            # extension could not be determined
            ext = None
        else:
            ext = splitted[len(splitted) - 1]

        executable = self.downloader.download(url, app_name, ext)

        runner = InstallerFactory().with_extension(ext).find()

        if re.match(self.exec_pattern, executable) and runner:
            runner.run(executable, install_dir)

        app.set_installed(True)
        self.repo.update_app(app)

    def uninstall(self, app_id):
        app = self.repo.load_app(app_id)
        uninstaller, has_uninstaller = self.__discover_uninstaller(app.get_name())
        ext = self.__discover_uninstaller(app.get_name())
        runner = self.factory.with_extension(ext).find()
        if app.is_installed() and has_uninstaller and runner:
            runner.run(uninstaller)
            app.set_installed(False)
            self.repo.update_app(app)

    def __discover_uninstaller(self, app_name):
        install_dir = self.install_dir + '/' + app_name
        if os.path.exists(install_dir):
            for app_file in os.scandir(install_dir):
                if '.exe' in app_file.name:
                    return (app_file.path, True)

        return (None, False)
