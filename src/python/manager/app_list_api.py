# external
from flask import jsonify
from flask_restful import Resource

# internal
from src.python.repository.app_repo import AppRepository


class AppListAPI(Resource):
    def __init__(self, repo=None):
        if not repo:
            self.repo = AppRepository()
        else:
            self.repo = repo

    def get(self):
        apps = self.repo.load_apps()
        return jsonify(apps)

    def delete(self):
        self.repo.remove_apps()

        return None, 204
