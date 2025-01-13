import datetime
from encode_defs import *


def decode(message: str, key: str):
    key_list = [key[i:i+4] for i in range(0, len(key), 4)]
    message_list = [message[i:i+3] for i in range(0, len(message), 3)]
    stringbuilder = ""
    
    keymap = {}

    for e in key_list:
        keymap.update({f"{e[0]}{e[1]}{e[3]}": e[2]})

    for m in message_list:
        stringbuilder += keymap.get(m)

    return stringbuilder



def decode_str(content_c: str):
    content = content_c[len(KEY_PREFIX) - 1:]
    key = content.split(KEY_SUFFIX)[0]
    content = content.split(KEY_SUFFIX)[1]

    message = content[len(MESSAGE_PREFIX) - 1:len(MESSAGE_SUFFIX)]

    print(message)

    return decode(message, key)