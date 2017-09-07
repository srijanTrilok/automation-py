import pandas as pd

data = pd.read_csv('intellitrail_dashboard_data.tsv', sep='\t', encoding= 'latin-1')

print(data.head())

###Q1  How much could I save on country X?
# This question addresses ALL hypothetical savings
# i.e without taking into account reasons preventing from upgrade/downgrade
country='France'
def totalSavings(country='France'):
    d = data.loc[data.FakeCountry==country]
    s1 = d.quant_underutilized.sum()
    s2 = d.quant_overutilized.sum()
    return(s1+s2)

###Q2 Which machines should I downgrade in country X?
def machineToDowngrade(country='France'):
    d = data.loc[data.FakeCountry == country]
    s1 = d.loc[d.recommendation=='downgrade']['MachineNumber']
    s2 = d.loc[d.recommendation=='downgrade']['machine_type_basename']
    return(list(zip(s1,s2)))

###Q3 Which machines should I upgrade in country X?
def machineToUpgrade(country='France'):
    d = data.loc[data.FakeCountry == country]
    s1 = d.loc[d.recommendation=='upgrade']['MachineNumber']
    s2 = d.loc[d.recommendation=='upgrade']['machine_type_basename']
    return(list(zip(s1,s2)))

###Q4 What are the top reasons why I can't upgrade or downgrade in country X?
def reasons(country='France', action='upgrade'):
    import re
    from collections import Counter

    d = data.loc[data.FakeCountry == country]
    try:
        if action=='upgrade':
            s1 = d.loc[(data.utilization == 'over') & pd.notnull(data.reasons)].reasons
        elif action=='downgrade':
            s1 = d.loc[(data.utilization == 'under') & pd.notnull(data.reasons)].reasons
        li = []
        for row in s1:
            r = re.findall(r"'(.*?)'", row, re.DOTALL)
            for i in r:
                li.append(i)

        return(Counter(li))
    except:
        print('Parameter action must be "upgrade" or "downgrade"')

