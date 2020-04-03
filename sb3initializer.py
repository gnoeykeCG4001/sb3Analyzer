# Create Project object

from sb3project import sb3project
from sb3project.sb3object import sb3target
from sb3project.sb3object import sb3block

def initializeProject(projectJsonString):
    Project = sb3project.SB3Project(projectJsonString)
    return Project