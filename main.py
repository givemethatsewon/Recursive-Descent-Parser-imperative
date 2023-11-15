import sys
import lexicalAnalyzer
import myToken as Token
import myParser as Parser

#python main.py -v input.txt
def main():
    command_line = sys.argv[1:] #[-v, input.txt]/
    try:
        if command_line[-1] != "-v":
            file_name = command_line[-1]
            verbose = True if command_line[0] == "-v" else False
            print("file_name:", file_name, "verbose:", verbose)
        else:
            raise IndexError

        file_handle = open(file_name, "r")
        lexicalAnalyzer.input_stream = file_handle
        if verbose:
            lexicalAnalyzer.lexicalAnalyzer()

        else:
            try:
                while lexicalAnalyzer.next_token != Token.EOF:
                    Parser.program()
            except RuntimeError as e:
                print(e)
                return


    except IndexError:
        print("Invalid arguments in command_line")
        print("Usage: python main.py [-v] <file_name>")
        print("-v: optional, file_name: required")
        return
    
    except FileNotFoundError:
        print("Error: File not found")
        return
    
    finally:
        file_handle.close()


if __name__ == "__main__":
    main()

