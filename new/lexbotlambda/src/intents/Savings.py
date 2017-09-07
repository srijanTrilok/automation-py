from ..modals.DBConnection import DBConnection
from ..utility import utility

def intent_process(event):
    dbConn = DBConnection()
    response = {}
    response['type'] = "else"
    slots = event["currentIntent"]["slots"]
    savings_data = 0
    countries = ""
    if slots['country'] is None:
        savings_data = dbConn.get_savings_data(countries)
        response['msg'] = "Globally, Savings in your machine portfolio is <b>&euro;%s</b>" % (str(format(int(savings_data), ",d")))
        
    else:
        country = slots['country']
        countryCount = dbConn.check_if_country_is_present_in_the_table(country)
        countryTitle = country.title()
        if countryCount == 0:
            response['msg'] = "Country with the name <strong>"+countryTitle+"</strong> is not present in our data set"
            return response

        #if country is present
        savings_data = dbConn.get_savings_data(country)
        response['msg'] = "In <b> %s</b>, Savings in your machine portfolio is <b>&euro;%s</b>" % (countryTitle, str(format(int(savings_data), ",d")))
    
    dbConn.close_the_connection()   
    return response   

