#external
import os

from flask import Flask
from flask_restful import Api

from installer.installer_api import AppInstallAPI
#internal
from manager.app_api import AppAPI, AppRegisterAPI
from manager.app_list_api import AppListAPI

APP = Flask(__name__)
API = Api(APP)

API.add_resource(AppInstallAPI, '/app/<int:app_id>/install', endpoint='app_install')
API.add_resource(AppAPI, '/app/<int:app_id>', endpoint='app_inquiry_update_delete')
API.add_resource(AppRegisterAPI, '/app', endpoint='app_registration')
API.add_resource(AppListAPI, '/apps', endpoint='app_query')

PORT = None
try:
    PORT = os.environ['PORT']
except KeyError:
    PORT = "8080"


if __name__ == "__main__" and PORT:
    APP.run(port=PORT)
elif __name__ == "__main__":
    APP.run()
