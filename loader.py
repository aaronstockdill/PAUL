import os

def load():
    files = [file[:-3] for file in os.listdir("Modules/") 
             if file != "__init__.py" 
             and file != "__pycache__"
             and file != "importer.py"]
    importer = open("Modules/importer.py", 'w')
    for file in files:
        importer.write("import Modules.{0} as {0}\n".format(file))
    importer.write("\nimport vocab\nvocab.add_new()")
    importer.close()
        

load()