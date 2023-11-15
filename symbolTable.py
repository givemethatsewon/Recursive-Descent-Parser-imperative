symbolTable = {}

def hasKey (key: str):
    return key in symbolTable

def getValue(key: str):
    return symbolTable.get(key)    #없으면 keyError가 아니라 None을 반환

def setVar(key: str, value: int):
    symbolTable[key] = value

def printSymbolTable():
    keys = sorted(symbolTable.keys())
    for key in keys:
        value = getValue(key)
        if value:
            print(f'{key}: {value};', end="")
        else:
            print(f'{key}: Unknown;', end="")