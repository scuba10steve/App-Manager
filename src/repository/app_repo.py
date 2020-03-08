#external
import os.path
import sqlite3

# internal
from typing import Union, List

from src.model.application import Application, ApplicationDecoder, ApplicationEncoder


class AppRepository:
    def __init__(self, encoder: ApplicationEncoder = None, decoder: ApplicationDecoder = None, repo_name: str = None):
        if not repo_name:
            self.repo_name = 'apps.db'
        else:
            self.repo_name = repo_name

        if not encoder:
            self.encoder = ApplicationEncoder()
        else:
            self.encoder = encoder

        if not decoder:
            self.decoder = ApplicationDecoder()
        else:
            self.decoder = decoder

    def store_app(self, app: Application) -> str:
        if not isinstance(app, Application):
            raise TypeError('Invalid type for "app": {}'.format(app))

        connection = self.connect()

        existing_app_row = connection.execute(
            'SELECT ID FROM APPS WHERE NAME = ? AND SYSTEM = ? AND PACKAGE = ?', (app.get_name(), app.get_system(), app.get_is_package()))
        if existing_app_row:
            existing_app = existing_app_row.fetchone()
            if existing_app:
                app_id = existing_app['ID']
                connection.close()
                return app_id

        connection.execute('INSERT INTO APPS(NAME, SOURCE_URL, SYSTEM, INSTALLED, PACKAGE) VALUES (?, ?, ?, \'False\', ?)',
                           (app.get_name(), app.get_source_url(), app.get_system(), app.get_is_package()))
        connection.commit()

        result = connection.execute('SELECT ID FROM APPS WHERE NAME = ? AND SYSTEM = ? AND PACKAGE = ?', (
            app.get_name(), app.get_system(), app.get_is_package()))
        app_id = result.fetchone()['ID']

        connection.close()

        return app_id

    def load_apps(self) -> List[Application]:
        apps = []
        if not self.does_repo_exist():
            return apps

        connection = self.connect()

        rows = connection.execute(
            'SELECT ID, NAME, SOURCE_URL, SYSTEM, INSTALLED FROM APPS')

        for row in rows:
            app = Application(row['NAME'], row['SOURCE_URL'], row['SYSTEM'],
                              row['ID'], installed=(row['INSTALLED'] == 'True'))
            apps.append(app)

        connection.close()

        return apps

    def load_app(self, app_id: str) -> Union[None, Application]:
        connection = self.connect()
        result = connection.execute(
            'SELECT ID, NAME, SOURCE_URL, SYSTEM, INSTALLED, PACKAGE FROM APPS WHERE ID = ?', (app_id,))

        app = None

        if result:
            cols = result.fetchone()
            if cols:
                app = Application(cols['NAME'], cols['SOURCE_URL'], cols['SYSTEM'], cols['ID'],
                                  installed=(cols['INSTALLED'] == 'True'), is_package=(cols['PACKAGE'] == 'True'))

        connection.close()

        return app

    def remove_app(self, app_id: str):
        connection = self.connect()
        connection.execute('DELETE FROM APPS WHERE ID = ?', (app_id,))
        connection.commit()
        connection.close()

    def remove_apps(self):
        if not self.does_repo_exist():
            return

        connection = self.connect()

        connection.execute('DELETE FROM APPS')

        connection.commit()
        connection.close()

    def update_app(self, app: Application):
        if not isinstance(app, Application):
            raise TypeError("Invalid type for app")

        existing_app = self.load_app(app.get_app_id())

        if app != existing_app and existing_app:
            # Update the app
            connection = self.connect()
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
                               (app.get_name(), app.get_system(), app.get_source_url(), str(app.is_installed()), app.get_app_id()))

            connection.commit()
            connection.close()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.repo_name)
        connection.row_factory = sqlite3.Row

        return connection

    def get_repo_name(self) -> str:
        return self.repo_name

    def does_repo_exist(self) -> bool:
        return (self.repo_name == ':memory:') or (os.path.isfile(self.repo_name))
