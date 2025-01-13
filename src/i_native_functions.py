# BUILTIN FUNCTIONS USED BY THE I++ PROGRAMMING LANGUAGE

import sys
import time
import math

from dialog_box import *
from world import *
from player import *


def printf(world, player: Player, program_variables: dict, parameters: list):

    for parameter in parameters:
        print(str(parameter), end="")

def scanf(world, player: Player, program_variables: dict, parameters: list):
    return input()

def tos(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("itos expected 1 parameter")
    
    return str(parameters[0])

def messagebox(world, player: Player, program_variables: dict, parameters: list):
    # title, message, window hints
    if len(parameters) < 3:
        raise Exception("Not enough parameters given to messagebox function")

    if len(parameters) == 3:
        messagebox = MessageBox(str(parameters[0]), str(parameters[1]), int(parameters[2]), world.screen)
        messagebox.show()
        return messagebox.get_choice()

    title = str(parameters[0])

    try:
        window_hints = int(parameters[-1])
    except:
        raise Exception(f"{parameters[-1]} <= unknown option")

    message = list_to_string(parameters, 1, -1)

    messagebox = MessageBox(title, message, window_hints, world.screen)

    messagebox.show()
    return messagebox.get_choice()

def facesetbox(world, player: Player, program_variables: dict, parameters: list):
    # title, message, window hints
    if len(parameters) < 4:
        raise Exception("Not enough parameters given to facesetbox function")

    if len(parameters) == 4:
        messagebox = FacesetBox(str(parameters[0]), str(parameters[1]), int(parameters[3]), str(parameters[2]) + ".png", world.screen)
        messagebox.show()
        return messagebox.get_choice()

    title = parameters[0]

    try:
        window_hints = int(parameters[-1])
        faceset = str(parameters[-2])
    except:
        raise Exception(f"{parameters[-2]};{parameters[-1]} <= unknown option")

    message = list_to_string(parameters, 1, -2)

    messagebox = FacesetBox(title, message, window_hints, faceset + ".png", world.screen)

    messagebox.show()
    return messagebox.get_choice()

def list_to_string(l: list, start: int, end: int):
    l = l[start:end]

    string = ""

    for e in l:
        string += str(e)

    return string

def startfx_npc(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 4:
        raise Exception("fx_npc expected 4 parameters")
    
    fx_size = world.current_map.fx_manager.get_fx_size(parameters[1])
    npc = parameters[0]

    pos_x = npc.position[0] + npc.w / 2 - fx_size[0] / 2
    pos_y = npc.position[1] + npc.h / 2 - fx_size[1] / 2

    world.current_map.fx_manager.start_fx(parameters[1], (pos_x, pos_y), parameters[2], parameters[3])

def sysexit(world, player: Player, program_variables: dict, parameters: list):
    pg.quit()
    sys.exit(int(parameters[0]))

def show_credits(world, player: Player, program_variables: dict, parameters: list):
    return "The i++ programming language, written by Younes B."

def show_version(world, player: Player, program_variables: dict, parameters: list):
    return f"The i++ programming language, version 0.1.0, running on: Python 3. Game map context: {world.current_map.map_path}"

def switch_map(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("switch_map function expected 1 parameter")

    world.switch_map(parameters[0])


def fopen(world, player: Player, program_variables: dict, parameters: list):

    if len(parameters) != 2:
        raise Exception("fopen function expected 2 parameters")

    try:
        file = open(parameters[0], parameters[1])
        return file
    except:
        raise Exception("io error")

def fclose(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("fclose expected 1 parameter")

    parameters[0].close()

def fprintf(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) == 0:
        raise Exception("fprintf expected at least 1 parameter")


    for parameter in parameters:
        if parameter != parameters[0]:
            print(parameter, end="", file=parameters[0])

def fscanf(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("fscanf expected 1 parameter")

    return parameters[0].read()

def cleanup(world, player: Player, program_variables: dict, parameters: list):
    program_variables.clear()

def arr_add(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("arr_add expected 2 parameters")

    parameters[0].append(parameters[1])

def arr_ins(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 3:
        raise Exception("arr_ins expected 3 parameters")

    parameters[0].insert(int(parameters[1]), parameters[2])

def arr_ind(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("arr_ins expected 2 parameters")

    return parameters[0].index(parameters[1])

def arr_pop(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("arr_pop expected 2 parameters")

    parameters[0].pop(int(parameters[1]))

def arr_del(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("arr_del expected 2 parameters")

    parameters[0].remove(parameters[1])

def arr_clear(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("arr_clear expected 1 parameter")

    parameters[0].clear()

def arr_at(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("arr_at expected 2 parameters")
    
    return parameters[0][int(parameters[1])]

def arr_set(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 3:
        raise Exception("arr_set expected 3 parameters")
    
    parameters[0][int(parameters[2])] = parameters[3]

def unix_time_sec(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("unix_time_sec expected no parameters")

    return int(time.time())

def unix_time_min(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("unix_time_min expected no parameters")

    return int(time.time() / 60)

def unix_time_hour(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("unix_time_hour expected no parameters")

    return int(time.time() / 60 / 60)

def unix_time_day(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("unix_time_day expected no parameters")

    return int(time.time() / 60 / 60 / 24)

def unix_time_month(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("unix_time_month expected no parameters")

    return int(time.time() / 60 / 60 / 24 / 30.4375)

def unix_time_year(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("unix_time_year expected no parameters")

    return int(time.time() / 60 / 60 / 24 / 365.25)

def ftoi(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("ftoi expected 1 parameter")
    
    return int(round(parameters[0]))

def itof(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("itof expected 1 parameter")
    
    return float(parameters[0])

def stoi(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("stoi expected 1 parameter")
    
    return int(parameters[0])

def stof(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("stof expected 1 parameter")
    
    return float(parameters[0])

def get_npc_x(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("getnpcx expected 1 parameter")
    
    return parameters[0].position[0]

def get_npc_y(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("getnpcy expected 1 parameter")
    
    return parameters[0].position[1]

def set_npc_x(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("setnpcx expected 2 parameters")
    
    parameters[0].position[0] = parameters[1]

def set_npc_y(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("setnpcy expected 2 parameters")
    
    parameters[0].position[1] = parameters[1]

def get_npc_name(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("getnpcname expected 1 parameter")
    
    return parameters[0].name

def get_npc_interactions(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("getnpcinteractions expected 1 parameter")
    
    return world.entity_manager.get_interactions(parameters[0].id)

def get_player_name(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("getplayername expected no parameters")
    
    return player.name

def fx_wait(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 0:
        raise Exception("fx_wait expected no parameters")
    
    should_continue_wait = True

    while should_continue_wait:
        fxs = [fx for fx in world.current_map.fx_manager.current_fxs if fx.loop != -1]
        
        has_found_unfinished_fx = False

        for fx in fxs:
            if fx.running:
                has_found_unfinished_fx = True

        if has_found_unfinished_fx == False:
            should_continue_wait = False

def set_npc_animation(world, player: Player, program_variables: dict, parameters: list):
    parameters[0].set_animation(parameters[1])

def mul(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"*\" operator expected 2 operands")

    return parameters[0] * parameters[1]

def div(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"/\" operator expected 2 operands")

    return parameters[0] / parameters[1]

def plus(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"+\" operator expected 2 operands")
    
    return parameters[0] + parameters[1]

def minus(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"-\" operator expected 2 operands")

    return parameters[0] - parameters[1]

def mod(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"%\" operator expected 2 operands")

    return parameters[0] % parameters[1]

def int_div(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"//\" operator expected 2 operands")

    return parameters[0] // parameters[1]

def pow_func(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"**\" operator expected 2 operands")

    return parameters[0] ** parameters[1]

def bin_and_func(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"&\" operator expected 2 operands")

    return parameters[0] & parameters[1]

def bin_or_func(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"|\" operator expected 2 operands")

    return parameters[0] | parameters[1]

def bin_xor_func(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"^\" operator expected 2 operands")

    return parameters[0] ^ parameters[1]

def bin_rev_func(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("\"~\" operator expected 1 operand")

    return ~(parameters[0])

def eq(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"eq\" operator expected 2 operands")

    return parameters[0] == parameters[1]

def neq(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"neq\" operator expected 2 operands")

    return parameters[0] != parameters[1]

def neg(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 1:
        raise Exception("\"!\" operator expected 1 operand")

    return not parameters[0]

def and_func(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"&&\" operator expected 2 operands")

    return parameters[0] and parameters[1]

def or_func(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"||\" operator expected 2 operands")

    return parameters[0] or parameters[1]

def greater(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\">\" operator expected 2 operands")

    return parameters[0] > parameters[1]

def smaller(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"<\" operator expected 2 operands")

    return parameters[0] < parameters[1]

def smaller_eq(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\"<eq\" operator expected 2 operands")

    return parameters[0] <= parameters[1]


def greater_eq(world, player: Player, program_variables: dict, parameters: list):
    if len(parameters) != 2:
        raise Exception("\">eq\" operator expected 2 operands")

    return parameters[0] >= parameters[1]

NEG="!"
REV="~"

MUL="*"
DIV="/"
PLUS="+"
MINUS="-"
MOD="%"
INT_DIV="//"
POW="**"
BIN_AND="&"
BIN_OR="|"
XOR="^"
EQ="=="
NEQ="!="
AND="&&"
OR="||"
GREATER=">"
SMALLER="<"
GREATER_EQ=">="
SMALLER_EQ="<="

# Sorted by operator priorities
unary_operators = [
    REV,
    NEG
]

binary_operators = [
    XOR,
    BIN_OR,
    BIN_AND,
    PLUS,
    MINUS,
    MOD,
    POW,
    INT_DIV,
    DIV,
    MUL,
    SMALLER_EQ,
    GREATER_EQ,
    SMALLER,
    GREATER,
    NEQ,
    EQ,
    OR,
    AND
]

native_functions = {
    "credits": show_credits,
    "version": show_version,
    "printf": printf,
    "scanf": scanf,
    "fprintf": fprintf,
    "fscanf": fscanf,
    "tos": tos,
    "messagebox": messagebox,
    "facesetbox": facesetbox,
    "sysexit": sysexit,
    "switch_map": switch_map,
    "fopen": fopen,
    "fclose": fclose,
    "cleanup": cleanup,
    "arradd": arr_add,
    "arrins": arr_ins,
    "arrind": arr_ind,
    "arrpop": arr_pop,
    "arrdel": arr_del,
    "arrclear": arr_clear,
    "arrat": arr_at,
    "arrset": arr_set,
    "unixtimesec": unix_time_sec,
    "unixtimemin": unix_time_min,
    "unixtimehour": unix_time_hour,
    "unixtimeday": unix_time_day,
    "unixtimemonth": unix_time_month,
    "unixtimeyear": unix_time_year,
    "ftoi": ftoi,
    "itof": itof,
    "stoi": stoi,
    "stof": stof,
    "fx_npc": startfx_npc,
    "fx_wait": fx_wait,
    "setnpcx": set_npc_x,
    "setnpcy": set_npc_y,
    "getnpcx": get_npc_x,
    "getnpcy": get_npc_y,
    "getnpcname": get_npc_name,
    "getnpcinteractions": get_npc_interactions,
    "getplayername": get_player_name,
    "setnpcanimation": set_npc_animation,
    MUL: mul,
    DIV: div,
    PLUS: plus,
    MINUS: minus,
    MOD: mod,
    INT_DIV: int_div,
    POW: pow_func,
    BIN_AND: bin_and_func,
    BIN_OR: bin_or_func,
    XOR: bin_xor_func,
    REV: bin_rev_func,
    EQ: eq,
    NEQ: neq,
    NEG: neg,
    AND: and_func,
    OR: or_func,
    GREATER: greater,
    SMALLER: smaller,
    GREATER_EQ: greater_eq,
    SMALLER_EQ: smaller_eq
}