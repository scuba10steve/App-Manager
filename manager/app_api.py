# external
from flask import jsonify
from flask_restful import Resource, reqparse

# internal
from manager.validator.input_validator import Validator
from model.application import Application, ApplicationEncoder
from repository.app_repo import AppRepository

# Works with getting/updating/deleting only one app at a time


class AppAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.encoder = ApplicationEncoder()
        self.repo = AppRepository()
        self.parser.add_argument('sourceUrl', type=str, location='json')
        self.parser.add_argument('system', type=str, location='json')
        super(AppAPI, self).__init__()

    def get(self, app_id):
        app = self.repo.load_app(app_id)
        return jsonify(self.encoder.encode(app))


# Only allows posting of a new app
class AppRegisterAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.encoder = ApplicationEncoder()
        self.validator = Validator()
        self.repo = AppRepository()
        self.parser.add_argument('sourceUrl', type=str, location='json')
        self.parser.add_argument('system', type=str, location='json')
        self.parser.add_argument('name', type=str, location='json')
        super(AppRegisterAPI, self).__init__()

    def post(self):
        new_app = None
        data = self.parser.parse_args()
        if data:
            source_url = data['sourceUrl']
            self.validator.validate_url(source_url)

            system = data['system']
            self.validator.validate_sys(system)

            name = data['name']

            new_app = Application(name, source_url, system)

            app_id = self.repo.store_app(new_app)

        return jsonify({'resource_uri': "/app/{}".format(app_id)})
