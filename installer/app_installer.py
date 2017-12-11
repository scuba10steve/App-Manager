#external
import os
import sys
from subprocess import run

#internal
from repository.app_repo import AppRepository
from installer.app_downloader import ApplicationDownloader

class ApplicationInstaller(ApplicationDownloader):
    def __init__(self):
        self.install_dir = './installation'
        self.repo = AppRepository()
        self.runner = CommandRunner()
        super().__init__()
    

    def install(self, app_id):
        app = self.repo.load_app(app_id)
        if not app:
            raise Exception("Unable to update app that doesn't exist yet")
        url = app.get_sourceUrl()
        app_name = app.get_name()
        install_dir = self.install_dir + '/' + app_name

        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        f = self.download(url, app_name)

        self.runner.run(f, install_dir)
        
        app.set_installed(True)
        self.repo.update_app(app)


    def uninstall(self, app_id):
        app = self.repo.load_app(app_id)
        app_name = app.get_name()
        install_dir = self.install_dir + '/' + app_name
        if app.is_installed():
            f = install_dir + '/' + 'unins000.exe'
            self.runner.run(f)
            app.set_installed(False)
            self.repo.update_app(app)


class CommandRunner():
    def __init__(self):
        self.dir = ''

    
    def run(self, installer, install_dir=None):
        if (sys.platform == 'win32'):
            default_params = [installer, '/VERYSILENT']
            if install_dir:
                default_params.append('/DIR=' + install_dir)
                run(default_params)
            else:
                run(default_params)