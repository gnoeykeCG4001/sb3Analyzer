# Target Object

## Imports
from sb3project.sb3object import sb3block

## Globals

variableDict = {} # stored as dict idx : [name, targetName, value] | variable handled as global (targetname = None) if cant find in local
listDict = {} # stored as dict idx : [name, targetName, [listvalues] ] | variable handled as global (targetname = None) if cant find in local
broadcastDict = {} # stored as dict idx : [name, targetName]  | broadcast handled as global (targetname = None) if cant find in local

def getVariableDict(): return variableDict
def getListDict(): return listDict
def getBroadcastDict(): return broadcastDict

## Helper functions

## Class declaration

class SB3Target:       
    def __init__(self, targetJsonObj):
        self.isStage = targetJsonObj['isStage']
        self.type = "stage" if targetJsonObj['isStage'] else "sprite"
        self.name = targetJsonObj['name']
        
        self.targetBlockList = []

        # extract block and add to list
        for blockIdx in targetJsonObj['blocks']:
            self.targetBlockList.append(sb3block.SB3Block(self.name, blockIdx, targetJsonObj['blocks'][blockIdx]))
        
        # extract variable and add to list
        for idx in targetJsonObj['variables']:
            variableDict[idx] = [targetJsonObj['variables'][idx], None, None] # all as global
        
        # extract list and add to list
        for idx in targetJsonObj['lists']:
            listDict[idx] = [targetJsonObj['lists'][idx], None, []] # all as global

        # extract broadcast and add to list
        for idx in targetJsonObj['broadcasts']:
            broadcastDict[idx] = [targetJsonObj['broadcasts'][idx], None] # all as global

    # Class Methods
    def get_self(self):
        return self

    def get_isStage(self):
        return self.isStage

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_blockList(self):
        return self.targetBlockList
    
    def getBlock_byId(self, idx):
        for tmpBlockObj in self.get_blockList():
            if tmpBlockObj.get_idx() == idx:
                return tmpBlockObj
        return None

    def containsBlock_byId(self, idx):
        for tmpBlockObj in self.get_blockList():
            if tmpBlockObj.get_idx() == idx:
                return True
        return False

# module methods

def getVariableArr_byId(idx):
        for key in getVariableDict():
            if key == idx:
                return getVariableDict()[key]
        return None

def containsVariable_byId(idx):
    for key in getVariableDict():
        if key == idx:
            return True
    return False

def getBroadcastArr_byId(idx):
        for key in getBroadcastDict():
            if key == idx:
                return getBroadcastDict()[key]
        return None

def containsBroadcast_byId(idx):
    for key in getBroadcastDict():
        if key == idx:
            return True
    return False

def getListArr_byId(idx):
        for key in getListDict():
            if key == idx:
                return getListDict()[key]
        return None

def containsList_byId(idx):
    for key in getListDict():
        if key == idx:
            return True
    return False
