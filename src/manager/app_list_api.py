# external
from typing import List, Tuple

from flask import jsonify
from flask_restful import Resource

# internal
from src.model.application import Application
from src.repository.app_repo import AppRepository


class AppListAPI(Resource):
    def __init__(self, repo: AppRepository = None):
        if not repo:
            self.repo = AppRepository()
        else:
            self.repo = repo

    def get(self) -> List[Application]:
        apps = self.repo.load_apps()
        return jsonify(apps)

    def delete(self) -> Tuple[None, int]:
        self.repo.remove_apps()

        return None, 204
