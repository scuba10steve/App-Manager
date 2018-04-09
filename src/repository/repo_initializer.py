from src.repository.app_repo import AppRepository


class AppRepositoryInitializer(AppRepository):
    def __init__(self, encoder=None, decoder=None, repo_name=None):
        super().__init__(encoder, decoder, repo_name)
        self.tables = ['APPS']

    def tables_exist(self):
        connection = super().connect()
        rows = connection.execute("""SELECT name FROM sqlite_master WHERE type='table';""")

        for row in rows:
            if row['name'] in self.tables:
                print('DB already initialized')
                return True

        connection.close()

        return False


    def initialize(self):
        if not self.tables_exist():
            connection = super().connect()
            apps_table = '''
            CREATE TABLE `APPS` 
            ( 
                `ID` INTEGER, 
                `NAME` TEXT,
                `SOURCE_URL` TEXT,
                `SYSTEM` TEXT,
                'INSTALLED' TEXT,
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

            # manager_metadata = '''
            # CREATE TABLE `METADATA`
            # (
            #     `SYSTEM` TEXT,
            #     `PK_MANAGER` TEXT,
            # )
            # '''
            connection.close()
