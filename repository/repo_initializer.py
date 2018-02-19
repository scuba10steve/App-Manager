from repository.app_repo import AppRepository


class AppRepositoryInitializer(AppRepository):
    def __init__(self):
        super().__init__()
        self.TABLES = ['APPS']

    def tables_exist(self):
        connection = super().connect()
        rows = connection.execute("""SELECT name FROM sqlite_master WHERE type='table';""")

        for row in rows:
            if row['name'] in self.TABLES:
                print('DB already initialized')
                return True
        
        connection.close()

        return False


    def initialize(self):
        if not self.tables_exist():
            connection = super().connect()
            table = '''
            CREATE TABLE `APPS` 
            ( 
                `ID` INTEGER, 
                `NAME` TEXT,
                `SOURCE_URL` TEXT,
                `SYSTEM` TEXT,
                'INSTALLED' TEXT,
                PRIMARY KEY(`ID`)
            )'''

            connection.execute(table)
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

            connection.close()
