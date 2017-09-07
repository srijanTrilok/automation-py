from ..utility import time_extract


def intent_process(event):
    duration = event["currentIntent"]["slots"]["datetime"]
    time_obj = time_extract.extract_time(duration)
    msg = "Overall service hand hygene health for food safety is 2 in last " + time_obj["time"] + " " + time_obj["time_type"]
    return msg