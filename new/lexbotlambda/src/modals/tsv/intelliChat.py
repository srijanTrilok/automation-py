import pandas as pd
import os


class intelliChat:

    country = ''

    def __init__(self, country = 'Germany'):
        current_file = os.path.abspath(os.path.dirname(__file__))
        self.data = pd.read_csv(current_file + '/data/intellitrail_dashboard_data.tsv', sep='\t', encoding= 'latin-1')
        self.country = country


    ###Q1  How much could I save on country X?
    # This question addresses ALL hypothetical savings
    # i.e without taking into account reasons preventing from upgrade/downgrade
    def totalSavings(self):
        #d = self.data.loc[self.data.FakeCountry == self.country]
        s1 = self.data.quant_underutilized.sum()
        s2 = self.data.quant_overutilized.sum()
        return(s1+s2)

    ###Q2 Which machines should I downgrade in country X?
    def machineToDowngrade(self):
        d = self.data.loc[self.data.FakeCountry == self.country]
        s1 = d.loc[d.recommendation=='downgrade']['MachineNumber']
        s2 = d.loc[d.recommendation=='downgrade']['machine_type_basename']
        return(list(zip(s1,s2)))

    ###Q2 Which machines should I upgrade in country X?
    def machineToUpgrade(self):
        d = self.data.loc[self.data.FakeCountry == self.country]
        s1 = d.loc[d.recommendation=='upgrade']['MachineNumber']
        s2 = d.loc[d.recommendation=='upgrade']['machine_type_basename']
        return(list(zip(s1,s2)))

    ###Q2 Which machines should I upgrade in country X?
    def machineRobotsStatus(self):
        under = self.data.quant_underutilized.count()
        over = self.data.quant_overutilized.count()
        return {'over': over, 'under': under, 'total': (over + under)}

    def dynaCaller(self, func_name):
        def func_not_found(): # just in case we dont have the function
            return "No Function "+func_name+" Found!"
        func = getattr(self,func_name,func_not_found)
        return func() # <-- this should work!


'''
### Default method to be called if no arguement is present
func_name = "machineToDowngrade"
## Create an instance of the class
ques = intelliChat()
## Check if country name is passed in the command line
if len(sys.argv) > 1:
    ques.country = sys.argv[1]
## Check if method name is passed in the command line
if len(sys.argv) > 2:
    func_name = sys.argv[2]
print(ques.dynaCaller(func_name))

## example
## python intelliChat.py
## python intelliChat.py Netherlands
## python intelliChat.py Netherlands machineToUpgrade
'''
