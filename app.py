# external
import os

from flask import Flask, url_for, redirect
from flask_restful import Api

# internal
from src.installer import ApplicationDownloader, ApplicationInstaller, AppInstallAPI
from src.manager import AppRegisterAPI, AppAPI, AppListAPI
from src.model import ApplicationEncoder, ApplicationDecoder
from src.repository import AppRepositoryInitializer, AppRepository


# Global dependency injection
ENCODER = ApplicationEncoder()
DECODER = ApplicationDecoder()
REPO = AppRepository(ENCODER, DECODER)
DOWNLOADER = ApplicationDownloader()
INSTALLER = ApplicationInstaller(REPO, DOWNLOADER)


def main(port=5000):
    initialize_app()
    initialize_api(API)
    APP.run(port=port)


def initialize_app():
    print("Initializing...")
    repo_init = AppRepositoryInitializer(ENCODER, DECODER)
    repo_init.initialize()
    APP.json_encoder = ApplicationEncoder


def initialize_api(api):
    api.add_resource(AppInstallAPI, '/app/<int:app_id>/install', endpoint='app_install', resource_class_kwargs={'installer': INSTALLER})
    api.add_resource(AppAPI, '/app/<int:app_id>', endpoint='app_inquiry_update_delete', resource_class_kwargs={'repo': REPO})
    api.add_resource(AppRegisterAPI, '/app', endpoint='app_registration', resource_class_kwargs={'repo': REPO})
    api.add_resource(AppListAPI, '/apps', endpoint='app_query', resource_class_kwargs={'repo': REPO})


APP = Flask(__name__)
API = Api(APP)


@APP.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))


PORT = None
try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = 8080

if __name__ == "__main__" and PORT:
    main(PORT)
elif __name__ == "__main__":
    main()
