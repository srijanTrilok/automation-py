from ..utility import time_extract


def intent_process(event):
    duration = event["currentIntent"]["slots"]["daytime"]
    time_obj = time_extract.extract_time(duration)
    msg = "There are 40 cases used and 20 cases wasted in last %d %s" % (time_obj["time"], time_obj["time_type"])
    return msg