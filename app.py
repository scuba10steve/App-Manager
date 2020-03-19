# external
import os

from flask import Flask, url_for, redirect
from flask_restful import Api

# internal
from src.installer.app_installer import ApplicationDownloader, ApplicationInstaller
from src.installer.installer_api import AppInstallAPI
from src.manager.app_api import AppRegisterAPI, AppAPI
from src.manager.app_initializer import ApplicationInitializer
from src.manager.app_list_api import AppListAPI
from src.model.application import ApplicationEncoder, ApplicationDecoder
from src.repository.app_repo import AppRepository
from src.repository.repo_initializer import AppRepositoryInitializer


# Global dependency injection
ENCODER = ApplicationEncoder()
DECODER = ApplicationDecoder()
REPO = AppRepository(ENCODER, DECODER)
DOWNLOADER = ApplicationDownloader()
REPO_INITIALIZER = AppRepositoryInitializer(ENCODER, DECODER)
APP_INITIALIZER = ApplicationInitializer(REPO_INITIALIZER)
INSTALLER = ApplicationInstaller(REPO, DOWNLOADER, APP_INITIALIZER)


def main():
    try:
        port = os.environ['PORT']
    except KeyError:
        port = 8080

    app = Flask(__name__)
    api = Api(app)
    initialize_app(app)
    initialize_api(api)

    # pylint: disable=unused-variable
    @app.route('/')
    def index():
        return redirect(url_for('static', filename='index.html'))

    app.run(port=port)

    return app


def initialize_app(app):
    print("Initializing...")
    REPO_INITIALIZER.initialize()
    APP_INITIALIZER.initialize()
    app.json_encoder = ApplicationEncoder


def initialize_api(api):
    api.add_resource(AppInstallAPI, '/app/<int:app_id>/install', endpoint='app_install', resource_class_kwargs={'installer': INSTALLER})
    api.add_resource(AppAPI, '/app/<int:app_id>', endpoint='app_inquiry_update_delete', resource_class_kwargs={'repo': REPO})
    api.add_resource(AppRegisterAPI, '/app', '/app/<int:app_id>', endpoint='app_registration', resource_class_kwargs={'repo': REPO})
    api.add_resource(AppListAPI, '/apps', endpoint='app_query', resource_class_kwargs={'repo': REPO})


if __name__ == "__main__":
    main()
