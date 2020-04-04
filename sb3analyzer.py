# Handles analysis of project

from sb3project import sb3project
from sb3project.sb3object import sb3target
from sb3project.sb3object import sb3block
from sb3helper.sb3helper import *
import copy
#import ast


blockList_unreachable = []



def delimit():
    pr("\\")

class SB3Analyzer:
    def __init__(self, analysisMode, project):
        if analysisMode == 0: #do all analysis
            pass
        else:
            pass

        

        
        # print
        # self.traversal_functCall(project, self.travPrint)

        # get unreachable
        # self.createUnreachableList(project)

    def traversal_functCall(self, project, L_funct):
        targetList = project.getTargetList()

        for target in targetList:
            for block in target.get_blockList():
                if block.isTopLevel():
                    L_funct([0, [99,"\n"], target]) # print newline
                    L_funct([0, [99,"\n"], target]) # print newline
                    self.traverse(0, [0, block.get_idx()], target, L_funct)

    def printBlockList(self, project):
        targetList = project.getTargetList()

        for target in targetList:
            for block in target.get_blockList():
                pr(target.get_name())
                delimit()
                pr(block.get_idx())
                delimit()
                pr(block.isTopLevel())
                delimit()
                pr(block.get_opcode())
                delimit()
                pr(block.get_blockFieldDict())
                delimit()
                pr(block.get_blockInputDict())
                pr("\n")

    def traverse(self, indent, type_val, target, L_funct): # checks if is block or others
        if (type_val[0] == 0): #block
            if target.containsBlock_byId(type_val[1]): #block exists
                currBlock = target.getBlock_byId(type_val[1])
                
                L_funct([indent, [0, currBlock.get_idx()], target]) # do smth like print or mark reachable

                self.unpackBlock(indent, currBlock, target, L_funct)

                if (currBlock.get_next() != None):
                    L_funct([0, [99,"\n"], target]) # print newline
                    self.traverse(indent, [0, currBlock.get_next()], target, L_funct)
        else: # not a block
            L_funct([0, type_val, target]) # mimic string
    
    def unpackBlock(self, indent, currBlock, target, L_funct):

        L_funct([0, [99,""], target]) # start

        blockFieldDict = copy.deepcopy(currBlock.get_blockFieldDict())
        blockInputDict = copy.deepcopy(currBlock.get_blockInputDict())
        
        L_funct([0, [99,"["], target]) if len(blockFieldDict) > 0 else None # print [
        for indivFieldKey in blockFieldDict:
            L_funct([0, [10, blockFieldDict[indivFieldKey][0]], target]) # mimic string
        L_funct([0, [99,"]"], target]) if len(blockFieldDict) > 0 else None # print ]

        substackList = []

        if "SUBSTACK" in blockInputDict:
            substackList.append(blockInputDict["SUBSTACK"])
            del blockInputDict["SUBSTACK"]
        if "SUBSTACK2" in blockInputDict:
            substackList.append(blockInputDict["SUBSTACK2"])
            del blockInputDict["SUBSTACK2"]

        L_funct([0, [99,"("], target]) # print (
        inCtr = 0
        for indivBlockKey in blockInputDict:
            L_funct([0, [99,", "], target]) if inCtr != 0 else None # print ,
            self.traverse(0, blockInputDict[indivBlockKey], target, L_funct)
            # if blockInputDict[indivBlockKey][0] == 0:
            #     self.traverse(0, blockInputDict[indivBlockKey], target, L_funct)
            # else:
            #     L_funct([0, blockInputDict[indivBlockKey], target]) # mimic string
            inCtr += 1

        L_funct([0, [99,")"], target]) # print )
        if len(substackList) > 0:
            for type_valBlock in substackList: # assume substacks are blocks
                L_funct([0, [99,"{\n"], target])
                self.traverse(indent + 1, type_valBlock, target, L_funct)
                L_funct([0, [99,"\n"], target])
                L_funct([indent, [99,"}"], target])
        
        L_funct([0, [99,""], target]) # end

    def travPrint(self, inputArr):
        indent = inputArr[0]
        type_val = inputArr[1]
        target = inputArr[2]
        
        if type_val[0] == 0:
            block = target.getBlock_byId(type_val[1])
            prInd(indent, block.get_opcode())
        elif type_val[0] == 99:
            prInd(indent, type_val[1])
        else:

            if(3 < type_val[0] < 11):
                pr(str(type_val[1]))
            elif(type_val[0] == 11):
                if(sb3target.containsBroadcast_byId(type_val[1])):
                    broadcastValArr = sb3target.getBroadcastArr_byId(type_val[1])
                    pr(str(broadcastValArr[1]))
            elif(type_val[0] == 12):
                if(sb3target.containsVariable_byId(type_val[1])):
                    varValArr = sb3target.getVariableArr_byId(type_val[1])
                    pr(str(varValArr[0][0]))
            elif(type_val[0] == 13):
                if(sb3target.containsList_byId(type_val[1])):
                    listValArr = sb3target.getListArr_byId(type_val[1])
                    pr(str(listValArr[0][0])) ## CHECK
            else:
                pr(str(type_val))




    def createUnreachableList(self, project):
        targetList = project.getTargetList()
        for target in targetList:
            for block in target.get_blockList():
                blockList_unreachable.append(block.get_idx()) # assume not reachable, remove if reachable
        self.traversal_functCall(project, self.removeReachable)
        
    def removeReachable(self, inputArr):
        type_val = inputArr[1]
        target = inputArr[2]
        
        if type_val[0] == 0:
            block = target.getBlock_byId(type_val[1])
            blockList_unreachable.remove(block.get_idx())