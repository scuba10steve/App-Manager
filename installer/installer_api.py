# external
from flask_restful import Resource

# internal
from installer.app_installer import ApplicationInstaller


class AppInstallAPI(Resource):

    def __init__(self):
        self.installer = ApplicationInstaller()

    def post(self, app_id):
        self.installer.install(app_id)
        return None, 204

    def delete(self, app_id):
        self.installer.uninstall(app_id)
        return None, 204
