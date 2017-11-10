from model import application
import os.path

APP_REPOSITORY_FILENAME = 'apps.json'

def store_app(app):
    if type(app) != application.Application:
        raise TypeError('Invalid type for "app": {}'.format(app))

    repo_file = None
    apps = []

    if not os.path.isfile(APP_REPOSITORY_FILENAME):
        repo_file = open(APP_REPOSITORY_FILENAME, 'w')
    else:
        apps.append(app)


    encoder = application.ApplicationEncoder()

    repo_file.write(encoder.encode(app))

