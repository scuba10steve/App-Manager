from flask import jsonify
from flask_restful import Resource, fields, reqparse 
from manager.validator.input_validator import Validator
from model.application import Application, ApplicationEncoder, ApplicationDecoder
from manager.app_repo import AppRepository

class AppRegistrationAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.encoder = ApplicationEncoder()
        self.validator = Validator()
        self.repo = AppRepository()
        self.parser.add_argument('sourceUrl', type=str, location='json')
        self.parser.add_argument('system', type=str, location='json')
        super(AppRegistrationAPI, self).__init__()

    def get(self, app_name):
        app = self.repo.load_app(app_name)
        return jsonify({'app' : self.encoder.encode(app)})

    def post(self, app_name):
        new_app = None
        data = self.parser.parse_args()
        if data and app_name:

            sourceUrl = data['sourceUrl']
            self.validator.validate_url(sourceUrl)

            system = data['system']
            self.validator.validate_sys(system)

            new_app = Application(app_name, sourceUrl, system)

            self.repo.store_app(new_app)

        return jsonify({'resource_uri': "/app/{}".format(app_name)})


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
        
        return jsonify({'apps': output})

    def delete(self):
        self.repo.remove_apps()
        return jsonify()