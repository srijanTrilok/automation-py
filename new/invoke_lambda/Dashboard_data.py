import pandas as pd
import config
from sqlalchemy import create_engine
import numpy as np



'''engine = create_engine('postgresql://w08459:Div123456!@datascience-dev.cy59ywvtinrm.eu-west-1.rds.amazonaws.com:5432'
                       '/datasciencedb')'''
def file_process(event):
    '''engine = create_engine('postgresql://automation:automation@automation.cxesxp0yaizx.us-east-1.rds.amazonaws.com:5432'
                                   '/automation')'''
    engine = create_engine('%s://%s:%s@%s:%s/%s' % (config.db_driver, config.db_user, config.db_pass, config.db_host, config.db_port, config.db_name))

    q = 'select a.*, b.*, a.machine_type as Model, b."FakeCountry" as "Country", b."SiteName1" as "SiteName" from machine_lookup a, "iss_usage_2012_q1" b where a.machine_type = b.machine_name_matched;'

    d = pd.read_sql(q, con=engine)
    del d['index']

    d = d.loc[d.Hours>0]

    FE = d.drop_duplicates(subset='MachineNumber')
    FE.reset_index(inplace=True, drop=True)

    usageMedian = d.groupby(by='MachineNumber')['Hours'].median()*60

    #usage in min
    usageQ3 = d.groupby(by='MachineNumber')['Hours'].quantile(q=0.75)*60
    usageQ1 = d.groupby(by='MachineNumber')['Hours'].quantile(q=0.25)*60
    FE['usageMedian'] = list(usageMedian)
    FE['usageQ3'] = list(usageQ3)
    FE['usageQ1'] = list(usageQ1)

    dmax = d.Date.max()
    dmin = pd.date_range(end=dmax, periods=30).min().date()

    def asset_utilization(i):
        d0 = d.loc[d.MachineNumber == i]
        if d0.shape[0] > 1:
            ran = (d0.Date.max() - d0.Date.min()).days + 1
            ndays = len(d0.Date.unique())
            if (ndays > 0) & (ran > 0):
                return(ndays/ran)
            else:
                return(0)

    def unused(i):
        d0 = d.loc[d.MachineNumber == i]
        d0 = d0.loc[d0.Date > dmin]
        if d0.shape[0] == 0 or d0.Hours.sum() > 0.5:
            return(-999)
        else:
            return(0)

    for index, row in FE.iterrows():
        asu = asset_utilization(row.MachineNumber)
        FE.set_value(index, col='assetUti', value=asu)
        uu = unused(row.MachineNumber)
        if uu == -999:
            FE.set_value(index, col='unused', value='unused')
        else:
            FE.set_value(index, col='unused', value='used')

    key = FE.usageMedian>FE.overutilization
    FE = FE.set_value(index=key, col='utilization', value='over')

    key = FE.loc[FE.assetUti<0.30].index.tolist()
    FE = FE.set_value(index=key, col='utilization', value='under')

    relo = FE.loc[FE.utilization=='under'].MachineNumber.sample(frac=0.5)
    key = FE.loc[FE.MachineNumber.isin(relo)].index.tolist()
    FE['relocated'] = 0
    FE = FE.set_value(index=key, col='relocated', value=1)

    ################
    # # Criteria for recommendation
    # #The criteria defined below depends sometimes depends on the client, the geographical location, etc
    # #this first test does not take any of this into account and defines the criteria as machine only dependent
    # #1) Does the contract allow a machine switch (allowed to 40% of the clients)
    cid = pd.DataFrame(data={'cid':d.CustomerId.unique()})
    cid['contract'] = np.random.binomial(1,0.7,cid.shape[0])
    mid = d.loc[d.CustomerId.isin(cid.loc[cid.contract==1].cid)].MachineNumber.unique()
    key = FE.loc[FE.MachineNumber.isin(mid)].index.tolist()
    FE['contract'] = 0
    FE = FE.set_value(index=key, col='contract', value=1)

    #    #1.1) Is the re-negotiation cost low (or free)? (50% of customers whose contract doesn't allow switch
    # #  can switch for a low premium or for free)
    cid_yes = cid.loc[cid.contract==0].cid.sample(frac=0.7)
    mid = d.loc[d.CustomerId.isin(cid_yes)].MachineNumber.unique()
    key = FE.loc[FE.MachineNumber.isin(mid)].index.tolist()
    FE['cost_negot'] = 1
    FE = FE.set_value(index=key, col='cost_negot', value=0)

    #
    # #2) Is there a bigger/smaller machine available (per customer?)
    FE['other_available'] = np.random.binomial(1, 0.7, FE.shape[0])

    #
    # #3) Is there a substitute machine in the close proximity (per location?)
    FE['other_in_proximity'] = np.random.binomial(1, 0.6, FE.shape[0])

    #
    # #4) Does the machine fit within the doorways
    FE['bigger_fit_doors'] = np.random.binomial(1, 0.9, FE.shape[0])

    #
    # #5) Is the storage closet big enough
    FE['storage_closet'] = np.random.binomial(1, 0.9, FE.shape[0])

    #
    # #6) Can the operators use it without training?
    FE['skills_in_team'] = np.random.binomial(1,0.9,FE.shape[0])

    #
    FE['change_to'] = ''
    for index, row in FE.iterrows():
        k = (all(row[['contract', 'cost_negot', 'other_available', 'other_in_proximity',
         'bigger_fit_doors', 'storage_closet', 'skills_in_team']])==1)
        if (k and row.utilization=='under'):
            FE = FE.set_value(index=index, col='recommendation', value='downgrade')
            FE = FE.set_value(index=index, col='change_to', value='Downgrade to')
        elif (k and row.utilization=='over'):
            FE = FE.set_value(index=index, col='recommendation', value='upgrade')
            FE = FE.set_value(index=index, col='change_to', value='Upgrade to')
        else:
            FE = FE.set_value(index=index, col='change_to', value='No change possible')


    FE['upgrade_to'] = ''       
    for index, row in FE.iterrows():
        if row.recommendation == 'downgrade' and row.ordinal > 1:
            try:
                FE = FE.set_value(index=index, col='downgrade_to', value=FE.loc[FE.ordinal == (row.ordinal - 1)]['machine_name_matched'].unique()[0])
            except IndexError:
                FE = FE.set_value(index=index, col='downgrade_to', value='null')
        if row.recommendation == 'upgrade' and row.ordinal < FE.ordinal.max():
            FE = FE.set_value(index=index, col='upgrade_to', value=FE.loc[FE.ordinal == (row.ordinal + 1)]['machine_name_matched'].unique()[0])

    FE['reasons'] = ''
    for index, row in FE.iterrows():
        ss = pd.DataFrame(data={'items': row[['contract', 'cost_negot', 'other_available', 'other_in_proximity',
                                              'bigger_fit_doors', 'storage_closet', 'skills_in_team']]})
        lab = ss.loc[ss['items'] == 0].index.tolist()
        FE = FE.set_value(index = index, col='reasons', value=lab)

    ##Quantification underutilization
    FE['quant_underutilized'] = 0
    FE['quant_overutilized'] = 0
    FE['savings'] = 0
    for index, row in FE.iterrows():
        qtUnder,qtOver  = 0, 0
        if(row.utilization == 'under'):
            try:
                FE = FE.set_value(index=index, col='quant_underutilized', value=row.price*0.5)
                qtUnder = row.price*0.5
            except:
                FE = FE.set_value(index=index, col='quant_underutilized', value=float(row.price.replace(',','')) * 0.5)
                qtUnder = float(row.price.replace(',','')) * 0.5

        if row.utilization == 'over' and row.ordinal > 1:
            x = FE.loc[FE.ordinal == (row.ordinal + 1)]['sq_hr']
            x.reset_index(inplace=True, drop=True)
            v = (row.usageMedian - (row.sq_hr / (x[0])) * 60) / 60 * 365 * 20
            FE = FE.set_value(index=index, col='quant_overutilized', value=v)
            qtOver = v

        FE = FE.set_value(index=index, col='savings', value=(qtUnder + qtOver))


    FE['difficulty_1'] = 0
    i = FE.loc[FE['contract']==0].index
    FE = FE.set_value(index=i, col='difficulty_1', value=30)

    FE['difficulty_2'] = 0
    i = FE.loc[FE['cost_negot']==0].index
    FE = FE.set_value(index=i, col='difficulty_2', value=30)

    FE['difficulty_3'] = 0
    i = FE.loc[FE['other_available']==0].index
    FE = FE.set_value(index=i, col='difficulty_3', value=100)

    FE['difficulty_4'] = 0
    i = FE.loc[FE['other_in_proximity']==0].index
    FE = FE.set_value(index=i, col='difficulty_4', value=30)

    FE['difficulty_5'] = 0
    i = FE.loc[FE['bigger_fit_doors']==0].index
    FE = FE.set_value(index=i, col='difficulty_5', value=100)

    FE['difficulty_6'] = 0
    i = FE.loc[FE['storage_closet']==0].index
    FE = FE.set_value(index=i, col='difficulty_6', value=100)

    FE['difficulty_7'] = 0
    i = FE.loc[FE['skills_in_team']==0].index
    FE = FE.set_value(index=i, col='difficulty_7', value=10)

    FE['difficulty'] = FE['difficulty_1']+FE['difficulty_2']+FE['difficulty_3']+FE['difficulty_4']+FE['difficulty_5']+\
    FE['difficulty_6']+FE['difficulty_7']

    i = FE.loc[FE.difficulty >= 100].index
    FE = FE.set_value(index=i, col='difficulty_type', value=3)
    FE = FE.set_value(index=i, col='Traffic', value='Red')

    i = FE.loc[(FE.difficulty > 30) & (FE.difficulty < 100)].index
    FE = FE.set_value(index=i, col='difficulty_type', value=2)
    FE = FE.set_value(index=i, col='Traffic', value='Amber')

    i = FE.loc[FE.difficulty <= 30].index
    FE = FE.set_value(index=i, col='difficulty_type', value=1)
    FE = FE.set_value(index=i, col='Traffic', value='Green')

    del FE['difficulty_1']
    del FE['difficulty_2']
    del FE['difficulty_3']
    del FE['difficulty_4']
    del FE['difficulty_5']
    del FE['difficulty_6']
    del FE['difficulty_7']
    del FE['difficulty']
    #FE.to_csv('/srv/s3_bucket/ISS Decision Sciences/Intellitrail_dashboard_data.tsv', sep='\t')
    FE.to_sql('tableau', con=engine, schema='public', if_exists='replace')
    print "done"

        

