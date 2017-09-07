import sys, os
import importlib
import pkgutil
import json
import urllib
#from src.execution import FileProcessing => throws pydal error
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/lib")


def lambda_handler(event, context):
    response = False
    if event:
        for file_obj in event['Records']:
            filename = urllib.unquote_plus(file_obj['s3']['object']['key'].encode("utf8"))
            fileExt = getFileExtension(filename)
            if fileExt == "json":
                import_path = "src.execution.FileProcessing"
            else:
                import_path = "src.execution.tsv_to_rds"

            if pkgutil.find_loader(import_path):
                process_module = importlib.import_module(import_path)
                process_module.file_process(event)
    '''import_path = "src.execution.tsv_to_rds"
    process_module = importlib.import_module(import_path)
    process_module.file_process(event)'''
    return "done"  

def getFileExtension(fileName):
    return fileName.split(".")[-1]
          
'''event = {
    "prefix": {
        "name": "persons_"
    }
}
print(lambda_handler(event, ""))'''
