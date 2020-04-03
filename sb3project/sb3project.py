# Project Object

# Imports
import json
from sb3project.sb3object import sb3target
from sb3project.sb3object import sb3block

class SB3Project:

    def __init__(self, rawProjString):
        projectJsonObj = json.loads(rawProjString)
        sectionHeaderList = list(projectJsonObj) # ['targets', 'monitors', 'extensions', 'meta']

        self.targetsList = []

        for indivSectionTitle in sectionHeaderList:
            # Create targets
            if (indivSectionTitle == "targets"):
                for targetNum in range(len(projectJsonObj[indivSectionTitle])):
                    tmpTargetObj = sb3target.SB3Target(projectJsonObj[indivSectionTitle][targetNum])
                    self.targetsList.append(tmpTargetObj)

            # Create monitors
            if (indivSectionTitle == "monitors"):
                pass

            # Create extensions
            if (indivSectionTitle == "extensions"):
                pass

            # Create meta
            if (indivSectionTitle == "meta"):
                pass

    def getTargetList(self):
        return self.targetsList
