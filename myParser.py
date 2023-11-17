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

#다음 토큰을 가져오는 함수. NEWLINE을 만나면 재귀적으로 실행되어 다음 토큰을 가져온다.
def getNextToken():
    #backup previous token
    global previousToken, previousTokenString, hasErrorOnStatement, recentMessage

    previousToken = lexicalAnalyzer.next_token
    previousTokenString = lexicalAnalyzer.token_string

    token = lexicalAnalyzer.lexical()
    # if next_token == Token.NEWLINE:
    #     return getNextToken()
    
    # print(f"Next_Token: {next_token}, Token String: {lexicalAnalyzer.token_string}")
    return token



#parser는 resetUntillEnd가 호출되면 lex가 newLine이나 EOF를 만날때까지 계속해서 lex를 호출한다.(consume)
def resetUntillEnd():
    next_token = getNextToken()

    while next_token != Token.NEWLINE and next_token != Token.EOF:
        next_token = getNextToken()
    
    lexicalAnalyzer.tokenCounter.printLine()

    return next_token


#<program> -> <statements>
def program():
    lexicalAnalyzer.charClass = lexicalAnalyzer.getChar() #첫 문자 가져오기
    next_token = getNextToken() #첫 토큰 가져오기
    # print(f"program() next_token: {next_token}, Token String: {lexicalAnalyzer.token_string}")
    # sys.exit(1)
    statements()
    

# <statements> → <statement> | <statement><semi_colon><statement>
def statements():
    global hasErrorOnStatement, recentMessage

    statement()
    lexicalAnalyzer.tokenCounter.printLine() #결과 출력
    
    current_token = lexicalAnalyzer.next_token #현재 토큰

    if current_token == Token.SEMICOLON:    #세미콜론 만남
        next_token = getNextToken() #다음 토큰

        if next_token == Token.EOF:
            hasErrorOnStatement = True
            recentMessage = '(Warning) Parser :: 경고_ 세미콜론 뒤에 주어진 <statement> 없음. 불필요한 ;이 사용되었음'
        statement() 
        lexicalAnalyzer.tokenCounter.printLine() #결과 출력


# <statement>   → <ident><assignment_op><expression>
def statement():
    global hasErrorOnStatement, recentMessage
    
    current_token = lexicalAnalyzer.next_token #현재 토큰
    
    if current_token == Token.IDENT:
        name = lexicalAnalyzer.token_string #현재 토큰(IDENT)의 token_string
        next_token = getNextToken() #다음 토큰
        if next_token == Token.ASSIGN_OP:
            next_token = getNextToken() #다음 토큰
            try:
                parsed_value = expression() 
                symbolTable.setVar(name, parsed_value)

            except TypeError:
                symbolTable.setVar(name, None)
                hasErrorOnStatement = True
                recentMessage = f'(Error) Parser:: 문법 오류_  정의되지 않은 변수가 사용됨'

            except Exception as e:  #expression에서 에러가 발생한 경우
                symbolTable.setVar(name, None)
                hasErrorOnStatement = True
                recentMessage = f'(Error) Parser:: 문법 오류_  RHS에서 오류 {e}.'
        else: #등호가 안 나온 경우
            hasErrorOnStatement = True
            recentMessage = '(Error) Parser :: 문법 오류_ ":=(assignment)"이 없음.'
    else: #ident가 안 나온 경우
        hasErrorOnStatement = True
        recentMessage = '(Error) Parser :: 문법 오류_ statement 형식이 잘못됨.'


# <expression>  → <term><term_tail>
def expression():
    parsed_value = term()

    isPlus = lexicalAnalyzer.token_string == "+"    #boolean, +면 True, -면 False #현재 토큰의 token_string
    if isPlus:
        parsed_value += term_tail()
    else:
        parsed_value -= term_tail()
    return parsed_value

# <term_tail> → <add_op><term><term_tail> | ε
def term_tail():
    global hasErrorOnStatement, recentMessage
    current_token = lexicalAnalyzer.next_token #현재 값
    if current_token == Token.ADD_OP:  # + or -
        next_token = getNextToken() #다음 값
        while next_token == Token.ADD_OP or next_token == Token.MULT_OP:
            hasErrorOnStatement = True
            if "중복연산자" in recentMessage:
                recentMessage = f'(Warning) Parser:: 경고_ 중복연산자 "{lexicalAnalyzer.token_string}" 제거, 추가적으로 {recentMessage}'
            else:
                recentMessage = f'(Warning) Parser:: 경고_ 중복연산자 "{lexicalAnalyzer.token_string}" 제거'

            lexicalAnalyzer.tokenCounter.change_line(lexicalAnalyzer.token_string)
            
            next_token = getNextToken()

        parsed_value = term()
        parsed_value += term_tail()    
        return parsed_value
    return 0    # epsilon case

# <term> → <factor><factor_tail>
def term():
    global recentMessage, hasErrorOnStatement
    parsed_value = factor()
    
    if lexicalAnalyzer.token_string == '*':  #현재 토큰의 toren_string
        parsed_value *= factor_tail()
    elif lexicalAnalyzer.token_string == '/':
        try:
            parsed_value /= factor_tail()
        except ZeroDivisionError:
            hasErrorOnStatement = True
            recentMessage = '(Warning) Parser:: 경고_ 0으로 나누는 경우 발생. 시스템의 최대 정수값으로 처리'
            return sys.maxsize
    return parsed_value


# <factor_tail> → <mult_op><factor><factor_tail> | ε
def factor_tail():
    global hasErrorOnStatement, recentMessage
    current_token = lexicalAnalyzer.next_token #현재 토큰

    if current_token == Token.MULT_OP:  # * or /
        next_token = getNextToken() #다음 토큰
        while next_token == Token.ADD_OP or next_token == Token.MULT_OP:
            hasErrorOnStatement = True
            if "중복 연산자" in recentMessage:
                recentMessage = f'(Warning) Parser:: 경고_ 중복연산자 "{lexicalAnalyzer.token_string}" 제거, 추가적으로 {recentMessage}'
            else:
                recentMessage = f'(Warning) Parser:: 경고_ 중복연산자 "{lexicalAnalyzer.token_string}" 제거'

            lexicalAnalyzer.tokenCounter.change_line(lexicalAnalyzer.token_string)
            next_token = getNextToken()

        parsed_value = factor()
        parsed_value *= factor_tail()
        return parsed_value
    return 1 #epsilon case
    

# <factor> → <left_paren><expression><right_paren> | <ident> | <const>
def factor():
    global hasErrorOnStatement, recentMessage
    current_token = lexicalAnalyzer.next_token #현재 토큰

    if current_token == Token.LEFT_PAREN:
        next_token = getNextToken() #다음 토큰
        parsed_value = expression()
        
        current_token = lexicalAnalyzer.next_token #현재 토큰
        if current_token == Token.RIGHT_PAREN:
            next_token = getNextToken() #다음 토큰
            return parsed_value
        hasErrorOnStatement = True
        recentMessage = '(Error) Parser :: 문법 오류_ ")" 로 괄호가 닫히지 않음'

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
    
    hasErrorOnStatement = True
    recentMessage = f'(Error) Parser :: 문법 오류_ 잘못된 factor ({previousTokenString})이(가) 주어짐, factor는 <left_paren>, 정의된 <ident>, <const> 중 하나가 와야함'

