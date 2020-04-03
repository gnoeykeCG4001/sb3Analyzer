
def pr(arg1, *argv):
    print (arg1, end='') 
    for arg in argv: 
        print(arg, end='')

def prInd(indent, arg1, *argv):
    tabSp = "\t" * indent
    print (tabSp, end='')
    print (arg1, end='')
    for arg in argv: 
        print(arg, end='')

def printInd(indent, arg1, *argv):
    tabSp = "\t" * indent
    print (tabSp, end='')
    print (arg1, end='')
    for arg in argv: 
        print(arg, end='')
    print()