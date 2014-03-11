from sys import argv

if len(argv) > 1:
    if argv[1] == "-nw" or argv[1] == "-qnw":
        import cli
    elif argv[1] == "-h":
        print("USAGE:\n    paul [-nw|-h] [input]\n\n" 
              + "    -nw : Run in command line mode.\n"
              + "    -qnw: Run in command line mode without a splash. No input after this.\n"
              + "    -h  : Show this help.")
    else:
        import gui
else:
    import gui