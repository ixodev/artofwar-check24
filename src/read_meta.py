""" Module used for reading meta files, provides functions for string manipulations, etc. """

# Builtin variables

SIZE = "size"
DEFAULT_ANIMATION = "default_animation"

FACESET = "faceset"
IDLE = "idle"
WALK = "walk"
JUMP = "jump"
CHARGE = "charge"
ATTACK = "attack"
DEAD = "dead"
ITEM = "item"
SPECIAL1 = "special1"
SPECIAL2 = "special2"

# lists to store numbers
VAR_ARRAY = [FACESET, IDLE, WALK, CHARGE, ATTACK, JUMP, DEAD, ITEM, SPECIAL1, SPECIAL2]
NUMBERS = [str(x) for x in range(10)]


""" Remove newlines in a string """
def remove_newline(string: str):
    return string.replace('\n', '')

""" Gets the "size" attribute of the meta file """
def compute_size(size: str):
    if not 'x' in size: # like size=16x16 for example
        raise SyntaxError(f"Syntax error: {size}")

    values = size.split('x') # Split string

    if len(values) != 2:
        raise ValueError(f"Value error: {size}. Need 2 values.")

    return (int(remove_newline(values[0])), int(remove_newline(values[1]))) # tuple with size in it

def analyze_line(line: str, variables: dict):
    values = line.split('=') # Separate operands

    if len(values) != 2:
        raise SyntaxError(f"Unknown expression: {line}")

    if values[0] == SIZE:
        variables.update({SIZE: compute_size(values[1])}) # Update dict
        return
    elif values[1].startswith('{'):
        value = values[1]
        value = value[1:]
        if values[1].endswith('\n'):
            value = value[:-2]
        else:
            value = value[:-1]

        variables.update({values[0]: value.split(',')})
        return

    if not values[1] in variables.keys():
        variables.update({remove_newline(values[0]): remove_newline(values[1])}) # Update dict
    else:
        variables.update({remove_newline(values[0]): variables.get(remove_newline(values[1]))}) # Update dict

def read_meta(content: str):
    variables = {}

    lines = content.split('\n')

    for line in lines:
        if not line.startswith('#') and line != '\n' and line != "\n\n" and line != '': # "#" is a comment
            analyze_line(line, variables) # Each line which is not a comment or newline tokens

    return variables # Returns dictionary

def read_meta_file(filename: str):
    file = open(filename)
    content = file.read()
    file.close()

    return read_meta(content)



# Test case, this can be removed
#if __name__ == "__main__":
    #print(read_meta_file("assets/Actor/Character/DarkNinja/animations.meta"))