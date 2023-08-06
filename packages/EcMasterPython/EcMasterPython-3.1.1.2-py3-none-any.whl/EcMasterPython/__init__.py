import os
import sys
import platform
os.environ["PATH"] += os.pathsep + "C:/Program Files/acontis_technologies/EC-Master-Windows-x86_32Bit/Bin/Windows/x86"
os.environ["PATH"] += os.pathsep + "C:/Program Files/acontis_technologies/EC-Master-Windows-x86_64Bit/Bin/Windows/x64"
installDir = os.path.dirname(__file__) + os.path.sep
sys.path.append(installDir + "Sources/EcWrapperPython")
sys.path.append(installDir + "Examples/EcMasterDemoPython")
from EcMasterPython.Examples.EcMasterDemoPython.EcDemoApp import *
from EcMasterPython.Sources.EcWrapperPython.EcWrapperPython import *
from EcMasterPython.Sources.EcWrapperPython.EcWrapperPythonTypes import *
from EcMasterPython.Sources.EcWrapperPython.EcWrapper import *
from EcMasterPython.Sources.EcWrapperPython.EcWrapperTypes import *

def IsMasterPackageInstalled():
    installDir = CEcWrapperPython.GetInstallDir()
    libPath = installDir + CEcWrapper.GetEcWrapperName()
    if os.path.isfile(libPath):
        return True
    return False

if IsMasterPackageInstalled() == False:
    print("Error: EC-Master package not found.\n\nPlease install EC-Master package and add path of binaries\nto PATH variable (if necessary) or contact support to\nrequest an EVAL version: 'https://www.acontis.com/.")
    os._exit(-1)     

