from sqlalchemy import create_engine, MetaData
#from sqlalchemy import create_engine, Column, Integer, String, Sequence, MetaData, ForeignKey
import pandas as pd
import os
import config

def import_db():

    csv_path = os.path.dirname(os.path.realpath(__file__)) + "/Machines.csv"
    #table_name = config.table_name
    table_name = 'machines'
    
    """engine = create_engine('%s://%s:%s@localhost:%s/%s' % (config.db_driver, config.db_user, config.db_pass,
                                                           config.db_port, config.db_name))"""
    engine = create_engine('postgresql://automation:automation@automation.cxesxp0yaizx.us-east-1.rds.amazonaws.com:5432/automation')   
    df = pd.read_csv("%s" % (csv_path))
    df.columns = map(str.lower, df.columns)
    #print type(df.columns)
    df.columns = map(str.strip, df.columns)
    df.to_sql(name=table_name, con=engine, if_exists='replace') # if there is some error in csv file this will not import any data


import_db()
	