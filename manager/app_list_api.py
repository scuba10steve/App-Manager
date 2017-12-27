# external
from flask import jsonify
from flask_restful import Resource

# internal
from model.application import ApplicationEncoder
from repository.app_repo import AppRepository


class AppListAPI(Resource):
    def __init__(self):
        self.encoder = ApplicationEncoder()
        self.repo = AppRepository()

    def get(self):
        apps = self.repo.load_apps()

        output = []
        for app in apps:
            encoded = self.encoder.encode(app)
            output.append(encoded)

        return jsonify(output)

    def delete(self):
        self.repo.remove_apps()
        return jsonify()
