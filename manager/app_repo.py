from model.application import Application, ApplicationEncoder, ApplicationDecoder
import os.path
import json

APP_REPOSITORY_FILENAME = 'apps.json'

def store_app(app):
    if type(app) != Application:
        raise TypeError('Invalid type for "app": {}'.format(app))

    repo_file = None
    apps = load_apps()

    repo_file = open(APP_REPOSITORY_FILENAME, 'w')
    
    apps.append(app)

    encoder = ApplicationEncoder()

    clist = []

    for item in apps:
        j_string = encoder.encode(item)
        clist.append(j_string)

    repo_file.write(json.dumps(clist, ensure_ascii=False).replace('\"', '"'))


def load_apps():
    apps = []
    if not os.path.isfile(APP_REPOSITORY_FILENAME):
        return apps

    if os.path.getsize(APP_REPOSITORY_FILENAME) > 0:
        repo_file = open(APP_REPOSITORY_FILENAME, 'r')
        for item in json.load(repo_file):
            apps.append(ApplicationDecoder().decode(item))

    return apps


def load_app(app_name):
    apps = load_apps()
    for app in apps:
        if app.name == app_name:
            return app

    return None



def remove_apps():
    if not os.path.isfile(APP_REPOSITORY_FILENAME):
        return
    os.remove(APP_REPOSITORY_FILENAME)
