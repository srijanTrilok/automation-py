from pydal import DAL, Field
from .. import config

class DBConnection(object):

    db = ''
    algos_table = ''

    def __init__(self, tableName, columnData):
        # only if conn is not defined
        if self.db is not None:
            print "connection initiate"
            #migrate is set to true to create the table in the db
            self.db = DAL(self.get_dbconn_string(), pool_size=0, migrate=True, migrate_enabled = True, ignore_field_case=True, attempts=1, folder = '/tmp')
            # define table schema
            
            #fields=[Field('addr%02i' %i,'string') for i in range(25)]
            #print fields
            #creates a table

            fields = [Field(items['name'], items['type']) for items in columnData]
            self.algos_table = self.db.define_table(tableName, *fields, migrate = True, redefine = True)
            
    
    def get_algos_table(self):
        return self.algos_table

    def bulk_insert_data(self, rowData, tableName):
        self.algos_table.bulk_insert(rowData)
        self.db.commit()
        return True

    def execute_sql(self, sql):
        return self.db.executesql(sql)    

    def get_dbconn_string(self):
        conn_string = ""
        if(config.db_driver):
            conn_string = config.db_driver + "://"
        if (config.db_user):
            conn_string += config.db_user + ":"
        if (config.db_pass):
            conn_string += config.db_pass + "@"
        if (config.db_host):
            conn_string += config.db_host + "/"
        if (config.db_name):
            conn_string += config.db_name

        return conn_string
       

    def close_the_connection(self):
        if self.db: 
            print "close the conn"
            self.db.close()

