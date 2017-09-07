"""responseCard": {
                "version": 1,
                "contentType": "application/vnd.amazonaws.card.generic",
                "genericAttachments": [
                    {
                        "title": "Active or Inactive ?",
                        #"imageUrl": "https://static.pexels.com/photos/50704/car-race-ferrari-racing-car-pirelli-50704.jpeg",
                        "buttons": [
                            {
                                "text": "Active/Online",
                                "value": "active"
                            },
                            {
                                "text": "Inactive/Offline",
                                "value": "inactive"
                            }
                        ]
                    }
                ]
            }
""" 
"""
cards, genericData, buttonsDict =   {}, {}, {}
listData, buttonsData = [], []
cards['version'] = 1
cards['contentType'] = "application/vnd.amazonaws.card.generic"
genericData['title'] = "Do you want me to ahead with next step? Please select the Country?"
genericData['imageUrl'] = "https://www.sketchappsources.com/resources/source-image/coutry-flags-by-joimau.png"

buttonsDict['title'] = "test"
buttonsDict['value'] = "test"

buttonsData.append(buttonsDict)

buttonsDict['title'] = "test"
buttonsDict['value'] = "test"

buttonsData.append(buttonsDict)

genericData['buttons'] = buttonsData
listData.append(genericData)
cards['genericAttachments'] = listData 
print cards


from collections import Counter
data = []
dictD = {}
data =['test1','test2','test3','test1','test1']
dictD = Counter(data)
print dictD['test1']

for i,j in dictD.items()[:3]:
    print(i,j)



data ="['test1','test2','test3','test1','test1']"
for val in list(data.split(',')[1:-1]):
    print val

def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    units = ['','one','two','three','four','five','six','seven','eight','nine']
    teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
             'seventeen','eighteen','nineteen']
    tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
            'eighty','ninety']
    thousands = ['','thousand','million','billion','trillion','quadrillion', \
                 'quintillion','sextillion','septillion','octillion', \
                 'nonillion','decillion','undecillion','duodecillion', \
                 'tredecillion','quattuordecillion','sexdecillion', \
                 'septendecillion','octodecillion','novemdecillion', \
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = (numStrLen+2)/3
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = groups-(i/3+1)
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+',')
    if join: return ' '.join(words)
    return words

print numToWords(12332,True)  



# print rowData
        #print self.algos_table
        #print type(self.algos_table)
        a = {}
        for i in rowData:
            for j, k in i.items():
                a[str(j)] = str(k)
        #print(a)
        tb = "persons"
        self.db.tb.bulk_insert([a])
        #self.db.table_nameinsert(table_name = str(config.db_name), Firstname = "Some") 

columnData = ["hello","bolo","holo"]
*[Field(items) for items in columnData]

s = "hello_sadfsdf"
tb = s.split("_")
print(tb[0])


#once processing is done copy the file to inserted_json_files folder
        #s3.Object( bucket_name, afterInsertMoveToFolder+'/'+filename ).copy_from(CopySource = bucket_name+'/'+filename)
        Archive.upload_glacier(event)
        #once moved the file to folder delete them
        #s3.Object( bucket_name, filename).delete()
"""

d = [1,2,3,4,5]
print d
d = []
d = [21]
print d
