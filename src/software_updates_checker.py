import requests
from read_meta import *
from dialog_box import *


UPDATES_DIR = "http://ixodev.github.io/updates/artofwar/"
PATH_TO_FILE = f"{UPDATES_DIR}updates.meta"



def check_software_updates():
    try:
        meta_content = read_meta(requests.get(PATH_TO_FILE).text)

        update = False
        for val in meta_content.values():
            if val != "NULL":
                update = True

        if update:
            ...
            #messagebox = MessageBox("Art Of War", "An update is available on http://www.ixodev.github.io", MESSAGEBOX_OK)

    except:
        return None