import os
from lib.configobj import ConfigObj


CONFIG_FILE= os.path.join(os.getcwd(), "config.ini")
CFG = ConfigObj(CONFIG_FILE)

def CheckSection(sec):
    """ Check if INI section exists, if not create it """
    try:
        CFG[sec]
        return True
    except:
        CFG[sec] = {}
        return False

def check_setting_str(config, cfg_name, item_name, def_val, log=True):
    try:
        my_val = config[cfg_name][item_name]
    except:
        my_val = def_val
        try:
            config[cfg_name][item_name] = my_val
        except:
            config[cfg_name] = {}
            config[cfg_name][item_name] = my_val
    return my_val


def check_setting_int(config, cfg_name, item_name, def_val):
    try:
        my_val = int(config[cfg_name][item_name])
    except:
        my_val = def_val
        try:
            config[cfg_name][item_name] = my_val
        except:
            config[cfg_name] = {}
            config[cfg_name][item_name] = my_val
    return my_val

CheckSection('General')
DB_ROOT = check_setting_str(CFG, 'General', 'DB_ROOT', os.path.join(os.getcwd(), "Calibre Library"))
TEMPLATEDIR = check_setting_str(CFG, 'General', 'TEMPLATEDIR', os.path.join(os.getcwd(), "views"))
PORT = check_setting_str(CFG, 'General', 'PORT', 1337)
NEWEST_BOOKS = check_setting_str(CFG, 'General', 'NEWEST_BOOKS', 20)
ALL_BOOKS = check_setting_str(CFG, 'General', 'ALL_BOOKS', 100)
USER = check_setting_str(CFG, 'General', 'USER', "admin")
PASS = check_setting_str(CFG, 'General', 'PASS', "calibreserver")
WEB_ADMIN = bool(check_setting_int(CFG, 'General', 'WEB_ADMIN', 1))

SYS_ENCODING="UTF-8"

configval={}
configval["DB_ROOT"] = DB_ROOT
configval["TEMPLATEDIR"] = TEMPLATEDIR
configval["PORT"] = PORT
configval["NEWEST_BOOKS"] = NEWEST_BOOKS
configval["ALL_BOOKS"] = ALL_BOOKS
configval["USER"] = USER
configval["PASS"] = PASS
configval["WEB_ADMIN"] = WEB_ADMIN

def save_config(configval):
    new_config = ConfigObj()
    new_config.filename = CONFIG_FILE
    new_config['General'] = {}
    new_config['General']['DB_ROOT'] = configval["DB_ROOT"]
    new_config['General']['TEMPLATEDIR'] = configval["TEMPLATEDIR"]
    new_config['General']['PORT'] = configval["PORT"]
    new_config['General']['NEWEST_BOOKS'] = configval["NEWEST_BOOKS"]
    new_config['General']['ALL_BOOKS'] = configval["ALL_BOOKS"]
    new_config['General']['USER'] = configval["USER"]
    new_config['General']['PASS'] = configval["PASS"]
    new_config['General']['WEB_ADMIN'] = int(configval["WEB_ADMIN"])
    new_config.write()
    return "Saved"

save_config(configval)