#/*-----------------------------------------------------------------------------
# * EcDemoAppInteractive.py
# * Copyright                acontis technologies GmbH, Ravensburg, Germany
# * Description              Interactive EC-Master demo application for Python
# *---------------------------------------------------------------------------*/
# pylint: disable=unused-wildcard-import, wildcard-import
import sys
from EcDemoApp import *

demo = EcMasterDemoPython()
demo.pAppParms.tRunMode = RunMode.Master
demo.pAppParms.dwBusCycleTimeUsec = 4000
demo.pAppParms.szENIFilename = "ENI.xml"
demo.pAppParms.szLinkLayer = "winpcap 127.0.0.0 1"
demo.pAppParms.nVerbose = 3
demo.parseCommandLine(sys.argv[1:])
demo.startDemo()
print("EcMasterDemoPython is running.")
print("Type demo.help() for interactive help.")
#demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.set(1)
#demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.get()
#demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.dmp()
#demo.stopDemo()

'''
# IDLE: Paste this code
exec("""
import os
import sys
INSTALLDIR = "C:/Program Files/acontis_technologies/EC-Master-Windows-x86_64Bit/"
os.environ["PATH"] += os.pathsep + INSTALLDIR + "Bin/Windows/x64"
sys.path.append(INSTALLDIR + "Sources/EcWrapperPython")
sys.path.append(INSTALLDIR + "Examples/EcMasterDemoPython")
from EcDemoApp import *
demo = EcMasterDemoPython()
demo.pAppParms.tRunMode = RunMode.Master
demo.pAppParms.dwBusCycleTimeUsec = 4000
demo.pAppParms.szENIFilename = "ENI.xml"
demo.pAppParms.szLinkLayer = "winpcap 127.0.0.0 1"
demo.pAppParms.nVerbose = 3
demo.startDemo()
print("EcMasterDemoPython is running.")
print("Type demo.help() for interactive help.")
""")
'''