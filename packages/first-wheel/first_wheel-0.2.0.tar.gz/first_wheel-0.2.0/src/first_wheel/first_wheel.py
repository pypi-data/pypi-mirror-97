"""
Usage:
    first_wheel.py -v|--version
    first_wheel.py -h|--help
    first_wheel.py -i|--info

Options:
    -h --help       # Show usage.
    -v --version    # Show version.
"""
import sys
import docopt
version = "0.2.0"

def first_wheel(argv):
    dargs = docopt.docopt(__doc__, argv = argv)
    #print(dargs)
    if dargs.get("--version") == True or dargs.get("-v") == True:
        global version
        print("version:", version)
    elif dargs.get("--info") == True or dargs.get("-i") == True:
        with open("./config/info.cfg", "r") as f:
            print("info:", f.read())
            pass
    else:
        pass
    pass

def main():
    try:
        first_wheel(sys.argv[1:])
    except:
        pass
    pass

if __name__ == "__main__":
    main()
    pass