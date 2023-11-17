import sys
import lexicalAnalyzer
import myToken as Token
import myParser as Parser
import symbolTable

#python main.py -v input.txt
def main():
    command_line = sys.argv[1:] #[-v, input.txt]
    # print(command_line)
    try:
        if command_line[-1] != "-v":
            file_name = command_line[-1]
            verbose = True if command_line[0] == "-v" else False
        else:
            raise IndexError

        file_handle = open(file_name, "r")
        lexicalAnalyzer.input_stream = file_handle

        if verbose:
            lexicalAnalyzer.lexicalAnalyzer()

        else:
            while lexicalAnalyzer.next_token != Token.EOF:
                try:
                    Parser.program()
                except RuntimeError as e:
                    if Parser.resetUntillEnd() == Token.EOF:
                        print(e)
                        break
            # lexicalAnalyzer.tokenCounter.printLine() #결과 출력
            print('Result ==>', end=" ")
            for key, value in symbolTable.symbolTable.items():
                value = value if value else "Unknown"
                print(f'{key}: {value};', end=" ")



    except IndexError:
        print("Invalid arguments in command_line")
        print("Usage: python main.py [-v] <file_name>")
        print("-v: optional, file_name: required")
        return
    
    except FileNotFoundError:
        print("Error: File not found")
        return
    
    else:
        file_handle.close()
        return
    



if __name__ == "__main__":
    main()