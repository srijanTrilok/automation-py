import boto3
import json
import urllib
import logging
from ..modals.DBConnection import DBConnection
from .. import config
import Archive

s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def file_process(event):
    bucket_name = config.s3bucket
    for file_obj in event['Records']:
        fieldStr, fieldPK = '', ''
        columnData = []
        filename = urllib.unquote_plus(file_obj['s3']['object']['key'].encode("utf8"))
        #filename = "persons_1231255.json"
        fileObj = s3.get_object(Bucket = bucket_name, Key = filename)

        #process the file if table is not present create a table else update the data
        json_data = json.loads(fileObj['Body'].read().decode('utf-8'))
        for tblName in json_data:
            tableName = tblName
            break

        bulkInsert = json_data[tableName][0]["Data"]
        for rowdata in json_data[tableName][0]["Columns"]:
            if rowdata['ColumnName'].lower() != 'id':
                typeDataValue = getType(rowdata['DataType'].lower())
                emptyDict = {}
                emptyDict = { 'name': rowdata['ColumnName'].lower(), 'type': typeDataValue}
                columnData.append(emptyDict)

        #initilise a connection        
        dbConn = DBConnection(tableName, columnData)

        insertDataList, deleteRowItem, updateData = [], [], []
        deleteRItem = ''
        for dictItems in bulkInsert:
            data = {}
            data = dict((str(k.lower()), str(v)) for k,v in dictItems.iteritems())
            
            caseCheck = data['sys_change_operation']
            # A Delete all, D is to delete based on the Id, U is to update, else I ie.Insert
            if caseCheck == 'A':
                #if delete entire data Empty the list for insert update and delete
                insertDataList, deleteRowItem, updateData = [], [], []
                deleteRItem = ''

                sql = ''
                sql = "DELETE FROM "+tableName
                dbConn.execute_sql(sql)

            elif caseCheck == 'D':
                deleteRowItem.append(data['id'])
                deleteRItem += data['id']+","

            elif caseCheck == 'U':
                print "update to be done here"
                updateData.append(data)

            else:
                insertDataList.append(data)
            
            
        #Interacting with the db starts here for insert delete update

        #insert data
        if insertDataList:
            dbConn.bulk_insert_data(insertDataList, tableName)

        #update Items
        if updateData:
            for updateRow in updateData:
                updateSql, updateWhere, finalUpdateSql = '', '', ''
                updateSql = "UPDATE "+tableName+" SET "
                for updateKey, updateValue in updateRow.iteritems():
                    if updateKey != 'id':
                        updateSql += updateKey + "='"+str(updateValue) +"',"
                    else:
                        updateWhere = " WHERE "+ updateKey +"="+ updateValue
                finalUpdateSql = updateSql[:-1] + updateWhere
                print finalUpdateSql
                dbConn.execute_sql(finalUpdateSql)


        #delete items
        if deleteRowItem:
            sql = ''
            sql = "DELETE FROM "+tableName+" WHERE id IN ("+deleteRItem[:-1]+")"
            dbConn.execute_sql(sql)

        #close a connection
        dbConn.close_the_connection()
        #archive file to Glacier
        Archive.upload_glacier(event)

        return True

def getType(typeData):
    typeStr = typeData.replace("system.","")
    if typeStr.startswith('int'):
        return 'integer'
    elif typeStr.startswith('string'):
        return 'string'
    else:
        return 'string'

