#external
import os

from flask import Flask
from flask_restful import Api

#internal
from manager.app_api import AppAPI, AppRegisterAPI
from manager.app_list_api import AppListAPI
from manager.app_initializer import ApplicationInitializer
from repository.repo_initializer import AppRepositoryInitializer
from repository.app_repo import AppRepository
from installer.app_installer import ApplicationInstaller, CommandRunner
from installer.app_downloader import ApplicationDownloader
from installer.installer_api import AppInstallAPI
from model.application import ApplicationEncoder, ApplicationDecoder


#Global dependency injection
ENCODER = ApplicationEncoder()
DECODER = ApplicationDecoder()
REPO = AppRepository(ENCODER, DECODER)
RUNNER = CommandRunner()
DOWNLOADER = ApplicationDownloader()
INSTALLER = ApplicationInstaller(REPO, RUNNER, DOWNLOADER)


def main(port=5000):
    initialize_app(APP)
    initialize_api(API)
    APP.run(port=port)


def initialize_app(app):
    print("Initializing...")
    repo_init = AppRepositoryInitializer()
    repo_init.initialize()
    app_init = ApplicationInitializer()
    app_init.determine_os()

def initialize_api(api):
    api.add_resource(AppInstallAPI, '/app/<int:app_id>/install', endpoint='app_install', resource_class_kwargs={'installer': INSTALLER})
    api.add_resource(AppAPI, '/app/<int:app_id>', endpoint='app_inquiry_update_delete', resource_class_kwargs={'encoder': ENCODER, 'repo': REPO})
    api.add_resource(AppRegisterAPI, '/app', endpoint='app_registration', resource_class_kwargs={'encoder': ENCODER, 'repo': REPO})
    api.add_resource(AppListAPI, '/apps', endpoint='app_query', resource_class_kwargs={'encoder': ENCODER, 'repo': REPO})


APP = Flask(__name__)
API = Api(APP)

PORT = None
try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = 8080

if __name__ == "__main__" and PORT:
    main(PORT)
elif __name__ == "__main__":
    main()
