import re

def pwd_minmal_valid(pwd):
    if len(pwd) < 8:
        return False
    return True

# strong pwd
def pwd_strong_valid(pwd):
    if len(pwd) < 8:
        return False
    if not re.search(r'[a-z]', pwd):
        return False
    if not re.search(r'[A-Z]', pwd):
        return False
    if not re.search(r'[0-9]', pwd):
        return False
    return True