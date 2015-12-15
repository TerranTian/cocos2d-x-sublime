import sublime
import os
import hashlib
import sys
import fnmatch;
import re;
import codecs

def getFileList(root, patterns = '*',encludePatterns=None, single_level = False, yield_folders=False):
    pj = os.path.join
    result = [];
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        result.extend([pj(path,name) for name in sorted(files) for pattern in patterns if(fnmatch.fnmatch(pj(path,name), pattern))])
        
        if single_level:
            break
        
    if(encludePatterns):
        encludePatterns = encludePatterns.split(';')
        enclude = [n for n in result for p in encludePatterns if fnmatch.fnmatch(n, p)]
        return [f for f in result if f not in enclude]
    
    return result;

# read content from a file
def readFile(path):
    # f = open(path, "r")
    f = codecs.open(path,"r",'utf-8')
    content = f.read()#.encode('utf-8').decode("gbk")
    f.close()
    return content

# write content to a file
def writeFile(path, content):
    f = open(path, "w+")
    f.write(content)
    f.close()

# check file extention
def checkFileExt(file,ext):
    ext1 = os.path.splitext(file)[1][1:]
    if ext1 == ext:
        return True
    else:
        return False

def md5(str):
    return hashlib.md5(str.encode(sys.getfilesystemencoding())).hexdigest()

def isST3():
    return sublime.version()[0] == '3'

def loadSettings(name):
    return sublime.load_settings(name+".sublime-settings")
