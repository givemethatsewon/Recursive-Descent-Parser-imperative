import myToken as Token
import myParser as Parser

token_string = None
next_token = None
input_stream = None
input_char = ''
lexeme = []
charClass = None

CHAR_GROUP = {
    "LETTER": 0,
    "DIGIT": 1,
    "ASSIGNMENT_1": 2,
    "ASSIGNMENT_2": 3,
    "EXTRA": 4,
    "WHITESPACE": 5,
    "NEWLINE": 6,
    "EOF": 7,
    "UNKNOWN": 8
}

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
        if ch != '\n':
            self.current_line += ch
    
    def change_line(self, ch: str):
        self.current_line = self.current_line.replace(f" {ch}", "", 1)
        self.token_count[self.op_idx] -= 1

    def printLine(self):
        if self.current_line.strip() != "":
            print(self.current_line)
            print(f'ID: {self.token_count[self.id_idx]}; CONST: {self.token_count[self.const_idx]}; OP: {self.token_count[self.op_idx]};')
            if not Parser.hasErrorOnStatement:
                print("(OK)") 
            else:
                print(Parser.recentMessage)
                Parser.hasErrorOnStatement = False #출력하고 에러 플래그 초기화
                Parser.recentMessage = ""   #출력하고 현재 에러 메세지 초기화
            self.current_line = ""
            self.token_count[0] = self.token_count[1] = self.token_count[2] = 0

tokenCounter = TokenCounter()

#-v 옵션을 사용할 경우 호출되는 함수
def lexicalAnalyzer():
    global charClass
    
    charClass = getChar()
    Token.print_token(lexical())
    while next_token != Token.EOF:
        Token.print_token(lexical())



#addChar - a function to add input_char(nextChar) to lexeme
def addChar():
    global lexeme
    lexeme.append(input_char)
        

#getChar - a function to get the next character of input and returns its character class
def getChar():
    global input_char, tokenCounter, input_stream

    input_char = input_stream.read(1)
    
    if input_char:
        tokenCounter.appendChar(input_char)
        if input_char.isalpha():
            return CHAR_GROUP["LETTER"]
        elif input_char.isdigit():
            return CHAR_GROUP["DIGIT"]
        elif input_char.isspace():
            if input_char == '\n':
                return CHAR_GROUP["NEWLINE"]
            else:
                return CHAR_GROUP["WHITESPACE"]
        elif input_char == ":": 
            return CHAR_GROUP["ASSIGNMENT_1"]
        elif input_char == "=":
            return CHAR_GROUP["ASSIGNMENT_2"]
        else:
            return CHAR_GROUP["EXTRA"]
    else:
        return CHAR_GROUP["EOF"]




#lexical - a simple lexical analyzer for expressions
def lexical():
    global next_token, token_string, charClass, lexeme, tokenCounter, input_char    
    #skip whitespace
    while input_char.isspace():
        charClass = getChar()

    #IDENT
    if charClass == CHAR_GROUP["LETTER"]:
        addChar()
        charClass = getChar()
        while charClass == CHAR_GROUP["LETTER"] or charClass == CHAR_GROUP["DIGIT"]:
            addChar()
            charClass = getChar()
        next_token = Token.IDENT
        tokenCounter.addId()    #ID 카운트 증가
    
    #CONST
    elif charClass == CHAR_GROUP["DIGIT"]:
        addChar()
        charClass = getChar()
        while charClass == CHAR_GROUP["DIGIT"]:
            addChar()
            charClass = getChar()
        next_token = Token.CONST
        tokenCounter.addConst() #CONST 카운트 증가
    
    elif charClass == CHAR_GROUP["ASSIGNMENT_1"]:
        addChar()
        charClass = getChar()
        if charClass == CHAR_GROUP["ASSIGNMENT_2"]:
            addChar()
            charClass = getChar()
            next_token = Token.ASSIGN_OP

        else:
            print(f'(Error) Lexical Anaylzer :: 모르는 문자(" {input_char} ")가 입력되었습니다.')
            print('예상했던 문자는 "="입니다.')
            next_token = Token.UNKNOWN

    
    elif charClass == CHAR_GROUP["ASSIGNMENT_2"]:   #틀린 파싱이므로 addChar()를 하지 않는다.
        print(f'(Error) Lexical Anaylzer :: 모르는 문자(" {input_char} ")가 입력되었습니다.')
        print('예상했던 문자는 ":="입니다.')
        next_token = Token.UNKNOWN
    
    elif charClass == CHAR_GROUP["NEWLINE"]:
        next_token = Token.NEWLINE
        charClass = getChar()
    
    elif charClass == CHAR_GROUP["EXTRA"]:
        ch = input_char
        if ch == '+' or ch == '-':
            tokenCounter.addOp()    #OP 카운트 증가
            next_token = Token.ADD_OP
        elif ch == '*' or ch == '/':
            tokenCounter.addOp()    #OP 카운트 증가
            next_token = Token.MULT_OP
        elif ch == '(':
            tokenCounter.addOp()    #OP 카운트 증가
            next_token = Token.LEFT_PAREN
        elif ch == ')':
            tokenCounter.addOp()    #OP 카운트 증가
            next_token = Token.RIGHT_PAREN
        elif ch == ';':
            next_token = Token.SEMICOLON
        else:    
            print(f'(Error) Lexical Anaylzer :: 정의되지 않은 문자 (" {input_char} ")가 입력되었습니다.')
            next_token = Token.UNKNOWN
        addChar()
        charClass = getChar()
    
    elif charClass == CHAR_GROUP["EOF"]:
        next_token = Token.EOF
        lexeme.append('EOF')
    
    token_string = ''.join(lexeme)
    lexeme = []
    return next_token


