CONST = 0  # "[09]+"
IDENT = 1  # "LETTER[LETTER | DIGIT]*"
ASSIGN_OP = 2  # ":="
SEMICOLON = 3  # ";"
ADD_OP = 4  # "[+ | -]"
MULT_OP = 5  # "[* | /]"
LEFT_PAREN = 6  # "("
RIGHT_PAREN = 7  # ")"
NEWLINE = 8  # "[\n]"
EOF = 98  # "EOF"
UNKNOWN = 99  # Exception

def print_token(t: int):
    if t == CONST:
        print("CONST")
    elif t == IDENT:
        print("IDENT")
    elif t == ASSIGN_OP:
        print("ASSIGN_OP")
    elif t == SEMICOLON:
        print("SEMICOLON")
    elif t == ADD_OP:
        print("ADD_OP")
    elif t == MULT_OP:
        print("MULT_OP")
    elif t == LEFT_PAREN:
        print("LEFT_PAREN")
    elif t == RIGHT_PAREN:
        print("RIGHT_PAREN")
    elif t == NEWLINE:
        print("NEWLINE")
    elif t == EOF:
        print("EOF")
    elif t == UNKNOWN:
        print("UNKNOWN")
    else:
        print(f"Error: Unknown token {t}")

    