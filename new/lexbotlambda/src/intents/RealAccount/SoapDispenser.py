
def intent_process(event):
    lowhigh = event["currentIntent"]["slots"]["lowno"].lower()

    if lowhigh == "low":
        msg = "There are 2 low soap dispensers"
    if lowhigh == "no" or lowhigh == "high":
        msg = "There is 1 high soap dispenser."

    return msg