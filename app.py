from flask import Flask, request
from model import application
from manager import app_repo
from manager.validator import input_validator
import json


app = Flask(__name__)

@app.route('/')
def root():
    return "Hello World!"

# Register a new resource for the app to manage
@app.route('/app/register/<app_name>', methods=['POST'])
def register(app_name):
    new_app = None
    if request.data and app_name:
        source_url = json.loads(request.data)['sourceUrl']
        input_validator.validate(source_url)
        new_app = application.Application(app_name, source_url)

        app_repo.store_app(new_app)

    return json.dumps(application.ApplicationEncoder().encode(new_app))


if __name__ == "__main__":
    app.run()