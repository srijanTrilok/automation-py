from ..modals.DBConnection import DBConnection

def intent_process(event):
    #initialize
    dbConn = DBConnection()
    response, cards, genericData, buttonsDict = {}, {}, {}, {}
    listData, buttonsData = [], []
    totalOfupgradeAndDowngrade, savingPercent = 0, 0
    slots = event["currentIntent"]["slots"]
    if slots['country']:
        country = slots['country']
        savings_data = dbConn.get_savings_data(country)
        reasonString = dbConn.get_reason_for_country(country)
        # in the below function will get the data with reasons filled
        totalUgradeDowngrade = dbConn.get_how_saving_can_be_archived(country)
        #reason - total = remaining upgrde downgrade
        #to get the data where there is no reasons (savings_data - totalUgradeDowngrade)
        totalOfupgradeAndDowngrade = savings_data - totalUgradeDowngrade
        savingPercent =  (totalOfupgradeAndDowngrade*100) / savings_data
        countryTitle = country.title()
        msg = "In <b> "+countryTitle+"</b>, <b> "+str(int(savingPercent))+"%</b> of the savings cannot be achieved due to the following top 3 reasons "+reasonString+" "
        
        response['msg'] = msg 
        response['type'] = "else"
    else:  
        response['type'] = "ElicitSlot" 
        response['slotToElicit'] = "country"

        top_countries = dbConn.get_top_countries()
        output = ''
        if top_countries:
            counter = 0
            #form a card
            cards['version'] = 1
            cards['contentType'] = "application/vnd.amazonaws.card.generic"
            genericData['title'] = "Do you want me to ahead with next step? Please select the Country?"
            genericData['imageUrl'] = "https://openclipart.org/download/233143/United-Globe.svg"

            for top_country in top_countries:
                counter = counter+1
                buttonsDict = {}
                output += str(counter) + '. ' + top_country[1] + ' (&euro;' + str((format(int(top_country[0]), ",d"))) + ') ' 
                buttonsDict['text'] = top_country[1] + ' (&euro;' + str((format(int(top_country[0]), ",d"))) + ') '
                buttonsDict['value'] = top_country[1]
                buttonsData.append(buttonsDict)
            """    
            for key, value in top_countries.items():
                counter = counter+1
                buttonsDict = {}
                output += str(counter) + '. ' + key + ' (' + str(value) + ') '
                buttonsDict['text'] = key + ' (' + str(value) + ') '
                buttonsDict['value'] = key
                buttonsData.append(buttonsDict)
            """

            genericData['buttons'] = buttonsData
            listData.append(genericData)
            cards['genericAttachments'] = listData

            response['responseCard'] = cards
        if output:
            response['msg'] = "This are the list of top 5 countries"
            #response['msg'] = "Top countries are " + output + " Do you want me to ahead with next step? which Country?"
        else:
            response['msg'] = "No record found!"
    print response
    dbConn.close_the_connection()
    return response