#is valid file name

def file_name_valid(file_name):
    if len(file_name) < 1:
        return False
    if len(file_name) > 255:
        return False
    return True