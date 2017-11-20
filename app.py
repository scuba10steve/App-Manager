#external
from flask import Flask, request
import json

#internal
from model.application import Application, ApplicationEncoder
from manager import app_repo
from manager.validator import input_validator

app = Flask(__name__)

@app.route('/')
def root():
    return "Hello World!"

# Register a new resource for the app to manage
@app.route('/apps/register/<app_name>', methods=['POST'])
def register(app_name):
    new_app = None
    if request.data and app_name:
        data = json.loads(request.data)

        sourceUrl = data['sourceUrl']
        input_validator.validate_url(sourceUrl)

        system = data['system']
        input_validator.validate_sys(system)

        new_app = Application(app_name, sourceUrl, system)

        app_repo.store_app(new_app)

    return "/apps/{}".format(app_name), 201


@app.route('/apps/register', methods=['DELETE'])
def deregister_apps():
    app_repo.remove_apps()
    return "", 204

@app.route('/apps/<app_name>', methods=['GET'])
def get_app(app_name):
    app = app_repo.load_app(app_name)
    return json.dump(ApplicationEncoder().encode(app)), 200

@app.route('/apps', methods=['GET'])
def get_registered_apps():
    apps = app_repo.load_apps()

    output = []
    for app in apps:
        encoded = ApplicationEncoder().encode(app)
        output.append(encoded)
    
    return json.dump(output), 200

if __name__ == "__main__":
    app.run()