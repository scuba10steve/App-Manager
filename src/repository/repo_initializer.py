from sqlite3 import Connection

from .app_repo import AppRepository


class AppRepositoryInitializer(AppRepository):
    def __init__(self, encoder=None, decoder=None, repo_name=None):
        super().__init__(encoder, decoder, repo_name)
        self.tables = ['APPS', 'SYSTEM_METADATA']

    def __tables_exist(self, connection: Connection):
        rows = connection.execute("""SELECT name FROM sqlite_master WHERE type='table';""")

        existing_tables = []
        for row in rows:
            existing_tables.append(row['name'])

        missing_tables = []
        if len(existing_tables) < len(self.tables):
            for table in self.tables:
                if table not in existing_tables:
                    print("Table: " + table + " not initialized!")
                    missing_tables.append(table)

            connection.commit()
            return False, missing_tables

        print("DB Already initialized...")
        return True, missing_tables

    def initialize(self):
        connection = super().connect()
        tables_exist, missing_tables = self.__tables_exist(connection)
        if not tables_exist:
            if 'APPS' in missing_tables:
                apps_table = '''
                CREATE TABLE `APPS` 
                ( 
                    `ID` INTEGER, 
                    `NAME` TEXT,
                    `SOURCE_URL` TEXT,
                    `SYSTEM` TEXT,
                    'INSTALLED' TEXT,
                    'PACKAGE' TEXT,
                    PRIMARY KEY(`ID`)
                )'''

                connection.execute(apps_table)
                connection.commit()

                index_default = '''
                CREATE INDEX `IDX_DEFAULT` ON `APPS` (
                    `NAME`,
                    `SYSTEM`,
                    `SOURCE_URL`
                );'''

                connection.execute(index_default)
                connection.commit()

                installed_index = '''
                CREATE INDEX 'IDX_INSTALLED' ON 'APPS' (
                    'INSTALLED'
                )
                '''

                connection.execute(installed_index)
                connection.commit()

            if 'SYSTEM_METADATA' in missing_tables:
                manager_metadata = '''
                CREATE TABLE `SYSTEM_METADATA`
                (
                    `SYS_ID` TEXT,
                    'SYS_VERSION' TEXT,
                    `PK_MANAGER` TEXT
                )
                '''

                connection.execute(manager_metadata)
                connection.commit()

            connection.close()
    # pylint: disable=invalid-name
    def store_sys_metadata(self, os: str, os_version: str, package_mgr: str):
        connection = super().connect()

        rows = connection.execute('SELECT 1 FROM SYSTEM_METADATA WHERE SYS_ID = ?', (os,))
        if rows and not rows.fetchone():
            connection.execute('INSERT INTO SYSTEM_METADATA(SYS_ID, SYS_VERSION, PK_MANAGER) VALUES (?, ?, ?)',
                               (os, os_version, package_mgr))
        connection.commit()
        connection.close()
