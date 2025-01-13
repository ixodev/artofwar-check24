import random
import datetime
from encode_defs import *



def shuffle_string(s: str):
    l = list(s)
    random.shuffle(l)
    return "".join(l)

def string_list_to_string(l: list):
    stringbuilder = ""

    for e in l:
        stringbuilder += e

    return stringbuilder

def generate_key(keymap: dict):
    stringbuilder_list = []

    for key in keymap.keys():
        stringbuilder_list.append(f"{key[0]}{key[1]}{keymap.get(key)}{key[2]}")

    random.shuffle(stringbuilder_list)
    return string_list_to_string(stringbuilder_list)

def encode(message: str, model_string: str):
    std_to_enc = {}
    enc_to_std = {}
    already_taken = []
    stringbuilder = ""
    enc = None

    for std in message:
        if not std in std_to_enc.keys():
            enc = f"{random.choice(model_string)}{random.choice(model_string)}{random.choice(model_string)}"
            while enc in already_taken:
                enc = f"{random.choice(model_string)}{random.choice(model_string)}{random.choice(model_string)}"
            already_taken.append(enc)
            std_to_enc.update({std: enc})
            enc_to_std.update({enc: std})
        stringbuilder += std_to_enc.get(std)

    return [stringbuilder, generate_key(enc_to_std)]



def write_msg_file(message_to_encode: str, path: str):
    model_string = shuffle_string("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                                     + " \n#,;:!?./§^$ù*/¨£%µ+=°&é\"'(-è_çà)~[{|`\^@]}\\")
    
    message = encode(message_to_encode, model_string)

    file = open(path, "w")
    file.write(KEY_PREFIX + message[1] + KEY_SUFFIX)
    file.write(MESSAGE_PREFIX + message[0] + MESSAGE_SUFFIX)
    file.close()