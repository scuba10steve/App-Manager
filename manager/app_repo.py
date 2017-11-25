from model.application import Application, ApplicationEncoder, ApplicationDecoder
import os.path
import json

class AppRepository():
    def __init__(self):
        self.APP_REPOSITORY_FILENAME = 'apps.json'
        self.encoder = ApplicationEncoder()
        self.decoder = ApplicationDecoder()

    def store_app(self, app):
        if type(app) != Application:
            raise TypeError('Invalid type for "app": {}'.format(app))

        repo_file = None
        apps = self.load_apps()

        repo_file = open(self.APP_REPOSITORY_FILENAME, 'w')
        
        apps.append(app)

        clist = []

        for item in apps:
            j_string = self.encoder.encode(item)
            clist.append(j_string)

        repo_file.write(json.dumps(clist, ensure_ascii=False).replace('\"', '"'))


    def load_apps(self):
        apps = []
        if not os.path.isfile(self.APP_REPOSITORY_FILENAME):
            return apps

        if os.path.getsize(self.APP_REPOSITORY_FILENAME) > 0:
            repo_file = open(self.APP_REPOSITORY_FILENAME, 'r')
            for item in json.load(repo_file):
                apps.append(self.decoder.decode(item))

        return apps


    def load_app(self,app_name):
        apps = self.load_apps()
        for app in apps:
            if app.name == app_name:
                return app

        return None


    def remove_apps(self):
        if not os.path.isfile(self.APP_REPOSITORY_FILENAME):
            return
        os.remove(self.APP_REPOSITORY_FILENAME)
