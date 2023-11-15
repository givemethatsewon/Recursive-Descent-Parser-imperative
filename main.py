import sys
import lexicalAnalyzer
import myToken
import myParser

#python main.py -v input.txt
def main():
    # command_line = sys.argv[1:] #[-v, input.txt]/
    command_line = ["-v", "inputs/eval1.in.txt"]
    try:
        if command_line[-1] != "-v":
            file_name = command_line[-1]
            verbose = True if command_line[0] == "-v" else False
            print("file_name: ", file_name, "verbose: ", verbose)
        else:
            raise IndexError

        if verbose:
            file_handle = open(file_name, "r")
            lexicalAnalyzer.lexicalAnalyzer(file_handle)




    except IndexError:
        print("Invalid arguments in command_line")
        print("Usage: python main.py [-v] <file_name>")
        print("-v: optional, file_name: required")
        return
    
    except FileNotFoundError:
        print("Error: File not found")
        return
    
    except RuntimeError as e:
        print(e)
        return
    

if __name__ == "__main__":
    main()

