from model.application import Application, ApplicationEncoder, ApplicationDecoder
import os.path
import json
import sqlite3

class AppRepository():
    def __init__(self):
        self.repo_name = 'apps.db'
        self.encoder = ApplicationEncoder()
        self.decoder = ApplicationDecoder()
    

    def store_app(self, app):
        if type(app) != Application:
            raise TypeError('Invalid type for "app": {}'.format(app))

        connection = self.connect()

        existing_app_row = connection.execute('SELECT ID FROM APPS WHERE NAME = ? AND SYSTEM = ?', (app.get_name(), app.get_system()))
        if existing_app_row:
            existing_app = existing_app_row.fetchone()
            if existing_app:
                app_id = existing_app['ID']
                connection.close()
                return app_id


        connection.execute('INSERT INTO APPS(NAME, SOURCE_URL, SYSTEM) VALUES (?, ?, ?)', (app.get_name(), app.get_sourceUrl(), app.get_system()))
        connection.commit()

        result = connection.execute('SELECT ID FROM APPS WHERE NAME = ? AND SYSTEM = ? AND SOURCE_URL = ?', (app.get_name(), app.get_system(), app.get_sourceUrl(),))
        app_id = result.fetchone()['ID']
        
        connection.close()

        return app_id


    def load_apps(self):
        apps = []
        if not os.path.isfile(self.repo_name):
            return apps

        connection = self.connect()

        rows = connection.execute('SELECT ID, NAME, SOURCE_URL, SYSTEM FROM APPS')

        for row in rows:
            app = Application(row['NAME'], row['SOURCE_URL'], row['SYSTEM'], row['ID'])
            apps.append(app)

        connection.close()

        return apps


    def load_app(self, app_id):
        connection = self.connect()
        result = connection.execute('SELECT ID, NAME, SOURCE_URL, SYSTEM FROM APPS WHERE ID = ?', (app_id,))
        
        app = None

        if result:
            cols = result.fetchone()
            app = Application(cols['NAME'], cols['SOURCE_URL'], cols['SYSTEM'], cols['ID'])
            
        connection.close()
        
        return app

    def remove_apps(self):
        if not os.path.isfile(self.repo_name):
            return
        os.remove(self.repo_name)

    
    def connect(self):
        connection = sqlite3.connect(self.repo_name)
        connection.row_factory = sqlite3.Row

        return connection



class AppRepositoryInitializer(AppRepository):
    def __init__(self):
        super().__init__()

    
    def initialize(self):
        connection = self.connect()
        table = '''CREATE TABLE `APPS` 
        ( `ID` INTEGER, `NAME` TEXT, `SOURCE_URL` TEXT, `SYSTEM` TEXT, PRIMARY KEY(`ID`) )'''

        connection.execute(table)
        connection.commit(table)
        index = '''CREATE INDEX `IDX_DEFAULT` ON `APPS` (
                    `NAME`,
                    `SYSTEM`,
                    `SOURCE_URL`
                );'''
        connection.execute(index)
        connection.commit()
        connection.close()