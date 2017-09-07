import pandas as pd
import numpy as np

###MACHINE TYPE CLEANING
#read all data
raw = pd.read_csv('raw.tsv', sep='\t', error_bad_lines=False)

#fix machineNumber
def uidFixer(x):
    try:
        o = str(int(float(x)))
    except:
        o = str(x)
    return(o)

mi = [uidFixer(x) for x in raw.MachineNumber]
raw['MachineNumber'] = mi

#Global is USA?
raw.head()
i = raw.loc[raw.FakeCountry=='Global'].index.tolist()
raw.set_value(i, col='FakeCountry', value='USA')

#read machine type lookup
machinetype = pd.read_csv('machine_type_lookup.tsv', sep='\t')#, error_bad_lines=False)

data = pd.merge(raw, machinetype,
                left_on = 'MachineTypDesignation', right_on = 'machine_type_old', how = 'inner')
#read machine price swap ordinal lookup
machineordinalswap = pd.read_csv('type_swap_price_ordinal_lookup.tsv', sep='\t', error_bad_lines=False)
machineordinalswap.head()

data = pd.merge(data, machineordinalswap,
                left_on = 'machine_type_basename', right_on = 'machine_type', how = 'inner')
print(data.head())

#Extract only meaningful columns
cols = ['MachineNumber', 'machine_type_basename', 'Date', 'Hours', 'CustomerId', 'SiteId',
        'SiteNumber', 'SiteName1', 'FakeCountry', 'sq_hr', 'price_euro', 'type', 'size',
        'overutilization', 'swap_up_with', 'swap_down_with']
data = data[cols]
data = data.loc[data.Hours>0.0]

#Template DF
FE = data[['MachineNumber', 'machine_type_basename', 'FakeCountry',
           'SiteId', 'SiteNumber', 'SiteName1', 'sq_hr', 'price_euro',
           'type','size','overutilization', 'swap_up_with', 'swap_down_with']].drop_duplicates(subset='MachineNumber')
FE.reset_index(inplace=True, drop=True)
print(FE.head())
#FE.to_csv('data.tsv', sep='\t', index=False, encoding='utf8')

usageMedian = data.groupby(by='MachineNumber')['Hours'].median()*60
#usage in min
usageQ3 = data.groupby(by='MachineNumber')['Hours'].quantile(q=0.75)*60
usageQ1 = data.groupby(by='MachineNumber')['Hours'].quantile(q=0.25)*60
FE['usageMedian'] = list(usageMedian)
FE['usageQ3'] = list(usageQ3)
FE['usageQ1'] = list(usageQ1)
print(FE.head())
#
# #Asset utilization
data['date_'] = pd.to_datetime(arg=data['Date'])
print(data.head())
#
i = data.MachineNumber.unique()[0]
d = data.loc[data.MachineNumber == i]


def asset_utilization(i):
    d = data.loc[data.MachineNumber == i]
    if d.shape[0] > 1:
        ran = ((d.date_.max() - d.date_.min()) / np.timedelta64(1, 'D')).astype(float)+1
        ndays = len(d.Date.unique())
        if (ndays > 0) & (ran > 0):
            return(ndays/ran)
        else:
            return(0)

FE['assetUti'] = ''
for index, row in FE.iterrows():
    asu = asset_utilization(row.MachineNumber)
    FE.set_value(index, col='assetUti', value=asu)

print(FE.head())
#

key = FE.usageMedian>FE.overutilization
FE.set_value(index=key, col='utilization', value='over')
print(FE.head())

#key = FE.loc[(FE.usageMedian<20) | (FE.assetUti<0.15) ].index.tolist()
key = FE.loc[FE.assetUti<0.30].index.tolist()
FE.set_value(index=key, col='utilization', value='under')
print(FE.head())

# RELOCATION CRITERIA
#50% of the underutilized machines can be relocated
relo = FE.loc[FE.utilization=='under'].MachineNumber.sample(frac=0.5)
key = FE.loc[FE.MachineNumber.isin(relo)].index.tolist()
FE['relocated'] = 0
FE.set_value(index=key, col='relocated', value=1)
print(FE.head())

#
# # Criteria for recommendation
# #The criteria defined below depends sometimes depends on the client, the geographical location, etc
# #this first test does not take any of this into account and defines the criteria as machine only dependent
# #1) Does the contract allow a machine switch (allowed to 40% of the clients)
cid = pd.DataFrame(data={'cid':data.CustomerId.unique()})
cid['contract'] = np.random.binomial(1,0.7,cid.shape[0])
mid = data.loc[data.CustomerId.isin(cid.loc[cid.contract==1].cid)].MachineNumber.unique()
key = FE.loc[FE.MachineNumber.isin(mid)].index.tolist()
FE['contract'] = 0
FE.set_value(index=key, col='contract', value=1)
print(FE.head())
#    #1.1) Is the re-negotiation cost low (or free)? (50% of customers whose contract doesn't allow switch
# #  can switch for a low premium or for free)
cid_yes = cid.loc[cid.contract==0].cid.sample(frac=0.7)
mid = data.loc[data.CustomerId.isin(cid_yes)].MachineNumber.unique()
key = FE.loc[FE.MachineNumber.isin(mid)].index.tolist()
FE['cost_negot'] = 1
FE.set_value(index=key, col='cost_negot', value=0)
print(FE.head())
#
# #2) Is there a bigger/smaller machine available (per customer?)
FE['other_available'] = np.random.binomial(1, 0.7, FE.shape[0])
print(FE.head())
#
# #3) Is there a substitute machine in the close proximity (per location?)
FE['other_in_proximity'] = np.random.binomial(1, 0.6, FE.shape[0])
print(FE.head())
#
# #4) Does the machine fit within the doorways
FE['bigger_fit_doors'] = np.random.binomial(1, 0.9, FE.shape[0])
print(FE.head())
#
# #5) Is the storage closet big enough
FE['storage_closet'] = np.random.binomial(1, 0.9, FE.shape[0])
print(FE.head())
#
# #6) Can the operators use it without training?
FE['skills_in_team'] = np.random.binomial(1,0.9,FE.shape[0])
print(FE.head())
#
for index, row in FE.iterrows():
    k = (all(row[['contract', 'cost_negot', 'other_available', 'other_in_proximity',
     'bigger_fit_doors', 'storage_closet', 'skills_in_team']])==1)
    if (k and row.utilization=='under'):
        FE.set_value(index=index, col='recommendation', value='downgrade')
    elif (k and row.utilization=='over'):
        FE.set_value(index=index, col='recommendation', value='upgrade')

#recommendation test
print(FE.head())


FE['upgrade_to'] = ''
FE['downgrade_to'] = ''
for index, row in FE.iterrows():
    if (row.recommendation == 'downgrade'):
        FE.set_value(index=index, col='downgrade_to', value=row.swap_down_with)
    if(row.recommendation == 'upgrade'):
        FE.set_value(index=index, col='upgrade_to', value=row.swap_up_with)

FE['reasons'] = ''
for index, row in FE.iterrows():
    ss = pd.DataFrame(data={'items':row[['contract', 'cost_negot', 'other_available', 'other_in_proximity',
           'bigger_fit_doors', 'storage_closet', 'skills_in_team']]})
    lab = ss.loc[ss['items'] == 0].index.tolist()
    if (len(lab) > 0):
        FE.set_value(index = index, col='reasons', value=lab)

##Quantification underutilization
FE['quant_underutilized'] = ''
FE['quant_overutilized'] = ''
for index, row in FE.iterrows():
    if(row.utilization == 'under'):
        FE.set_value(index=index, col='quant_underutilized', value=row.price_euro*0.5)
    if(row.utilization == 'over'):
        try:
            x = FE.loc[FE.swap_down_with == row.machine_type_basename].sq_hr
            x.reset_index(inplace=True, drop=True)
            v = (row.usageMedian - (row.sq_hr/(x[0]))*60)/60*365*20
            FE.set_value(index=index, col='quant_overutilized', value=v)
        except:
            pass


FE.to_csv('Intellitrail_dashboard_data.tsv', sep='\t')


x = FE.loc[FE.FakeCountry == 'Finland']