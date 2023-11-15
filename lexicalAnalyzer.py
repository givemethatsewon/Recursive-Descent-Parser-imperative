import myToken as Token

token_count = 0
token_string = ''
next_token = None
input_stream = None
input_char = None
longLexeme = False


char_group = {
    "LETTER": 0,
    "DIGIT": 1,
    "ASSIGNMENT_1": 2,
    "ASSIGNMENT_2": 3,
    "EXTRA": 4,
    "NEWLINE": 5,
    "WHITESPACE": 6,
    "EOF": 7
}

def addChar():
    global token_string, input_char, longLexeme
    if len(token_string) < 100:
        token_string += input_char
        return    
    if not longLexeme:
        longLexeme = True
        print("(Warning) Lexical Anaylzer :: Lexeme이 100글자를 초과")
        

def getChar(add: bool):
    global input_char
    input_char = input_stream.read(1)
    
    if add:
        addChar()
    
    if not input_char:
        return char_group["EOF"]
    elif input_char.isalpha():
        return char_group["LETTER"]
    elif input_char.isdigit():
        return char_group["DIGIT"]
    elif input_char.isspace():
        if input_char == "\n" or input_char == "\r":
            return char_group["NEWLINE"]
        else:
            return char_group["WHITESPACE"]
    elif input_char == ":": 
        return char_group["ASSIGNMENT_1"]
    elif input_char == "=":
        return char_group["ASSIGNMENT_2"]
    else:
        return char_group["EXTRA"]

def isWhitespace(ch: str):
    if ch == '\n' or ch == '\r':
        return False
    return ord(ch) <= 32 

def lexical():
    global token_string, next_token, longLexeme, input_char, tokenCounter
    token_string = ""
    charClass = getChar(False)

    # Skip whitespace
    while charClass == char_group["WHITESPACE"]:
        charClass = getChar(False)

    #LETTER
    if charClass == char_group["LETTER"]:
        addChar()
        charClass = getChar(True)

        while charClass == char_group["LETTER"] or charClass == char_group["DIGIT"]:
            getChar(False)
            addChar()
            charClass = getChar(True)
        
        tokenCounter.addId()
        next_token = Token.IDENT
        longLexeme = False
        return next_token
    
    elif charClass == char_group["DIGIT"]:
        addChar()
        charClass = getChar(True)

        while charClass == char_group["DIGIT"]:
            getChar(False)
            addChar()
            charClass = getChar(True)

        tokenCounter.addConst()
        next_token = Token.CONST
        return next_token
    
    elif charClass == char_group["ASSIGNMENT_1"]:
        addChar()
        charClass = getChar(False)
        if charClass == char_group["ASSIGNMENT_2"]:
            addChar()
            charClass = getChar(True)
            next_token = Token.ASSIGN_OP
            return next_token
        
        print(f'(Error) Lexical Anaylzer :: 모르는 문자(" {input_char} ")가 입력되었습니다.')
        print('  예상했던 문자는 "="입니다.')

        next_token = Token.UNKNOWN
        return next_token
    
    elif charClass == char_group["ASSIGNMENT_2"]:
        print(f'(Error) Lexical Anaylzer :: 모르는 문자(" {input_char} ")가 입력되었습니다.')
        print('  예상했던 문자는 ":="입니다.')
        
    elif charClass == char_group["EXTRA"]:
        addChar()
        c = token_string[0]
        if ord(c) <= 32:
            return lexical()
        elif c == '+' or c == '-':
            tokenCounter.addOp()
            next_token = Token.ADD_OP
        elif c == '*' or c == '/':
            tokenCounter.addOp()
            next_token = Token.MULT_OP
        elif c == '(':
            tokenCounter.addOp()
            next_token = Token.LEFT_PAREN
        elif c == ')':
            tokenCounter.addOp()
            next_token = Token.RIGHT_PAREN
        elif c == ';':
            next_token = Token.SEMICOLON
        
        print(f'(Error) Lexical Anaylzer :: 모르는 문자(" {input_char} ")가 입력되었습니다.')
        next_token = Token.UNKNOWN
        return next_token
    
    elif charClass == char_group["NEWLINE"]:
        next_token = Token.NEWLINE
        return next_token
    
    elif charClass == char_group["EOF"]:
        next_token = Token.EOF
        return next_token
    
    else:
        next_token = Token.UNKNOWN
        return next_token


class TokenCounter:
    id_idx = 0
    const_idx = 1
    op_idx = 2

    current_line = ""
    token_count = [0, 0, 0]

    def addId(self):
        self.token_count[self.id_idx] += 1
    
    def addConst(self):
        self.token_count[self.const_idx] += 1
    
    def addOp(self):
        self.token_count[self.op_idx] += 1
    
    def appendChar(self, ch: str):
        if ch != '\n' and ch != '\r':
            self.current_line += ch

    def printLine(self):
        if self.current_line.strip() != "":
            print(self.current_line)
            print(f'ID: {self.token_count[self.id_idx]}; CONST: {self.token_count[self.const_idx]}; OP: {self.token_count[self.op_idx]};')
            self.current_line = ""
            self.token_count[0] = self.token_count[1] = self.token_count[2] = 0


tokenCounter = TokenCounter()