import sys, os
import importlib
import pkgutil
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/lib")


def lambda_handler(event, context):
    intent_name = event["currentIntent"]["name"]
    intents_path = "src.intents." + intent_name
    message = {}
    # check if modules is available
    if pkgutil.find_loader(intents_path):
        utt_module = importlib.import_module(intents_path)
        message = utt_module.intent_process(event)  # need this function name in every file under lib/intents
    else:
        message['msg'] = "You do not have any handler for this intent."


    if message['type'] is "ElicitSlot":
        response = {
            'sessionAttributes': {},
            'dialogAction': {
                "type": "ElicitSlot",
                "slots": event['currentIntent']['slots'],
                "slotToElicit": message['slotToElicit'],
                "intentName": event['currentIntent']['name'],
                "message": {
                    'contentType': 'PlainText',
                    'content': message['msg']
                },
                "responseCard": message['responseCard']
            }
        }
    else:
        response = {
            'sessionAttributes': {},
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': "Fulfilled",
                'message': {
                    'contentType': 'PlainText',
                    'content': message['msg']
                }
            }
        }

    return response

"""
event = {
    "currentIntent": {
        "name": "TopCountries",
        "slots": {"country": ""}
    },
    "sessionAttributes": {}
}
print(lambda_handler(event, ""))

event = {
    "currentIntent": {
        "name": "Savings",
        "slots": {"country": ""}
    },
    "sessionAttributes": {}
}

print(lambda_handler(event, ""))

event = {
    "currentIntent": {
        "name": "RobotsStatus",
        "slots": {"country": "francess"}
    },
    "sessionAttributes": {}
}
print(lambda_handler(event, ""))

"""