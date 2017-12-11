#external
import os
from flask import Flask
from flask_restful import Api

#internal
from manager.app_manager import AppAPI, AppRegisterAPI, AppListAPI
from installer.installer_api import AppInstallAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(AppInstallAPI, '/app/<int:app_id>/install', endpoint='app_install')
api.add_resource(AppAPI, '/app/<int:app_id>', endpoint='app_inquiry_update_delete')
api.add_resource(AppRegisterAPI, '/app', endpoint='app_registration')
api.add_resource(AppListAPI, '/apps', endpoint='app_query')

p = None
try:
    p = os.environ['PORT']
except KeyError:
    p = "8080"


if __name__ == "__main__" and p:
    app.run(port=p)
elif __name__ == "__main__":
    app.run()