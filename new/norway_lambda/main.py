import sys, os
import importlib
import pkgutil
import json
import urllib
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/lib")


def lambda_handler(event, context):
    response = False
    import_path = "Dashboard_data"
    process_module = importlib.import_module(import_path)
    process_module.file_process(event)
    return "done"