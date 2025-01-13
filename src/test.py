def split_expression_util(string: str, positions_to_split: list, sep: str):
    substrs = []
    seps_to_split_pos = []
    
    current_sep = 0
    char_number = 0

    for char in string:

        if char == sep:
            
            if current_sep in positions_to_split:
                
                if current_sep == 0:
                    substrs.append(string[:char_number])
                else:
                    substrs.append(string[seps_to_split_pos[-1] + 1:char_number])

                seps_to_split_pos.append(char_number)

            current_sep += 1

        char_number += 1


    substrs.append(string[seps_to_split_pos[-1] + 1:])
        

    return substrs


print(split_expression_util("hello;world;guys;i;hate;you;gogo;", [0, 2, 3, 6], ";"))