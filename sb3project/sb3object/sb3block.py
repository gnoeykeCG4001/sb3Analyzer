# Block Object

# Imports

# Class declaration

class SB3Block:

    # Constructor
        
    def __init__(self, containerTarget, blockIdx, blockJsonObj):
        
        self.containerTarget = containerTarget
        self.idx = blockIdx
        self.opcode = blockJsonObj['opcode']
        self.next = blockJsonObj['next']
        self.parent = blockJsonObj['parent']
        self.topLevel = blockJsonObj['topLevel']
        self.blockInputDict = {}
        self.blockFieldDict = {}

        self.reachable = False
        
        # check if is target attribute getter (size/direction etc)

        # extract inputs and add to list

        inputLabel = list(blockJsonObj['inputs'])
        for indivInputLabel in inputLabel:
            # Label : [Type, Value]
            # blockJsonObj['inputs'][indivInputLabel][0] is discarded
            self.blockInputDict[indivInputLabel] = decodeInput(blockJsonObj['inputs'][indivInputLabel][1])

        # extract fields and add to list
        
        fieldLabel = list(blockJsonObj['fields'])
        for indivFieldLabel in fieldLabel:
            # Label : [NameId, Reference]
            self.blockFieldDict[indivFieldLabel] = decodeField(blockJsonObj['fields'][indivFieldLabel])

    # Class Methods
    def get_self(self):
        return self
    
    def get_idx(self):
        return self.idx

    def get_opcode(self):
        return self.opcode

    def get_next(self):
        return self.next

    def get_parent(self):
        return self.parent
    
    def isTopLevel(self):
        return self.topLevel

    def get_blockInputDict(self):
        return self.blockInputDict

    def get_blockFieldDict(self):
        return self.blockFieldDict

    def markReachable(self):
        self.reachable = True
    
    def isReachable(self):
        return self.reachable

primitiveType = {
    # 0 : References to Objects etc
    1 : "",
    2 : "",
    3 : "",
    4 : "Number",
    5 : "PositiveNumber",
    6 : "PositiveInteger",
    7 : "Integer",
    8 : "Angle",
    9 : "Color",
    10 : "String",
    11 : "Broadcast",
    12 : "Variable",
    13 : "List",
}

def decodeInput(inputArr):

    isString =  isinstance(inputArr, str)

    if isString:
        # Type 0, Value | 0 might represent reference Costumes etc
        return [0, inputArr]
    else:
        if inputArr[0] >= 11:
            # Type, Value
            return [inputArr[0], inputArr[2]]
        else:
            # Type, Value
            return [inputArr[0], inputArr[1]]

def decodeField(fieldArr):
    # NameId, Reference
    return [fieldArr[0], fieldArr[1]]