# Handles input of .sb3 file and input of analysis mode
# Stores Project and Analyzer Object

import zipfile
import sb3analyzer
import sb3initializer



# taking file from current working directory
import os
cwd = os.path.abspath(os.getcwd())
sb3filepath = cwd + "\\CatJumpJump.sb3"
#sb3filepath = cwd + "\\tmpUnreachableCode.sb3"
#sb3filepath = cwd + "\\tmpUnreachableCode2.sb3"


# Configuration
sb3filepath = sb3filepath
analysisMode = 0


# File Handling
sb3file = zipfile.ZipFile(sb3filepath, 'r')
projectJsonFile = sb3file.read('project.json')
projectJsonString = "".join(projectJsonFile.decode("ascii","ignore")) # protection from using unknown unicode characters


Project = sb3initializer.initializeProject(projectJsonString)

Analyzer = sb3analyzer.SB3Analyzer(analysisMode, Project)

