# Handles analysis of project

from sb3project import sb3project
from sb3project.sb3object import sb3target
from sb3project.sb3object import sb3block
from sb3helper.sb3helper import *
import copy
#import ast


blockList_unreachable = []
headOpcodeList = ['event_whenflagclicked','event_whenkeypressed','event_whenthisspriteclicked','event_whenbackdropswitchesto','event_whengreaterthan','event_whenbroadcastreceived']



def delimit():
    pr("\\")

class SB3Analyzer:
    def __init__(self, analysisMode, project):


        # future analysis configuration to mux assessments to execute
        # if analysisMode == 0: #do all analysis
        #     pass
        # else:
        #     pass

        
        ### A - Example  on Printing Block List Detail Summary
        ## print block list
        #self.printBlockList(project)

        ### B - Example on converting reachable code into indented textual representation 
        ## print indented
        self.traversal_functCall(project, self.travPrint)


        ### C - Example on getting list of unreachable blocks
        ## create list of index of unreachable block and print it out
        # self.createUnreachableList(project)
        # print(blockList_unreachable)
        # if blockList_unreachable:
        #     print("unreachable blocks:")
        #     targetList = project.getTargetList()
        #     for target in targetList:
        #         for block in target.get_blockList():
        #             if block.get_idx() in blockList_unreachable:
        #                 print(str(block.get_idx()) + " : " + str(block.get_opcode()))



        ### D - Example  on getting a list of reachable blocks matching opcode list ["control_if", "control_if_else"]
        ## get list of reachable blocks matching opcode list
        ## Reference from Dr Scratch
        ## based on matching code can give a score
        # matchBlkList = self.getBlockList_matchOpcodeList(project, ["control_if", "control_if_else"])
        # if matchBlkList:
        #     print("matched blocks:")
        #     targetList = project.getTargetList()
        #     for target in targetList:
        #         for block in target.get_blockList():
        #             if block.get_idx() in matchBlkList:
        #                 print(str(block.get_idx()) + " : " + str(block.get_opcode()))




    def traversal_functCall(self, project, L_funct):
        targetList = project.getTargetList()

        for target in targetList:
            for block in target.get_blockList():
                if block.isTopLevel() and block.get_opcode() in headOpcodeList:
                    L_funct([0, [99,"\n"], target]) # print newline
                    L_funct([0, [99,"\n"], target]) # print newline
                    self.traverse(0, [0, block.get_idx()], target, L_funct)

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
                    pr(str(broadcastValArr[0]))
            elif(type_val[0] == 12):
                if(sb3target.containsVariable_byId(type_val[1])):
                    varValArr = sb3target.getVariableArr_byId(type_val[1])
                    pr(str(varValArr[0][0]))
            elif(type_val[0] == 13):
                if(sb3target.containsList_byId(type_val[1])):
                    listValArr = sb3target.getListArr_byId(type_val[1])
                    pr(str(listValArr[0][0]))
            else:
                pr(str(type_val))






    def createUnreachableList(self, project):
        targetList = project.getTargetList()
        for target in targetList:
            for block in target.get_blockList():
                blockList_unreachable.append(block.get_idx()) # assume not reachable, remove if reachable
        #print(blockList_unreachable)
        self.traversal_functCall(project, self.removeReachable)
        
    def removeReachable(self, inputArr):
        type_val = inputArr[1]
        target = inputArr[2]
        
        if type_val[0] == 0:
            #print(type_val)
            block = target.getBlock_byId(type_val[1])
            blockList_unreachable.remove(block.get_idx())








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

    
    
    def getBlockList_matchOpcodeList(self, project, opcodeList):
        targetList = project.getTargetList()

        self.createUnreachableList(project)

        blockIdx_ofOpcodeMatch = []

        for target in targetList:
            for block in target.get_blockList():
                if block.get_opcode() in opcodeList:
                    if block.get_idx() not in blockList_unreachable:
                        blockIdx_ofOpcodeMatch.append(block.get_idx())
        return blockIdx_ofOpcodeMatch