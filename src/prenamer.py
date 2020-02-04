''' http://python.org/dev/peps/pep-0263/
encoding: utf-8
Pattern Renamer
This application renames and organizes files imported from iPhones or Nikon cameras.
It can be easily extended to support other types of imports. The purpose of the 
application is to rename files from their original names, e.g. IMG_123.JPG to something
easier to relate to, as a date. The files will be named according to the date of creation
plus the name of the folder they are stored in. This makes it easier to catalog the files,
without having several hundred files named exactly the same on your drive. In case of a 
drive failure, individual file naming could come in handy, but it's also easier to know 
from which album this particular photo is.

Copyright 2012 Adrian Bastholm adrian@javaguru.org

MIT License

'''
import os, sys, locale, re, shutil, time, datetime


if __name__ == '__main__':
    pass

print("Pattern renamer application")


locale.setlocale(locale.LC_ALL,"sv_SE.UTF-8")
print("Encoding: " + sys.stdout.encoding)
print(sys.stdout)
print([(k, os.environ[k]) for k in os.environ if k.startswith('LC')])
print([(k, os.environ[k]) for k in os.environ if k.startswith('LANG')])
print(locale.getlocale())
#print('\u00e5')
#print('\u0061\u030a')
print("\n")

reallyDo = False
method = "ctime"
#iPhone saves as JPG and MOV 
handledExtensions = set([".JPG", ".MOV"])
#Nikon and iPhone file names handled by default. Add patterns here to extend
handledPatterns = set(["DSC","CSC","IMG"])

def getBaseDirName(path):
    return os.path.basename(os.path.abspath(path))

def isHandledType(path):
    (name,ext) = os.path.splitext(path)
    if ext.upper() in handledExtensions:
        return True
    else:
        return False

def getMediaPrefix(path):
    if '.' in path:
        (name,ext) = os.path.splitext(path)
        return name[0:3]
    else:
        return None
    
''' Find JPG files not already renamed to yyyy-mm-dd pattern '''
def match(path):
    # pattern 0000-00-00--sometext
    pattern = re.compile('\d{4}-\d{2}-\d{2}--\w*')
    if re.match(pattern, path):
        print("Path date pattern match : " + path)
        return False
    else:
        if path[0:3] in handledPatterns:
            return True
        else:
            return False

def getCreationTime(filename):
    time = os.path.getctime(filename)
    return datetime.date.fromtimestamp(time)

def traverse (targetDir):
    currentDir = targetDir
    dirs = os.listdir(targetDir)
    for entry in dirs:
        if os.path.isdir(os.path.join(currentDir,entry)):
            print("Traversing " + os.path.join(targetDir,entry))
            traverse(os.path.join(targetDir,entry))
        else:
            if os.path.isfile(os.path.join(targetDir,entry)) and isHandledType(entry) and match(entry) and not match(getBaseDirName(targetDir)):
                if method == "ctime":
                    newFileName = str(getCreationTime(os.path.join(targetDir,entry))) + entry.lstrip(getMediaPrefix(entry))
                elif method == "parent":
                    newFileName = getBaseDirName(currentDir) + entry.lstrip(getMediaPrefix(entry))
                
                if reallyDo and os.access(targetDir, os.W_OK) and os.access(os.path.join(targetDir,entry), os.W_OK):
                    try:
                        print("Moving" + " " + os.path.abspath(os.path.join(targetDir,entry)) + " to\t\t new file: " +  os.path.abspath(os.path.join(targetDir,newFileName)))
                        shutil.move(os.path.abspath(os.path.join(targetDir,entry)), os.path.abspath(os.path.join(targetDir,newFileName)))
                    except IOError:
                        print("IOERROR " + IOError.__cause__)
                    
            #else:
                #print("Skipping : " + os.path.abspath(os.path.join(getBaseDirName(currentDir),entry)))
    print("\n-- Directory change --")

if len(sys.argv) < 3:
    print("Synopsis: prenamer <target dir> <--really> <--method>. Without --really it's doing a dry run (simulation)\n")

if len(sys.argv) == 4:
    targetDir = sys.argv[1]
    if not os.path.exists(targetDir) or not os.path.isdir(targetDir) or not os.access(targetDir, os.W_OK) :
        print("I/O Error: " + targetDir)
        sys.exit()
    if sys.argv[2] == "--really":
        reallyDo = True
        traverse(targetDir)
    else:
        print("Synopsis: prenamer <target dir> <--really> <--method>. Without --really it's doing a dry run (simulation)\n")
        sys.exit()
        
print("\nDone!")
