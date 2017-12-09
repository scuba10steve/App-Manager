from flask import jsonify
from flask_restful import Resource, fields, reqparse 
from manager.validator.input_validator import Validator
from model.application import Application, ApplicationEncoder, ApplicationDecoder
from manager.app_repo import AppRepository

#Works with getting/updating/deleting only one app at a time
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


#Only allows posting of a new app
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
            sourceUrl = data['sourceUrl']
            self.validator.validate_url(sourceUrl)

            system = data['system']
            self.validator.validate_sys(system)

            name = data['name']

            new_app = Application(name, sourceUrl, system)

            app_id = self.repo.store_app(new_app)

        return jsonify({'resource_uri': "/app/{}".format(app_id)})


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