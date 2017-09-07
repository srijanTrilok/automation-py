
def intent_process(event):
    activity = event["currentIntent"]["slots"]["activity"].lower()
    msg = "Sorry we did not find anything for your query."

    if activity == "active" or activity == "online":
        msg = "Currently 50 robots are online out of 70 robots"
    if activity == "inactive" or activity == "offline":
        msg = "10 robots are Inactive out of 70 robots."

    return msg