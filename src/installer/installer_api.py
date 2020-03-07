# external
from typing import Tuple
from flask_restful import Resource

# internal
from src.installer.app_installer import ApplicationInstaller


class AppInstallAPI(Resource):
    def __init__(self, installer: ApplicationInstaller = None):
        if not installer:
            self.installer = ApplicationInstaller()
        else:
            self.installer = installer

    def post(self, app_id) -> Tuple[None, int]:
        self.installer.install(app_id)
        return None, 204

    def delete(self, app_id) -> Tuple[None, int]:
        self.installer.uninstall(app_id)
        return None, 204
