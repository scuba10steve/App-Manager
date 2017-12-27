#external
import os.path
import sqlite3

#internal
from model.application import Application, ApplicationEncoder, ApplicationDecoder


class AppRepository():
    def __init__(self):
        self.repo_name = 'apps.db'
        self.encoder = ApplicationEncoder()
        self.decoder = ApplicationDecoder()

    def store_app(self, app):
        if isinstance(app) != Application:
            raise TypeError('Invalid type for "app": {}'.format(app))

        connection = self.__connect()

        existing_app_row = connection.execute(
            'SELECT ID FROM APPS WHERE NAME = ? AND SYSTEM = ?', (app.get_name(), app.get_system()))
        if existing_app_row:
            existing_app = existing_app_row.fetchone()
            if existing_app:
                app_id = existing_app['ID']
                connection.close()
                return app_id

        connection.execute('INSERT INTO APPS(NAME, SOURCE_URL, SYSTEM) VALUES (?, ?, ?)',
                           (app.get_name(), app.get_sourceUrl(), app.get_system()))
        connection.commit()

        result = connection.execute('SELECT ID FROM APPS WHERE NAME = ? AND SYSTEM = ? AND SOURCE_URL = ?', (
            app.get_name(), app.get_system(), app.get_sourceUrl(),))
        app_id = result.fetchone()['ID']

        connection.close()

        return app_id

    def load_apps(self):
        apps = []
        if not os.path.isfile(self.repo_name):
            return apps

        connection = self.__connect()

        rows = connection.execute(
            'SELECT ID, NAME, SOURCE_URL, SYSTEM, INSTALLED FROM APPS')

        for row in rows:
            app = Application(row['NAME'], row['SOURCE_URL'], row['SYSTEM'],
                              row['ID'], installed=(row['INSTALLED'] == 'True'))
            apps.append(app)

        connection.close()

        return apps

    def load_app(self, app_id):
        connection = self.__connect()
        result = connection.execute(
            'SELECT ID, NAME, SOURCE_URL, SYSTEM, INSTALLED FROM APPS WHERE ID = ?', (app_id,))

        app = None

        if result:
            cols = result.fetchone()
            app = Application(cols['NAME'], cols['SOURCE_URL'], cols['SYSTEM'],
                              cols['ID'], installed=(cols['INSTALLED'] == 'True'))

        connection.close()

        return app

    def remove_app(self, app_id):
        connection = self.__connect()
        connection.execute('DELETE FROM APPS WHERE ID = ?', (app_id))
        connection.commit()
        connection.close()

    def remove_apps(self):
        if not os.path.isfile(self.repo_name):
            return

        connection = self.__connect()

        connection.execute('DELETE * FROM APPS')

        connection.commit()
        connection.close()

    def update_app(self, app):
        if isinstance(app) != Application:
            raise TypeError("Invalid type for app: " + type(app))

        existing_app = self.load_app(app.get_app_id())

        if app == existing_app:
            return
        else:
            # Update the app
            connection = self.__connect()
            connection.execute('''
            UPDATE 
                APPS 
            SET 
                NAME = ?, 
                SYSTEM = ?, 
                SOURCE_URL = ?,
                INSTALLED = ? 
            WHERE 
                ID = ?''',
                               (app.get_name(), app.get_system(), app.get_sourceUrl(), str(app.is_installed()), app.get_app_id()))

            connection.commit()
            connection.close()

    def __connect(self):
        connection = sqlite3.connect(self.repo_name)
        connection.row_factory = sqlite3.Row

        return connection
