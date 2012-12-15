''' http://python.org/dev/peps/pep-0263/
# coding: utf-8
Created on Jun 1, 2012
Copyright adrian@javaguru.org
'''
import os, sys, locale, re, shutil

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

def getBaseDirName(path):
    return os.path.basename(os.path.abspath(path))

def isJpg(path):
    (name,ext) = os.path.splitext(path)
    if ext.upper() == ".JPG":
        return True
    else:
        return False
    
''' Find JPG files not already renamed to yyyy-mm-dd pattern '''
def match(path):
    # pattern 0000-00-00--sometext
    pattern = re.compile('\d{4}-\d{2}-\d{2}--\w*')
    if re.match(pattern, path):
        print("Path date pattern match : " + path)
        return False
    else:
        return True

def traverse (targetDir):
    currentDir = targetDir
    dirs = os.listdir(targetDir)
    for entry in dirs:
        if os.path.isdir(os.path.join(currentDir,entry)):
            print("Traversing " + os.path.join(targetDir,entry))
            traverse(os.path.join(targetDir,entry))
        else:
            if os.path.isfile(os.path.join(targetDir,entry)) and isJpg(entry) and match(entry) and not match(getBaseDirName(targetDir)):
                newFileName = getBaseDirName(currentDir) + entry.lstrip("DSC")

                if reallyDo and os.access(targetDir, os.W_OK) and os.access(os.path.join(targetDir,entry), os.W_OK):
                    try:
                        print("Moving" + " " + os.path.abspath(os.path.join(targetDir,entry)) + " to\t\t new file: " +  os.path.abspath(os.path.join(targetDir,newFileName)))
                        shutil.move(os.path.abspath(os.path.join(targetDir,entry)), os.path.abspath(os.path.join(targetDir,newFileName)))
                    except IOError:
                        print("IOERROR " + IOError.__cause__)
                    
            else:
                print("Skipping : " + os.path.abspath(os.path.join(getBaseDirName(currentDir),entry)))
    print("\n-- Directory change --")

if len(sys.argv) < 3:
    print("Synopsis: prenamer <target dir> <--really> . Without --really it's doing a dry run (simulation)\n")

if len(sys.argv) == 3:
    targetDir = sys.argv[1]
    if not os.path.exists(targetDir) or not os.path.isdir(targetDir) or not os.access(targetDir, os.W_OK) :
        print("I/O Error: " + targetDir)
        sys.exit()
    if sys.argv[2] == "--really":
        reallyDo = True
        traverse(targetDir)
    else:
        print("Synopsis: prenamer <target dir> <--really> . Without --really it's doing a dry run (simulation)\n")
        sys.exit()
        
print("\nDone!")


