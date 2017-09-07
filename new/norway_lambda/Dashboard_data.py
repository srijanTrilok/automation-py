import pandas as pd
import config
from sqlalchemy import create_engine
import numpy as np

def file_process(event):
    
    engine = create_engine('%s://%s:%s@%s:%s/%s' % (config.db_driver, config.db_user, config.db_pass, config.db_host, config.db_port, config.db_name))
    #q = 'select a.*, b.*, a.machine_type as Model, b."FakeCountry" as "Country", b."SiteName1" as "SiteName" from machine_lookup a, "iss_usage_2012_q1" b where a.machine_type = b.machine_name_matched;'
    q = 'SELECT a.*, b.*, c.* FROM (iss_usage_2012_q1 a LEFT JOIN tableau b ON a."FakeCountry" = b."Country" AND a."MachineNumber" = b."MachineNumber" AND a."SiteId" = b."SiteId") LEFT JOIN machines c ON b."SiteName" = c."name" AND b."machine_type" = c."type of machine"'
    print "processing file"
    
    d = pd.read_sql(q, con=engine)
    del d['index']
    '''data = d
    data['weekly cleaning frequency'] = d['weekly cleaning frequency'].fillna(0)
    data['calculated time machine cleaning'] = d['calculated time machine cleaning'].fillna(0)
    data['area suitable for machine cleaning'] = d['area suitable for machine cleaning'].fillna(0)
    data['iss department'] = d['iss department'].fillna(0)'''

    d[['weekly cleaning frequency', 'calculated time machine cleaning', 'area suitable for machine cleaning', 'iss department']] = d[['weekly cleaning frequency', 'calculated time machine cleaning', 'area suitable for machine cleaning', 'iss department']].fillna(value=0)
    d.to_sql('tableau_norway', con=engine, schema='public', if_exists='replace', chunksize=1000)
    print "done"
    return True

        

