import os
import pandas as pd
import boto3
import urllib
from sqlalchemy import create_engine
from sqlalchemy import types
from .. import config

s3 = boto3.client('s3')


def file_process(event):
    bucket_name = config.s3bucket
    for file_obj in event['Records']:
        cols = ['MachineNumber', 'MachineTypDesignation', 'Date', 'Hours', 'CustomerId', 'SiteId',
                'SiteNumber', 'SiteName1', 'FakeCountry']
        ###MACHINE TYPE CLEANING
        #read all data
        '''raw = pd.read_csv('/srv/s3_bucket/ISS Decision Sciences/raw.tsv', sep='\t', error_bad_lines=False,
                          usecols = cols)
        csv_path = os.path.dirname(os.path.realpath(__file__)) + "/../../tsv/raw-Table.csv"'''
        filename = urllib.unquote_plus(file_obj['s3']['object']['key'].encode("utf8"))
        fileObj = s3.get_object(Bucket = bucket_name, Key = filename)

        raw = pd.read_csv(fileObj['Body'], sep=',', error_bad_lines=False,
                          usecols = cols)



        raw['MachineNumber'] = [uidFixer(x) for x in raw.MachineNumber]
        raw['Date'] = pd.to_datetime(raw.Date)

        raw['MachineNameTemp'] = [x.lower()  for x in raw['MachineTypDesignation']]
        raw['MachineNameTemp'] = [x.replace("taski", "") for x in raw['MachineNameTemp']]
        raw['MachineNameTemp'] = [x.lstrip() for x in raw['MachineNameTemp']]
        raw['machine_name_matched'] = ''

        i = raw.loc[raw.FakeCountry=='Global'].index.tolist()
        raw.set_value(i, col='FakeCountry', value='USA')

        """engine = create_engine('postgresql://w08459:Div123456!@datascience-dev.cy59ywvtinrm.eu-west-1.rds.amazonaws.com:5432'
                               '/datasciencedb')"""
        engine = create_engine('postgresql://automation:automation@automation.cxesxp0yaizx.us-east-1.rds.amazonaws.com:5432'
                               '/automation')

        q = "select * from machine_lookup"
        lookup = pd.read_sql(q, con=engine)


        from numpy import argmax
        import difflib

        for index, row in raw.iterrows():
            distance = [difflib.SequenceMatcher(None, x,row.MachineNameTemp).ratio() for x in lookup.machine_type]
            if max(distance) > 0.6:
                raw.set_value(index, col='machine_name_matched', value=lookup['machine_type'][argmax(distance)])
            else:
                pass

        del raw['MachineNameTemp']
        from datetime import datetime
        print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        raw.to_sql('iss_usage_2012_q1', con=engine, schema='public', if_exists='replace', chunksize=100,
                   dtype={'MachineNumber':types.VARCHAR,
                          'MachineTypDesignation':types.VARCHAR,
                          'Date':types.DATE,
                          'Hours':types.FLOAT,
                          'CustomerId':types.VARCHAR,
                          'SiteId':types.VARCHAR,
                          'SiteNumber':types.VARCHAR,
                          'SiteName1':types.VARCHAR,
                          'FakeCountry':types.VARCHAR,
                          'machine_name_matched':types.VARCHAR
                          })
        print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return True

def uidFixer(x):
    try:
        o = str(int(float(x)))
    except:
        o = str(x)
    return(o)
