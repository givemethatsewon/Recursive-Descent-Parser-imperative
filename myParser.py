import sys
import lexicalAnalyzer
import symbolTable
import myToken as Token


hasErrorOnStatement = False
recentMessage = ""

previousToken = -1
previousTokenString = ""

#에러 처리를 위한 함수
def raise_parser_exception(message: str):
    global hasErrorOnStatement, recentMessage
    hasErrorOnStatement = True
    recentMessage = message
    raise Exception(f'(Error) 문법 오류: {message}')

#경고 처리를 위한 함수
def raise_parser_warning(message: str):
    global recentMessage, hasErrorOnStatement
    hasErrorOnStatement = True
    recentMessage = message
    print(f'(Warning) 경고: {message}')

#다음 토큰을 가져오는 함수. NEWLINE을 만나면 재귀적으로 실행되어 다음 토큰을 가져온다.
def getNextToken():
    #backup previous token
    global previousToken, previousTokenString

    previousToken = lexicalAnalyzer.next_token
    previousTokenString = lexicalAnalyzer.token_string

    next_token = lexicalAnalyzer.lexical()
    if next_token == Token.NEWLINE:
        return getNextToken()
    
    print("Next_Token: " + next_token + ", Token String: " + lexicalAnalyzer.token_string)
    return next_token



#parser는 reset이 호출되면 lex가 newLine이나 EOF를 만날때까지 계속해서 lex를 호출한다.(consume)
def resetUntillEnd():
    next_token = lexicalAnalyzer.lexical()

    while next_token != Token.NEWLINE and next_token != Token.EOF and next_token != Token.SEMICOLON:
        next_token = lexicalAnalyzer.lexical()
    
    lexicalAnalyzer.printLine()

    return next_token


#<program> -> <statements>
def program():
    print("Enter program")
    token = getNextToken()
    statements()
    print("Exit program")

# <statements> → <statement> | <statement><semi_colon><statements>
def statements():
    print("Enter statements")
    statement()

    current_token = lexicalAnalyzer.next_token #현재 토큰

    if current_token == Token.SEMICOLON:
        next_token = getNextToken() #다음 토큰
        if next_token == Token.EOF:
            raise_parser_warning('세미콜론 뒤에 주어진 <statement> 없음. 불필요한 ;이 사용되었음')
        statement() #else 있어야하나?
    print("Exit statements")


# <statement>   → <ident><assignment_op><expression>
def statement():
    print("Enter statement")
    current_token = lexicalAnalyzer.next_token #현재 토큰
    
    if current_token == Token.IDENT:
        name = lexicalAnalyzer.token_string #현재 토큰(IDENT)의 token_string
        next_token = getNextToken() #다음 토큰
        if next_token == Token.ASSIGN_OP:
            next_token = getNextToken() #다음 토큰
            try:
                parsed_value = expression() 
                symbolTable.setVar(name, parsed_value)
            except Exception as e:
                raise_parser_exception(str(e))
        else: #등호가 안 나온 경우
            raise_parser_exception('"=(assignment)"이 없음.')
    else: #ident가 안 나온 경우
        raise_parser_exception('statement 형식이 잘못됨.')
    print("Exit statement")


# <expression>  → <term><term_tail>
def expression():
    print("Enter expression")
    parsed_value = term()

    isPlus = lexicalAnalyzer.token_string == "+"    #boolean, +면 True, -면 False #현재 토큰의 token_string
    if isPlus:
        parsed_value += term_tail()
    else:
        parsed_value -= term_tail()
    print("Exit expression")
    return parsed_value

# <term_tail> → <add_op><term><term_tail> | ε
def term_tail():
    print("Enter term_tail")

    current_token = lexicalAnalyzer.next_token #현재 값
    if current_token == Token.ADD_OP:  # + or -
        next_token = getNextToken() #다음 값
        parsed_value = term()
        parsed_value += term_tail()
        print("Exit term_tail")
        return parsed_value
    print("Exit term_tail")
    return 0    # epsilon case

# <term> → <factor><factor_tail>
def term():
    print("Enter term")
    parsed_value = factor()
    
    if lexicalAnalyzer.token_string == '*':  #현재 토큰의 toren_string
        parsed_value *= factor_tail()
    elif lexicalAnalyzer.token_string == '/':
        try:
            parsed_value /= factor_tail()
        except ZeroDivisionError:
            raise_parser_warning('0으로 나누는 경우가 발생. 0, 시스템의 최대 정수값으로 처리')
            return sys.maxsize
    return parsed_value


# <factor_tail> → <mult_op><factor><factor_tail> | ε






