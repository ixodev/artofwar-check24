import sys

from i_native_functions import *

PROC = "proc"
ENDPROC = "endproc"
CALL = "()"
COMMENT = "#"
SEP = ";"
EQUAL = "="
ARRAY = "[]"
VARIABLE = "$"
ARRAY_INDEX = "."
MAIN_FUNCTION = "main"
RET = "ret"
INCLUDE = "include"
IF = "if"
ELSE = "else "
CONST = "const"
FORBIDDEN_VARIABLE_NAMES_CHARS = [",", "\t", "+", "-", "*", "/", "%", "[", "]", "{", "}", "\\", "=", "|", "&", "^", ".", ":", ",", "$", "(", ")", "?", "!", "#", "~", "\"", "'", "´", "`", "<", ">"]
PLUS = "+"
MINUS = "-"
MUL = "*"
DIV = "/"
MOD = "%"
AND = "||"
OR = "&&"
NEG = "!"
REV = "~"
BIN_AND = "&"
BIN_OR = "|"
BIN_XOR = "^"
ARITHMETIC_OPERATORS = [MUL, DIV, MOD, PLUS, MINUS]
STRING = "\""
DEFAULT_RETURN_VALUE = 0
VAR = "var"

sys.setrecursionlimit(10**6)

class IPPInterpreter:

    def __init__(self, program_filename: str, world, player: Player):
        self.player = player
        self.world = world
        self.program_filename = program_filename
        self.program = ""
        self.current_conditions = []
        self.current_conditions_values = []
        self.last_finished_condition = ""
        self.conditions_zones = []

        file = open(self.program_filename, "r")
        self.program = file.read()
        file.close()

        self.lines = self.program.split("\n")
        self.rm_identation()

    def rm_identation(self):
        lines_copy = []

        for line in self.lines:
            lines_copy.append(line.strip(" "))

        self.lines = lines_copy

    def search_function(self, line: str, function_name: str):

        # It's then a function declaration
        if line.startswith(PROC + " "):
            tokens = line.split(" ")
            # Function declarations are like this:
            if len(tokens) != 2:
                raise Exception(f"{line} <= invalid syntax")

            # The function name we're searching for
            if tokens[1].split(";")[0] == function_name:
                return True

        return False

    def search_end_function(self, function_name: str):
        line_number = 0 # The line where to find the end function declaration

        for line in self.lines:
            if self.can_be_interpreted(line):
                if line.startswith(ENDPROC):
                    # Because an end function declaration is like: endproc <function>
                    operands = line.split(' ')
                    if operands[1] == function_name:
                        return line_number

            line_number += 1

        return -1

    def can_be_interpreted(self, line: str):
        # If it's not a comment or just a blank line
        return not line.startswith(COMMENT) and line != '\n' and line != "\n\n" and line != ''

    def evaluate_expression(self, expr: str, program_variables: dict):

        expr = expr.strip(" ")

        for operator in unary_operators:
            if expr.startswith(operator):
                operand = expr[1:]
                return native_functions[operator](self.world, self.player,
                                                  program_variables,
                                                  [self.evaluate_expression(operand, program_variables)])

        for operator in binary_operators:
            operands = expr.split(operator)
            if len(operands) == 2:
                return native_functions[operator](self.world, self.player,
                                                  program_variables,
                                                  [self.evaluate_expression(operands[0], program_variables),
                                                   self.evaluate_expression(operands[1], program_variables)])

            if len(operands) != 2 and len(operands) != 1 and len(operands) != 0:
                operands = expr.split(operator, 1)
                return native_functions[operator](self.world, self.player,
                                                  program_variables,
                                                  [self.evaluate_expression(operands[0], program_variables),
                                                   self.evaluate_expression(operands[1], program_variables)])

        if expr in program_variables.keys():
            return program_variables[expr]


        # Try to convert it into a number
        try:
            n = float(expr)

            if n.is_integer():
                
                return int(n)
            
            return n

        except:
            pass

        if expr.startswith(STRING):
            if not expr.endswith(STRING):
                raise Exception(f"{expr} <= \" expected")
            
            if expr == "":
                return expr
            
            return expr[1:-1]

        elif expr.startswith(CALL):
            expr = expr[len(CALL):] # Remove the call symbol
            return self.handle_function_call(expr, program_variables)
        
        elif expr.startswith('(' + CALL):
            expr = expr[len('(' + CALL):-1]
            return self.handle_function_call(expr, program_variables)
    
        elif expr.startswith(';(' + CALL):
            expr = expr[len(';(' + CALL):-1]
            return self.handle_function_call(expr, program_variables)

        raise Exception(f"\"{expr}\" <= unknown expression")

    def is_constant(self, variable_name: str):

        has_found_lowercase = False

        for c in variable_name:
            if not c.isupper() and c != "_":
                has_found_lowercase = True
                break

        return not has_found_lowercase


    def register_variable(self, line: str, program_variables: dict):
        operands = line.split(EQUAL)

        # In the whole function, operands[0] will be the variable name

        if len(operands[0].split(" ")) != 1:
            raise Exception(f"{line} <= variable names cannot contain spaces")

        # In i, variable written in uppercase letters are automatically assigned as constants

        #for c in operands[0]:
         #   if c in FORBIDDEN_VARIABLE_NAMES_CHARS:
          #      raise Exception(f"{line} <= variable name contains forbidden character: {c}")

            # Special case
        if operands[1] == "\n":
            program_variables.update({operands[0]: operands[1]})
            return
        # Make sure we cannot re-assign values to already-defined constant variables
        if operands[0] in program_variables.keys(): # If the variable exists already
            if self.is_constant(operands[0]): # If the variable is a constant
                raise Exception(f"{line} <= cannot re-assign value to constant")

        program_variables.update({operands[0]: self.evaluate_expression(operands[1].replace("\n", "").replace("\n\n", ""), program_variables)})

    def find_closing_expr_function_call(self, tokens: list):
        current_token = 0

        for token in tokens:

            if token.endswith(')'):
                return current_token
            
            current_token += 1

        last_token = len(tokens) - 1
        return last_token

    def check_function_call_as_parameter(self, tokens: list, program_variables: dict):
        current_token = 0

        operands = []
        tokens_copy = []

        for token in tokens:

            if current_token != 0:
                tokens_copy.append(";" + token)
            else:
                tokens_copy.append(token)

            current_token += 1

        tokens.clear()
        tokens = tokens_copy.copy()

        current_token = 0
        jump_next_tokens = 0
        token_jumper_counter = 0

        for token in tokens:
            if jump_next_tokens != 0:
                token_jumper_counter += 1

                if token_jumper_counter == jump_next_tokens:
                    token_jumper_counter = 0
                    jump_next_tokens = 0

            elif token.startswith(";(()") or token.startswith("(()"):
                end_expr = self.find_closing_expr_function_call(tokens)

                listbuilder = tokens[current_token:end_expr + 1]
                stringbuilder = ""

                for e in listbuilder:
                    stringbuilder += e

                operands.append(stringbuilder)

                jump_next_tokens = len(listbuilder) - 1
                token_jumper_counter = 0
            else:
                operands.append(token.replace(";", ""))

            current_token += 1

        return operands

    def handle_function_call(self, line: str, program_variables: dict):
        # Is this line a call of a native function, like log?
        # How can we call functions in the i programming language?
        # ()myfunction;param1;param2;param3, etc.
        # or myfunction;param1;param2;param3
        # So we split the line by ";" and look for the first token, if it's an existing function name
        # First we look into the dictionary of the native functions, defined in i_native_functions.py

        tokens = line.split(SEP)
        function_to_call = tokens[0]
        tokens = tokens[1:]  # Remove the function name, we just want the parameters, function name is in function_to_call

        operands = self.check_function_call_as_parameter(tokens, program_variables)

        # parameters given to the function with the evaluated expressions
        parameters = []


        # evaluate all the parameters given as expressions
        for operand in operands:
            parameter = self.evaluate_expression(operand, program_variables)
            parameters.append(parameter)

        if function_to_call in native_functions.keys():
            return native_functions[function_to_call](self.world, self.player, program_variables,
                                               parameters)  # Call the function located in the native_functions dict

        return self.call_i_function(function_to_call, parameters)

    def find_endif(self, start_if: int):

        n = 0

        for line in self.lines:
            if self.can_be_interpreted(line):

                if line.startswith("}") and n > start_if:
                    return n

            n += 1

    # Returns true if condition should be executed or not
    def analyze_conditions(self, line: str, program_variables: dict):
        if len(self.current_conditions_values) == 0:
            return True

        if self.current_conditions_values[-1]:
            return True
        else:
            return False
        


    def analyze_line(self, line: str, program_variables: dict, line_number: int):

        if not self.can_be_interpreted(line):
            return

        if line == "}":
            try:
                self.last_finished_condition = self.current_conditions[-1]
                self.current_conditions.pop(-1)
                self.current_conditions_values.pop(-1)
                self.conditions_zones.pop(-1)
            except IndexError:
                raise Exception(f"\"{line}\" <= wasn't expected")
            return

        if line.startswith(ELSE):
            if not line.endswith("{"):
                raise Exception(line + " <= \"{\" expected")

            if self.analyze_conditions(line, program_variables):
                self.current_conditions.append("")
                self.current_conditions_values.append(not self.evaluate_expression(self.last_finished_condition, program_variables))
                self.conditions_zones.append(False)
            else:
                self.current_conditions.append("")
                self.current_conditions_values.append(False)
                self.conditions_zones.append(False)

            return

        #self.last_finished_condition = ""

        if line.startswith(IF):
            if not line.endswith("{"):
                raise Exception(f"{line}: \"(\" expected")

            if self.analyze_conditions(line, program_variables):
                self.current_conditions.append(line.split(" ")[1])
                self.current_conditions_values.append(self.evaluate_expression(line.split(" ")[1], program_variables))
                self.conditions_zones.append(False)
            else:
                self.current_conditions.append("")
                self.current_conditions_values.append(False)
                self.conditions_zones.append(False)
            
            return

        if self.analyze_conditions(line, program_variables) == False:
            return

        if line.startswith(RET):
            c = line.replace(" ", "")

            if c == RET:
                return DEFAULT_RETURN_VALUE

            return self.evaluate_expression(line.split(" ", 1)[1], program_variables)

        # Then register a variable, because of the use of the assignment operator
        if line.startswith(VAR + " "):
            self.register_variable(line.split(" ", 1)[1], program_variables)
            return

        # You can call functions like myfunction;param1;param2
        # But you can also call like this: ()myfunction;param1;param2
        # NB: When calling function in an expression, () symbol is mandatory

        if line.startswith(CALL):
            # We write line[len(CALL):] to remove the call symbol
            self.handle_function_call(line[len(CALL):], program_variables)
            return
        
        if len(line.split('=')) != 0:
            parts = line.split('=')

            if parts[0] in program_variables:
                program_variables.update({parts[0]: self.evaluate_expression(parts[1], program_variables)})
                return

        # Else, try to call the function
        self.handle_function_call(line, program_variables)


    def fill_in_with_builtin_variables(self, function_name: str, program_variables: dict):

        program_variables.update({"NULL": None})

        self.register_variable(f"TRUE=1", program_variables)
        self.register_variable(f"FALSE=2", program_variables)

        self.register_variable(f"NEWLINE=\"\n\"", program_variables)
        self.register_variable(f"TAB=\"\t\"", program_variables)
        self.register_variable(f"ANTISLASH=\"\\\"", program_variables)
        self.register_variable(f"QUOTE=\"\"\"", program_variables)

        program_variables.update({"STDOUT": sys.stdout})
        program_variables.update({"STDERR": sys.stderr})
        program_variables.update({"STDIN": sys.stdin})

        self.register_variable(f"MESSAGEBOX_OK={MESSAGEBOX_OK}", program_variables)
        self.register_variable(f"MESSAGEBOX_OK_CANCEL={MESSAGEBOX_OK_CANCEL}", program_variables)
        self.register_variable(f"MESSAGEBOX_YES_NO={MESSAGEBOX_YES_NO}", program_variables)
        self.register_variable(f"MESSAGEBOX_YES_NO_CANCEL={MESSAGEBOX_YES_NO_CANCEL}", program_variables)
        self.register_variable(f"MESSAGEBOX_OK_YES_STATUS={MESSAGEBOX_OK_YES_STATUS}", program_variables)
        self.register_variable(f"MESSAGEBOX_NO_STATUS={MESSAGEBOX_NO_STATUS}", program_variables)
        self.register_variable(f"MESSAGEBOX_CANCEL_STATUS={MESSAGEBOX_CANCEL_STATUS}", program_variables)

        self.register_variable(f"MESSAGEBOX_STANDARD={MESSAGEBOX_STANDARD}", program_variables)
        self.register_variable(f"MESSAGEBOX_FACESET={MESSAGEBOX_FACESET}", program_variables)

        self.register_variable(f"DEFAULT_FACESET=\"{MESSAGEBOX_DEFAULT_FACESET}\"", program_variables)

        #program_variables.update({"CURRENT_MAP_FILENAME": world.current_map.filename})
        #program_variables.update({"CURRENT_MAP_PATH": world.current_map.map_path})
        #program_variables.update({"CURRENT_FUNCTION_NAME": function_name})

    def check_functions(self):
        function_names = []
        function_name = ""

        for line in self.lines:
            if line.startswith(PROC):
                function_name = line.split(" ")[1]

                if function_name in function_names:
                    raise Exception(f"{function_name} <= exists already")

                function_names.append(function_name)


    def init_function_parameters(self, signature: str, parameters: list, program_variables: dict):
        parameters_names = signature.split(" ")[1].split(SEP)[1:]

        if len(parameters) != len(parameters_names):
            raise Exception(f"{signature.split(' ')[1].split(';')[0]} expected {len(parameters_names)} parameters")

        for x in range(len(parameters_names)):
            program_variables.update({parameters_names[x]: parameters[x]})


    def call_i_function(self, function_name: str, parameters: list):


        self.check_functions()

        start_function_line_number = 0
        has_found_function = False

        for line in self.lines:
            if self.can_be_interpreted(line): # "#" is a comment
                # Search function declaration
                if self.search_function(line, function_name): # Each line which is not a comment or newline tokens
                    has_found_function = True
                    break

            start_function_line_number += 1 # Current line

        if not has_found_function:
            raise Exception(f"{function_name} <= unknown expression")

        # Then search end function declaration
        end_function_line_number = self.search_end_function(function_name)
        if end_function_line_number == -1:
            raise Exception(f"function {function_name} has no end declaration")


        # Initialize variables dictionary
        program_variables = {}
        self.fill_in_with_builtin_variables(function_name, program_variables)
        self.init_function_parameters(self.lines[start_function_line_number], parameters, program_variables)

        # Execute all lines from the point where we found the function declaration line to the end function declaration
        # We don't need to execute the start function declaration so I add + 1 to the start value in the range
        # Same for end function declaration, so I don't add + 1 to end value in the range
        for i in range(start_function_line_number + 1, end_function_line_number):
            result = self.analyze_line(self.lines[i], program_variables, i)

            if result != None:
                return result

    def import_modules(self):

        for l in self.lines:
            if l.startswith(INCLUDE):
                line = l.replace("\n", "") # Remove newlines

                operands = line.split(" ") # operands[0] is include directive, operands[1] is the module to import

                if len(operands) != 2:
                    raise Exception(f"{line} <= invalid statement")

                try:
                    file = open(f"{operands[1]}.ipp")
                    content = file.read()
                    file.close()
                except IOError:
                    raise Exception(f"{line} <= could not include module")

                program = "\n" + self.program + "\n" + content # Replace include directive with program content, insert newlines for safety
                program = program.replace(line, "") # Remove include directive

    def exec_program_as_string(self):
        
        try:
            #import_modules(program)
            result = self.call_i_function("main", [])
            if result is None:
                result = 0
            return result
        except Exception as err:
            print(f"I Interpreter - fatal error: {err}", file=sys.stderr)
            return 1
        

    def exec_function(self, function_name: str, parameters: list):
        try:
            #import_modules(program)
            result = self.call_i_function(function_name, parameters)
            if result is None:
                result = 0
            return result
        except Exception as err:
            print(f"I Interpreter - fatal error: {err}", file=sys.stderr)
            return 1


        return self.call_i_function(function_name, parameters)

    def run(self):

        if self.world is None or self.player is None:
            print("/!\\ Warning: i++ is running in GI-mode", file=sys.stderr)
        
        result = self.exec_program_as_string()
        print(f"\nProgram finished with exit code {result}\n\n")





