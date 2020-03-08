# external
from flask import jsonify
from flask_restful import Resource, reqparse, abort

# internal
from src.manager.validator.input_validator import Validator
from src.model.application import Application
from src.repository.app_repo import AppRepository


# Works with getting/updating/deleting only one app at a time
class AppAPI(Resource):
    def __init__(self, repo: AppRepository = None, validator: Validator = None):
        self.parser = reqparse.RequestParser()

        if repo:
            self.repo = repo
        else:
            self.repo = AppRepository()

        if validator:
            self.validator = validator
        else:
            self.validator = Validator()

        self.parser.add_argument('source_url', type=str, location='json')
        self.parser.add_argument('system', type=str, location='json')
        self.parser.add_argument('name', type=str, location='json')
        super(AppAPI, self).__init__()

    def get(self, app_id):
        app = self.repo.load_app(app_id)
        if app:
            return jsonify(app)
        abort(404)

    def put(self, app_id):
        data = self.parser.parse_args()
        source_url = data['source_url']
        self.validator.validate_url(source_url)

        system = data['system']
        self.validator.validate_sys(system)

        name = data['name']

        app = self.repo.load_app(app_id)
        if app:
            app.set_source_url(source_url)
            app.set_system(system)
            app.set_name(name)
            return jsonify(app)
        abort(404)


# Only allows posting of a new app
class AppRegisterAPI(Resource):
    def __init__(self, repo: AppRepository = None, validator: Validator = None):
        self.parser = reqparse.RequestParser()

        if repo:
            self.repo = repo
        else:
            self.repo = AppRepository()

        if validator:
            self.validator = validator
        else:
            self.validator = Validator()

        self.parser.add_argument('source_url', type=str, location='json')
        self.parser.add_argument('system', type=str, location='json')
        self.parser.add_argument('name', type=str, location='json')
        super(AppRegisterAPI, self).__init__()

    def post(self):
        data = self.parser.parse_args()
        app_id = 0
        if data:
            source_url = data['source_url']
            self.validator.validate_url(source_url)

            system = data['system']
            self.validator.validate_sys(system)

            name = data['name']

            new_app = Application(name, source_url, system)

            app_id = self.repo.store_app(new_app)

        return jsonify({'resource_uri': "/app/{}".format(app_id)})
