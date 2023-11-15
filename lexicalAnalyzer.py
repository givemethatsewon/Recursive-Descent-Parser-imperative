import myToken as Token
import myParser as Parser

token_count = 0
token_string = ''
next_token = None
input_stream = None
input_char = None
longLexeme = False
#character group: "LETTER", "DIGIT", "ASSIGNMENT_1", "ASSIGNMENT_2", "EXTRA", "NEWLINE", "WHITESPACE", "EOF"
charClass = None

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
            if not Parser.hasErrorOnStatement:
                print("(OK)") 
            else:
                Parser.hasErrorOnStatement = False
                Parser.recentMessage = ""
                
            self.current_line = ""
            self.token_count[0] = self.token_count[1] = self.token_count[2] = 0

tokenCounter = TokenCounter()

#main driver
def lexicalAnalyzer():
    global charClass
    
    getChar()
    Token.print_token(lexical())
    while next_token != Token.EOF:
        Token.print_token(lexical())

def lookup():
    global next_token, tokenCounter
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
    else:    
        print(f'(Error) Lexical Anaylzer :: 정의되지 않은 문자 (" {input_char} ")가 입력되었습니다.')
        next_token = Token.UNKNOWN
    return next_token


def addChar():
    global token_string, input_char, longLexeme
    if len(token_string) < 100:
        token_string += input_char
        return    
    if not longLexeme:
        longLexeme = True
        print("(Warning) Lexical Anaylzer :: Lexeme이 100글자를 초과")
        

def getChar():
    global input_char, tokenCounter
    input_char = input_stream.read(1)
    
    if input_char:
        tokenCounter.appendChar(input_char)

    if not input_char:
        return "EOF"
    elif input_char.isalpha():
        return "LETTER"
    elif input_char.isdigit():
        return "DIGIT"
    elif input_char.isspace():
        if input_char == "\n" or input_char == "\r":
            return "NEWLINE"
        else:
            return "WHITESPACE"
    elif input_char == ":": 
        return "ASSIGNMENT_1"
    elif input_char == "=":
        return "ASSIGNMENT_2"
    else:
        return "EXTRA"

def isWhitespace(ch: str):
    if ch == '\n' or ch == '\r':
        return False
    return ord(ch) <= 32 

def lexical():
    global token_string, next_token, longLexeme, tokenCounter, charClass
    token_string = ""

    # Skip whitespace
    charClass = getChar()
    while charClass == "WHITESPACE":
        charClass = getChar()

    #LETTER
    if charClass == "LETTER":
        addChar()
        charClass = getChar()
        while charClass == "LETTER" or charClass == "DIGIT":
            addChar()
            charClass = getChar()

        tokenCounter.addId()
        next_token = Token.IDENT
        longLexeme = False
        return next_token
    
    #DIGIT
    elif charClass == "DIGIT":
        addChar()
        charClass = getChar()

        while charClass == "DIGIT":
            addChar()
            charClass = getChar()

        tokenCounter.addConst()
        next_token = Token.CONST
        return next_token
    
    #:
    elif charClass == "ASSIGNMENT_1":
        addChar()
        charClass = getChar()
        # =
        if charClass == "ASSIGNMENT_2":
            addChar()
            charClass = getChar()
            next_token = Token.ASSIGN_OP

            return next_token
        
        #경고 발생
        print(f'(Error) Lexical Anaylzer :: 모르는 문자(" {input_char} ")가 입력되었습니다.')
        print('예상했던 문자는 "="입니다.')

        next_token = Token.UNKNOWN
        return next_token
    
    #:없이 =만 입력된 경우
    elif charClass == "ASSIGNMENT_2":
        print(f'(Error) Lexical Anaylzer :: 모르는 문자(" {input_char} ")가 입력되었습니다.')
        print('예상했던 문자는 ":="입니다.')
    
        next_token = Token.UNKNOWN
        return next_token 
    
    #EXTRA(연산기호 등)
    elif charClass == "EXTRA":
        return lookup()

    elif charClass == "NEWLINE":
        next_token = Token.NEWLINE
        return next_token
    
    #EOF
    elif charClass == "EOF":
        next_token = Token.EOF
        return next_token
    
    else:
        next_token = Token.UNKNOWN
        return next_token


