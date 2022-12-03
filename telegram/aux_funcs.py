import re


def check_time_format(time_string: str):
    """Return None if time_string is not in format hh:mm"""
    selected_time_list = time_string.split(':')
    try:
        selected_time_list[1]
    except Exception as ex:
        ex
        return None
    if not re.findall(r'\d+', selected_time_list[0]):
        return None
    if int(selected_time_list[0]) > 23 or int(selected_time_list[0]) < 0:
        return None
    if not re.findall(r'\d+', selected_time_list[1]):
        return None
    if int(selected_time_list[1]) > 60 or int(selected_time_list[1]) < 0:
        return None
    return f'{selected_time_list[0]}:{selected_time_list[1]}'
