# external
from flask_restful import Resource

# internal
from model.application import ApplicationEncoder
from repository.app_repo import AppRepository


class AppListAPI(Resource):
    def __init__(self, encoder=None, repo=None):
        if not encoder:
            self.encoder = ApplicationEncoder()
        else:
            self.encoder = encoder

        if not repo:
            self.repo = AppRepository()
        else:
            self.repo = repo

    def get(self):
        apps = self.repo.load_apps()

        output = []
        for app in apps:
            encoded = self.encoder.encode(app)
            output.append(encoded)

        return output, 200

    def delete(self):
        self.repo.remove_apps()

        return None, 204
