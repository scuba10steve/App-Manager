#external
from flask import Flask
from flask_restful import Api
import os

#internal
from manager.app_manager import AppRegistrationAPI, AppListAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(AppRegistrationAPI, '/app/<app_name>', endpoint='app_registration')
api.add_resource(AppListAPI, '/apps', endpoint='app_query')

p = None
try:
    p = os.environ['PORT']
except KeyError:
    p = "8080"


if __name__ == "__main__" and p:
    app.run(port=p)
elif __name__ == "__main__":
    app.run()