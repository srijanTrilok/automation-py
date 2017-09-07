import re


def extract_time(str):
    split_time = re.split('(\d+)', str)
    get_first_part = split_time[0]
    get_time = split_time[1]
    get_time_type = split_time[2]

    if get_time_type == "D":
        msg_suffix = "Days"
    elif get_time_type == "W":
        msg_suffix = "Weeks"
    elif get_time_type == "M":
        if get_first_part == "PT":
            msg_suffix = "Minutes"
        else:
            msg_suffix = "Months"
    elif get_time_type == "Y":
        msg_suffix = "Years"
    elif get_time_type == "H":
        msg_suffix = "Hours"
    else:
        msg_suffix = "Days"
    return {"time": get_time, "time_type": msg_suffix}