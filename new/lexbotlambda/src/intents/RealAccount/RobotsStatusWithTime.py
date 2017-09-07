
def intent_process(event):
    activity = event["currentIntent"]["slots"]["activity"].lower()
    msg = "Sorry we did not find anything for your query."

    if activity == "active" or activity == "online":
        msg = "50 robots are online out of 70 robots for last 24 hours"
    if activity == "inactive" or activity == "offline":
        msg = "Ten robots are Inactive out of 70 robots for last 24 hours"

    return msg