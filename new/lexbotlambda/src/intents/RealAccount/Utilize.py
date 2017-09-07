
def intent_process(event):
    utilization = event["currentIntent"]["slots"]["utilization"].lower()
    if utilization == "under":
        msg = "There are 20 machines under utilized out of 100 machines."
    if utilization == "over":
        msg = "There are 20 machines over utilized."
    return msg