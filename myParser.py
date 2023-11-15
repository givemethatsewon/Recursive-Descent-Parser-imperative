import sys
import lexicalAnalyzer
import symbolTable
import myToken as Token

#TODO 세미콜론 없는 경우 경고 만들고 parsing 계속하도록
#전역 변수 - 함수 내에서 조회할 땐 그냥 쓰되 함수 내에서 전역 변수에 값 변경이 일어나야하면 global로 선언하고 사용
hasErrorOnStatement = False
recentMessage = ""

previousToken = -1
previousTokenString = ""

#에러 처리를 위한 함수
def raise_parser_exception(message: str):
    global hasErrorOnStatement, recentMessage
    hasErrorOnStatement = True
    recentMessage = message
    raise Exception(f'(Error) Parser :: 문법 오류 {message}')

#경고 처리를 위한 함수
def raise_parser_warning(message: str):
    global recentMessage, hasErrorOnStatement
    hasErrorOnStatement = True
    recentMessage = message
    print(f'(Warning) Parser :: {message}')

#다음 토큰을 가져오는 함수. NEWLINE을 만나면 재귀적으로 실행되어 다음 토큰을 가져온다.
def getNextToken():
    #backup previous token
    global previousToken, previousTokenString

    previousToken = lexicalAnalyzer.next_token
    previousTokenString = lexicalAnalyzer.token_string

    next_token = lexicalAnalyzer.lexical()
    if next_token == Token.NEWLINE:
        return getNextToken()
    
    # print(f"Next_Token: {next_token}, Token String: {lexicalAnalyzer.token_string}")
    return next_token



#parser는 reset이 호출되면 lex가 newLine이나 EOF를 만날때까지 계속해서 lex를 호출한다.(consume)
def resetUntillEnd():
    next_token = lexicalAnalyzer.lexical()

    while next_token != Token.NEWLINE and next_token != Token.EOF and next_token != Token.SEMICOLON:
        next_token = lexicalAnalyzer.lexical()
    
    lexicalAnalyzer.tokenCounter.printLine()

    return next_token


#<program> -> <statements>
def program():
    print("Enter program")
    token = getNextToken() #첫 토큰 가져오기
    statements()
    print("Exit program")

# <statements> → <statement> | <statement><semi_colon><statements>
def statements():
    print("Enter statements")
    statement()
    current_token = lexicalAnalyzer.next_token #현재 토큰

    lexicalAnalyzer.tokenCounter.printLine() #결과 출력
    if current_token == Token.SEMICOLON:
        next_token = getNextToken() #다음 토큰
        if next_token == Token.EOF:
            raise_parser_warning('세미콜론 뒤에 주어진 <statement> 없음. 불필요한 ;이 사용되었음')
        statement() 
        lexicalAnalyzer.tokenCounter.printLine() #결과 출력
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
def factor_tail():
    print("Enter factor_tail")
    current_token = lexicalAnalyzer.next_token #현재 토큰

    if current_token == Token.MULT_OP:  # * or /
        next_token = getNextToken() #다음 토큰
        parsed_value = factor()
        parsed_value *= factor_tail()
        print("Exit factor_tail")
        return parsed_value
    
    print("Exit factor_tail")
    return 1 #epsilon case
    

# <factor> → <left_paren><expression><right_paren> | <ident> | <const>
def factor():
    print("Enter factor")
    global hasErrorOnStatement
    current_token = lexicalAnalyzer.next_token #현재 토큰

    if current_token == Token.LEFT_PAREN:
        next_token = getNextToken() #다음 토큰
        parsed_value = expression()
        
        current_token = lexicalAnalyzer.next_token #현재 토큰
        if current_token == Token.RIGHT_PAREN:
            next_token = getNextToken() #다음 토큰
            return parsed_value
        raise_parser_exception('")" 로 괄호가 닫히지 않음')
    elif current_token == Token.IDENT:
        name = lexicalAnalyzer.token_string #현재 토큰(IDENT)의 token_string
        next_token = getNextToken() #다음 토큰
        if symbolTable.hasKey(name) and symbolTable.getValue(name):
            return symbolTable.getValue(name)
        symbolTable.setVar(name, None)
    elif current_token == Token.CONST:
        const = int(lexicalAnalyzer.token_string) #현재 토큰(CONST)의 token_string
        next_token = getNextToken() #다음 토큰
        return const
    else:
        #가장 작은 단위인 factor에서 연산자 중복 처리
        current_token = lexicalAnalyzer.next_token  #현재 토큰
        if (previousToken == Token.ADD_OP or previousToken == Token.MULT_OP) and (current_token == Token.ADD_OP or current_token == Token.MULT_OP):
            if "중복 연산자" in recentMessage:
                recentMessage = f'"중복연산자" {lexicalAnalyzer.token_string} 제거, 추가적으로 {recentMessage}'
            else:
                recentMessage = f'"중복연산자" {lexicalAnalyzer.token_string} 제거'

        #Token Counter 중복 연산자 제거, 여러개 중복까지 대응
        temp = lexicalAnalyzer.tokenCounter.current_line
        toReplace = lexicalAnalyzer.token_string
        lastIdx = temp.rfind(toReplace)
        firstIdx = temp.find(toReplace)
        #슬라이싱 사용
        temp = temp[:firstIdx] + toReplace + temp[lastIdx+1:]

        lexicalAnalyzer.tokenCounter.current_line = temp
        hasErrorOnStatement = True
        return factor()
    raise_parser_exception(f'잘못된 factor ({previousTokenString})이(가) 주어짐, factor는 <left_paren>, <ident>, <const> 중 하나가 와야함')

