import config
from pydal import DAL, Field
from collections import Counter

class DBConnection(object):

    db = ''
    algos_table = ''

    def __init__(self):
        # only if conn is not defined
        if self.db is not None:
            print "connection initiate"
            self.db = DAL(self.get_dbconn_string(), migrate = False, ignore_field_case=True, attempts=1)

            # define table schema
            self.algos_table = self.db.define_table(config.db_table,
                                 Field('index'),
                                 Field("MachineNumber"),
                                 Field("FakeCountry"),
                                 Field("quant_underutilized"),
                                 Field("quant_overutilized"),
                                 Field("sq_hr"),
                                 Field("reasons"),
                                 Field("utilization"),
                                 primarykey=['index'],
                                 redefine=True
                                 )

    def get_algos_table(self):
        return self.algos_table

    def get_top_countries(self):
        
        """
        aDict = {}
        machines = self.db().select(
            self.algos_table.FakeCountry,
            self.algos_table.quant_underutilized.sum(),
            groupby=self.algos_table.FakeCountry,
            orderby=self.algos_table.quant_underutilized.sum(),
            limitby=(0, 5)
        )
        """
        #machines = self.db.executesql('SELECT sum("machine_master"."quant_underutilized") + sum("machine_master"."quant_overutilized") as "total", "machine_master"."FakeCountry" FROM machine_master GROUP BY "machine_master"."FakeCountry" HAVING sum("machine_master"."quant_underutilized") + sum("machine_master"."quant_overutilized") > 0 ORDER BY total DESC')
        machines = self.db.executesql('SELECT sum("'+config.db_table+'"."quant_underutilized") + sum("'+config.db_table+'"."quant_overutilized") as "total", "'+config.db_table+'"."FakeCountry" FROM '+config.db_table+' GROUP BY "'+config.db_table+'"."FakeCountry" HAVING sum("'+config.db_table+'"."quant_underutilized") + sum("'+config.db_table+'"."quant_overutilized") > 0 ORDER BY total DESC LIMIT 5 OFFSET 0')
        
        return machines
        '''
        counter = 0
        for machine in machines:
            country = machine[1]
            savings = machine[0]
            aDict[country] = savings
            dicta.append(country,savings)

        print dicta    
        return aDict
        '''

    # get data for savings    
    def get_savings_data(self,country):
        underutilize, overutilization, response = 0, 0, 0
        where = ''
        if country:
            where = (self.algos_table.FakeCountry.like(country,case_sensitive=False))
        
        savingData = self.db(where).select(
                self.algos_table.quant_underutilized.sum(),
                self.algos_table.quant_overutilized.sum()
            )
        
        for savingTotal in savingData:
            if savingTotal[self.algos_table.quant_underutilized.sum()]:
                underutilize = savingTotal[self.algos_table.quant_underutilized.sum()]

            if savingTotal[self.algos_table.quant_overutilized.sum()]:
                overutilization = savingTotal[self.algos_table.quant_overutilized.sum()]

        response = underutilize + overutilization
        return response
        
    def get_reason_for_country(self,country):
        reasonString, responseStr = "", ""
        where = ""
        reasonList, testList = [], []
        reasonDict = {}
        if country:
            where = (self.algos_table.FakeCountry.like(country,case_sensitive=False))
            reasonData = self.db(where).select(
                self.algos_table.reasons
            )
        for reasonTotal in reasonData:
            if reasonTotal[self.algos_table.reasons]:
                reasonString = ""
                reasonString = reasonTotal[self.algos_table.reasons][1:-1].split(',')
                for val in reasonString:
                    reasonList.append(val.replace(" ", ""))
        
        reasonDict = Counter(reasonList)
        responseStr = "<br /><ul>"
        for ReasonName, ReasonCount in reasonDict.items()[:3]:
            responseStr += "<li>"+ ReasonName.replace("'","") + "</li>"

        responseStr += "</ul><div style='display:block;'><p> For additional details, please go to <a href='https://tableau-prod.digital.diversey.com/t/Analytics/views/Chatbot/GlobalSavings1?%3Aembed=y&%3AshowShareOptions=true&%3Adisplay_count=no&%3AshowVizHome=no#1' target='_blank'>Diversey Intellitrail Dashboard.</a><p></div>"
        return responseStr

    def get_machine_status(self,country):
        aDict = {}
        machine = ""
        where = ''
        if country:
            where = (self.algos_table.FakeCountry.like(country,case_sensitive=False))
        
        machines = self.db(where).select(
            self.algos_table.utilization,
            self.algos_table.MachineNumber.count(),
            self.algos_table.utilization.count(),
            groupby=self.algos_table.utilization
        )
        
        for machine in machines:
            aDict[machine[self.algos_table.utilization]] = machine['_extra']['count("'+config.db_table+'"."MachineNumber")']  
        return aDict       

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

    def get_how_saving_can_be_archived(self, country):
        underutilize, overutilization, response = 0, 0, 0
        where = ''
        if country:
            where = (self.algos_table.FakeCountry.like(country,case_sensitive=False)) & (self.algos_table.reasons.like('[%'))
        
        savingData = self.db(where).select(
                self.algos_table.quant_underutilized.sum(),
                self.algos_table.quant_overutilized.sum()
            )
        
        
        for savingTotal in savingData:
            if savingTotal[self.algos_table.quant_underutilized.sum()]:
                underutilize = savingTotal[self.algos_table.quant_underutilized.sum()]

            if savingTotal[self.algos_table.quant_overutilized.sum()]:
                overutilization = savingTotal[self.algos_table.quant_overutilized.sum()]

        response = underutilize + overutilization
        return response 


    def check_if_country_is_present_in_the_table(self, country):
        where = ''
        countryPresent = 0
        if country:
            where = (self.algos_table.FakeCountry.like(country,case_sensitive=False))
            countryPresent = self.db(where).count()

        return countryPresent
            

    def close_the_connection(self):
        if self.db: 
            print "close the conn"
            self.db.commit()
            self.db.close()



        #total saving - downgrade and upgrade    

    '''
    def __init__(self):

        # only if conn is not defined
        if self.__conn is not None:
            self.__conn = psycopg2.connect("host='%s' port='5432' dbname='%s' user='%s' password='%s'" %
                                           (config.db_host, config.db_name, config.db_user, config.db_password))
            self.__cur = self.__conn.cursor()

    def get_conn(self):
        sql = sqlalchemy()
        return self.__conn

    def get_cursor(self):
        return self.__cur
    '''