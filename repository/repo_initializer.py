from repository.app_repo import AppRepository

class AppRepositoryInitializer(AppRepository):
    def __init__(self):
        super().__init__()

    
    def initialize(self):
        connection = super().__connect()
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