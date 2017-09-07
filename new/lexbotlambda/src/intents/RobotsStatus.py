from ..modals.DBConnection import DBConnection

def intent_process(event):
    dbConn = DBConnection()
    response, savings_data = {}, {}
    response['type'] = "else"
    over, under, noneData, totalMachine = 0, 0, 0, 0
    slots = event["currentIntent"]["slots"]
    country = ''
    if slots['country'] is None:
        savings_data = dbConn.get_machine_status(country)
        if 'over' in savings_data:
            over = int(savings_data['over'])

        if 'under' in savings_data:
            under = int(savings_data['under'])

        if None in savings_data:
            noneData = int(savings_data[None])

        totalMachine = over + under + noneData
        
        response['msg'] = "Globally, there is <strong>"+str(((under + over) * 100)/totalMachine)+"%</strong> of savings opportunity in your machines portfolio.<ul><li>Total Machines: "+str(totalMachine)+"</li><li>Over-utilised machines: "+str(over)+"</li><li>Under-utilised machines: "+str(under)+"</li></ul>"
    
    else:
        country = slots['country']
        countryCount = dbConn.check_if_country_is_present_in_the_table(country)
        countryTitle = country.title()
        if countryCount == 0:
            response['msg'] = "Country with the name <strong>"+countryTitle+"</strong> is not present in our data set"
            return response

        #if country is present
        savings_data = dbConn.get_machine_status(country)

        if 'over' in savings_data:
            over = int(savings_data['over'])

        if 'under' in savings_data:
            under = int(savings_data['under'])

        if None in savings_data:
            noneData = int(savings_data[None])

        totalMachine = over + under + noneData
        
        response['msg'] = "In <strong>"+countryTitle+"</strong>, there is <strong>"+str(((under + over) * 100)/totalMachine)+"%</strong> of savings opportunity in your machines portfolio.<ul><li>Total Machines: "+str(totalMachine)+"</li><li>Over-utilised machines: "+str(over)+"</li><li>Under-utilised machines: "+str(under)+"</li></ul>"
    
    dbConn.close_the_connection()	
    return response
