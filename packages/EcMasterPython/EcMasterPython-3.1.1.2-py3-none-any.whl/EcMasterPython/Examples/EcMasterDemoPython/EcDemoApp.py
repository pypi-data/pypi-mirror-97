#/*-----------------------------------------------------------------------------
# * EcDemoApp.py
# * Copyright                acontis technologies GmbH, Ravensburg, Germany
# * Description              EC-Master demo application for Python
# *---------------------------------------------------------------------------*/
# pylint: disable=unused-wildcard-import, wildcard-import, unused-argument
from EcWrapperPython import *
from EcWrapperPythonTypes import *
from enum import Enum
import sys, getopt
from threading import Thread
import threading
import time

EC_DEMO_APP_NAME = "EcMasterDemoPython"

class RunMode(Enum):
    Unknown = 0
    Master = 1
    RasClient = 2
    MbxGateway = 3
    Simulator = 4

class EcLogging:
    def __init__(self):
        self.severity = DN_EC_LOG_LEVEL.INFO
        self.prefix = ""
        return

    def initLogger(self, dwSeverity, szLogFileprefix):
        self.severity = dwSeverity
        self.prefix = szLogFileprefix
        return True

    def logMsg(self, severity, msg, *args):
        if severity.value > self.severity.value:
            return
        if (len(args) > 0):
            msg = EcLogging.replaceFormatStr(msg)
            msg = msg.format(*args)
        print(msg.rstrip())
        return

    @staticmethod
    def replaceFormatStr(msg):
        msg = msg.replace("%d", "{}")
        msg = msg.replace("%lx", "{}")
        msg = msg.replace("%x", "{:02X}")
        msg = msg.replace("%02X", "{:02X}")
        msg = msg.replace("%04x", "{:04X}")
        msg = msg.replace("%04X", "{:04X}")
        msg = msg.replace("%4d", "{}")
        msg = msg.replace("%08X", "{:08X}")
        msg = msg.replace("%s", "{}")
        return msg

class EcProcessImageDynGroup(object):
    pass

class EcProcessImageGroup:
    def __init__(self):
        self._children = {}

    def hasChild(self, name):
        if name in self._children:
            return True
        return False
    
    def addChild(self, name, value):
        self._children[name] = value
        return

    def getChild(self, name):
        return self._children[name]

    def createDynObject(self):
        obj = EcProcessImageDynGroup()
        for name in self._children:
            value = self._children[name]
            # create dynamic object (escape special chars)
            name = name.replace("[", "_")
            name = name.replace("]", "_")
            name = name.replace(" ", "_")
            if isinstance(value, EcProcessImageGroup):
                value = value.createDynObject()
            setattr(obj, name, value) 
        return obj

class EcProcessImageVariable:
    def __init__(self, demo2, variable):
        self._demo = demo2
        self._variable = variable

    def set(self, value):
        variable = self._variable
        out_valueAsBytes = CEcWrapperPythonOutParam()
        dwRes = CEcWrapperPython.ConvValueToBytes(DN_EC_T_DEFTYPE(variable.wDataType), value, out_valueAsBytes)
        if dwRes != ECError.EC_NOERROR:
            print("ConvValueToBytes failed! Error Text: " + self._demo.oEcWrapper.GetErrorText(dwRes))    
            return None
        valueAsBytes = out_valueAsBytes.value
        dwRes = self._demo.oEcWrapper.SetProcessDataBits(not variable.bIsInputData, variable.nBitOffs, valueAsBytes, variable.nBitSize, 2000)    
        if dwRes != ECError.EC_NOERROR:
            print("Write process data failed! Error Text: " + self._demo.oEcWrapper.GetErrorText(dwRes))    
            return None

        print("Variable written.")    
        return
    
    def get(self):
        variable = self._variable
        pbyDataDst = [0] * ((variable.nBitSize + 8) // 8)
        dwRes = self._demo.oEcWrapper.GetProcessDataBits(not variable.bIsInputData, variable.nBitOffs, pbyDataDst, variable.nBitSize, 2000)    
        if dwRes != ECError.EC_NOERROR:
            print("Read process data failed! Error Text: " + self._demo.oEcWrapper.GetErrorText(dwRes))    
            return None

        out_dataRead = CEcWrapperPythonOutParam()
        dwRes = CEcWrapperPython.ReadValueFromBytes(pbyDataDst, 0, variable.nBitSize, DN_EC_T_DEFTYPE(variable.wDataType), out_dataRead)
        if dwRes != ECError.EC_NOERROR:
            print("ReadValueFromBytes failed! Error Text: " + self._demo.oEcWrapper.GetErrorText(dwRes))    
            return None

        dataRead = out_dataRead.value
        return dataRead

    def dmp(self):
        variable = self._variable
        print("szName       = " + str(variable.szName))
        print("wDataType    = " + str(variable.wDataType))
        print("wFixedAddr   = " + str(variable.wFixedAddr))
        print("nBitSize     = " + str(variable.nBitSize))
        print("nBitOffs     = " + str(variable.nBitOffs))
        print("bIsInputData = " + str(variable.bIsInputData))
        return

class EcProcessImageSlave:
    def __init__(self):
        self.address = 0
        self.name = ""
        self.variables = []

class EcProcessImage:
    def __init__(self, demo2):
        self.demo = demo2
        self.slaves = []
        self.variables = []
        return

    def reload(self):
        self.slaves.clear()    

        # /* Read amount of slaves from Master */
        oStatusArr = CEcWrapperPythonOutParam()
        self.demo.oEcWrapper.GetScanBusStatus(oStatusArr)
        oStatus = oStatusArr.value
        if oStatus.dwResultCode == ECError.EC_BUSY: #ECScanBus.BUSY:
            return

        if oStatus.dwSlaveCount == 0:
            return 

        ## /* Create slave nodes, if slaves are connected */
        for wIdx in range(0, oStatus.dwSlaveCount):
            oSlaveInfoArr = CEcWrapperPythonOutParam()

            # /* Request information about slave object */
            eRetVal = self.demo.oEcWrapper.GetSlaveInfo(False, 0 - wIdx, oSlaveInfoArr)
            oSlaveInfo = oSlaveInfoArr.value
            if ECError.EC_NOERROR != eRetVal:
                self.demo.logMasterError("Reading slave info failed: ", eRetVal)    
                continue    

            slaveData = EcProcessImageSlave()
            slaveData.address = oSlaveInfo.wPhysAddress
            slaveData.name = oSlaveInfo.abyDeviceName
            self.slaves.append(slaveData)

        for slaveData in self.slaves:
            inputVariables = self.ReadProcessVariablesFromSlave(slaveData.address, True)
            if inputVariables != None:
                slaveData.variables.extend(inputVariables)
            outputVariables = self.ReadProcessVariablesFromSlave(slaveData.address, False)
            if outputVariables != None:
                slaveData.variables.extend(outputVariables)

        self.variables = self.ReadProcessVariables()
        return

    #/// <summary>Reads all process variables of a slave</summary>
    def ReadProcessVariablesFromSlave(self, wSlaveAddress, input_):
        numOfVariablesArr = CEcWrapperPythonOutParam()
        eRes = ECError.EC_ERROR
        if input_:
            eRes = self.demo.oEcWrapper.GetSlaveInpVarInfoNumOf(True, wSlaveAddress, numOfVariablesArr)
        else:
            eRes = self.demo.oEcWrapper.GetSlaveOutpVarInfoNumOf(True, wSlaveAddress, numOfVariablesArr)
        numOfVariables = numOfVariablesArr.value
        if eRes != ECError.EC_NOERROR:
            self.demo.logMasterError("Reading number of process variables failed: ", eRes)    
            return None    

        if numOfVariables == 0:
            return None    

        numOfReadVariablesArr = CEcWrapperPythonOutParam()
        variablesArr = CEcWrapperPythonOutParam()
        if input_:
            eRes = self.demo.oEcWrapper.GetSlaveInpVarInfo(True, wSlaveAddress, numOfVariables, variablesArr, numOfReadVariablesArr)
        else:
            eRes = self.demo.oEcWrapper.GetSlaveOutpVarInfo(True, wSlaveAddress, numOfVariables, variablesArr, numOfReadVariablesArr)
        variables = variablesArr.value
        if eRes != ECError.EC_NOERROR:
            self.demo.logMasterError("Reading process variables failed: ", eRes)    
            return None    

        return variables
  
    def ReadProcessVariables(self):
        variables = []
        for slave in self.slaves:
            variables.extend(slave.variables)
        tree = EcProcessImageGroup()
        for variable in variables:
            parts = variable.szName.split(".")    
            cur = tree
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    cur.addChild(part, EcProcessImageVariable(self.demo, variable))
                elif not cur.hasChild(part):
                    cur.addChild(part, EcProcessImageGroup())
                cur = cur.getChild(part)
        return tree.createDynObject()

class MyAppDesc:
    def __init__(self):
        self.wFlashSlaveAddr = 0    
        self.dwFlashPdBitSize = 0        #/* Size of process data memory */
        self.dwFlashPdBitOffs = 0        #/* Process data offset of data */
        self.dwFlashTimer = 0    
        self.dwFlashInterval = 0    
        self.byFlashVal = 0              #/* flash pattern */
        self.pbyFlashBuf = None             #/* flash buffer */
        self.dwFlashBufSize = 0          #/* flash buffer size */

class EcDemoAppParams:
    ATEMRAS_DEFAULT_PORT = 6000    
    MBXGATEWAY_DEFAULT_PORT = 34980    

    def __init__(self):
        
        #/* configuration */
        self.tRunMode = RunMode.Unknown         #/* Run mode */
        self.szENIFilename = ""                 #/* ENI filename string */
        #/* link layer */
        self.szLinkLayer = ""                   #/* Link layer settings */
        #/* timing */
        self.dwBusCycleTimeUsec = 4000          #/* bus cycle time in usec */
        self.dwDemoDuration = 0                 #/* demo duration in msec */
        #/* logging */
        self.nVerbose = 0                       #/* verbosity level */
        self.dwAppLogLevel = DN_EC_LOG_LEVEL.UNDEFINED #/* demo application log level (derived from verbosity level) */
        self.dwMasterLogLevel = DN_EC_LOG_LEVEL.UNDEFINED #/* master stack log level (derived from verbosity level) */
        self.szLogFileprefix = ""               #/* log file prefix string */
        #/* RAS */
        self.wRasServerPort = 0                 #/* remote access server port */
        self.abyRasServerIpAddress = "127.0.0.1" #/* remote access server IP address */
        #/* additional parameters for the different demos */
        self.wFlashSlaveAddr = 0                #/* flashing output slave station address */

class EcDemoApp:
    c_MASTER_CFG_ECAT_MAX_BUS_SLAVES = 256    
    c_MASTER_CFG_MAX_ACYC_FRAMES_QUEUED = 32        #/* max number of acyc frames queued, 127 = the absolute maximum number */
    c_MASTER_CFG_MAX_ACYC_BYTES_PER_CYC = 4096      #/* max number of bytes sent during eUsrJob_SendAcycFrames within one cycle */
    c_MASTER_CFG_MAX_ACYC_CMD_RETRIES = 3    
    ETHERCAT_STATE_CHANGE_TIMEOUT = 15000           #/* master state change timeout in ms */
    ETHERCAT_SCANBUS_TIMEOUT = 10000                #/* scanbus timeout in ms, see also EC_SB_DEFAULTTIMEOUT */

    def __init__(self):
        self.pAppParms = EcDemoAppParams()
        self.pMyAppDesc = MyAppDesc()
        self.logger = EcLogging()
        self.oEcWrapper = CEcWrapperPythonEx()
        self.onDbgMsgNotificationId = -1
        self.onMasterNotificationId = -1
        self.onRasNotificationId = -1
        self.processImage = EcProcessImage(self)
        self.m_oJobTask = None
        self.m_bJobTaskRunning = False
        self.m_bJobTaskShutDown = False
        self.m_nCycleTime = 4

    def logMasterError(self, message, eRes):
        self.logMsg(DN_EC_LOG_LEVEL.ERROR, "{}{} (0x{:08X})".format(message, self.oEcWrapper.GetErrorText(eRes), eRes))    

    def logInfo(self, message, *args):
        self.logMsg(DN_EC_LOG_LEVEL.INFO, message, *args)    

    def logMsg(self, severity, message, *args):
        self.logger.logMsg(severity, message, *args)    

    def parseCommandLine(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hf:t:b:v:", ["mode=","log=","sp=","link=","flash="])
        except getopt.GetoptError as error:
            self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "Parse command line failed:\n%s\n\n", str(error))    
            self.showSyntaxCommon()
            return False

        for opt, arg in opts:
            if opt == '-h':
                self.showSyntaxCommon()
                return False
            elif opt in {"-f", "--file"}:
                self.pAppParms.szENIFilename = arg
            elif opt == "-t":
                self.pAppParms.dwDemoDuration = int(arg)
            elif opt == "-b":
                self.pAppParms.dwBusCycleTimeUsec = int(arg)
            elif opt == "-v":
                self.pAppParms.nVerbose = int(arg)
            elif opt == "--log":
                self.pAppParms.szLogFileprefix = arg
            elif opt == "--sp":
                self.pAppParms.wRasServerPort = int(arg)
            elif opt == "--mode":
                self.pAppParms.tRunMode = RunMode(int(arg))
            elif opt == "--link":
                self.pAppParms.szLinkLayer = arg
            elif opt == "--flash":
                self.pAppParms.wFlashSlaveAddr = int(arg)

        return True

    def setAppAndMasterLogLevel(self):
        if self.pAppParms.nVerbose == 0:
            self.pAppParms.dwAppLogLevel   = DN_EC_LOG_LEVEL.SILENT    
            self.pAppParms.dwMasterLogLevel = DN_EC_LOG_LEVEL.SILENT    
        elif self.pAppParms.nVerbose == 1:
            self.pAppParms.dwAppLogLevel   = DN_EC_LOG_LEVEL.INFO    
            self.pAppParms.dwMasterLogLevel = DN_EC_LOG_LEVEL.ERROR    
        elif self.pAppParms.nVerbose == 2:
            self.pAppParms.dwAppLogLevel   = DN_EC_LOG_LEVEL.INFO    
            self.pAppParms.dwMasterLogLevel = DN_EC_LOG_LEVEL.WARNING    
        elif self.pAppParms.nVerbose == 3:
            self.pAppParms.dwAppLogLevel   = DN_EC_LOG_LEVEL.VERBOSE    
            self.pAppParms.dwMasterLogLevel = DN_EC_LOG_LEVEL.WARNING    
        elif self.pAppParms.nVerbose == 4:
            self.pAppParms.dwAppLogLevel   = DN_EC_LOG_LEVEL.VERBOSE    
            self.pAppParms.dwMasterLogLevel = DN_EC_LOG_LEVEL.INFO    
        elif self.pAppParms.nVerbose == 5:
            self.pAppParms.dwAppLogLevel   = DN_EC_LOG_LEVEL.VERBOSE    
            self.pAppParms.dwMasterLogLevel = DN_EC_LOG_LEVEL.VERBOSE    
        else:
            self.pAppParms.dwAppLogLevel   = DN_EC_LOG_LEVEL.VERBOSE_CYC    
            self.pAppParms.dwMasterLogLevel = DN_EC_LOG_LEVEL.VERBOSE_CYC    

    def showSyntaxCommon(self):
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "Usage:\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -mode             Run mode\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     mode            1 = master, 2 = ras client, 3 = mailbox gateway, 4 = simulator\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -f                Use given ENI file\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     FileName        file name .xml\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -t                Demo duration\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     time            Time in msec, 0 = forever (default = 120000)\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -b                Bus cycle time\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     cycle time      Cycle time in usec\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -link             Link layer\n")
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     name [settings] name and link layer specific settings\n")
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "                     e.g. winpcap 127.0.0.0 1\n")
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -v                Set verbosity level\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     lvl             Level: 0=off, 1...n=more messages, 3(default) generate dcmlog file\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -log              Use given file name prefix for log files\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     prefix          prefix\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "   -sp               Start RAS server\n")    
        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "     port            port (default = %d)\n", EcDemoAppParams.ATEMRAS_DEFAULT_PORT)    
        return True

    @staticmethod
    def str_to_ip_address(string):
        return [int(octet) for octet in string.split(".")[0:4]]
    
    def createLinkParms(self):
        try:
            arLinkLayer = self.pAppParms.szLinkLayer.split(" ")
            if not arLinkLayer or len(arLinkLayer) < 1:
                return None

            name = arLinkLayer[0]
            oLinkParms = DN_EC_T_LINK_PARMS()

            if name == "winpcap":
                eLinkMode = int(arLinkLayer[2])
                oLinkParms.eLinkType = ELinkType.WINPCAP
                oLinkParms.eLinkMode = ELinkMode.INTERRUPT if eLinkMode == 0 else ELinkMode.POLLING
                oLinkParms.dwInstance = 0
                oLinkParms.oWinPcap = DN_EC_T_LINK_PARMS_WINPCAP()
                oLinkParms.oWinPcap.abyIpAddress = EcDemoApp.str_to_ip_address(arLinkLayer[1])
                return oLinkParms

            if name == "sockraw":
                szAdapterName = arLinkLayer[1]
                eLinkMode = int(arLinkLayer[2])
                oLinkParms.eLinkType = ELinkType.SOCKRAW
                oLinkParms.eLinkMode = ELinkMode.INTERRUPT if eLinkMode == 0 else ELinkMode.POLLING
                oLinkParms.dwInstance = 0
                oLinkParms.oSockRaw = DN_EC_T_LINK_PARMS_SOCKRAW()
                oLinkParms.oSockRaw.szAdapterName = szAdapterName
                return oLinkParms

            if name == "i8254x":
                dwInstance = int(arLinkLayer[1])
                eLinkMode = int(arLinkLayer[2])
                oLinkParms.eLinkType = ELinkType.I8254X
                oLinkParms.eLinkMode = ELinkMode.INTERRUPT if eLinkMode == 0 else ELinkMode.POLLING
                oLinkParms.dwInstance = dwInstance
                oLinkParms.oI8254x = DN_EC_T_LINK_PARMS_I8254X()
                return oLinkParms

            if name in {"i8255x", "rtl8139", "rtl8169", "ccat"}:
                dwInstance = int(arLinkLayer[1])
                eLinkMode = int(arLinkLayer[2])
                if name == "i8255x":
                    oLinkParms.eLinkType = ELinkType.I8255X
                elif name == "rtl8139":
                    oLinkParms.eLinkType = ELinkType.RTL8139
                elif name == "rtl8169":
                    oLinkParms.eLinkType = ELinkType.RTL8169
                elif name == "ccat":
                    oLinkParms.eLinkType = ELinkType.CCAT
                oLinkParms.eLinkMode = ELinkMode.INTERRUPT if eLinkMode == 0 else ELinkMode.POLLING
                oLinkParms.dwInstance = dwInstance
                oLinkParms.oDefault = DN_EC_T_LINK_PARMS_DEFAULT()
                return oLinkParms

            if name == "udp":
                eLinkMode = int(arLinkLayer[2])
                oLinkParms.eLinkType = ELinkType.UDP
                oLinkParms.eLinkMode = ELinkMode.INTERRUPT if eLinkMode == 0 else ELinkMode.POLLING
                oLinkParms.dwInstance = 0
                oLinkParms.oUdp = DN_EC_T_LINK_PARMS_UDP()
                oLinkParms.oUdp.abyIpAddress = EcDemoApp.str_to_ip_address(arLinkLayer[1])
                return oLinkParms
        
            if name == "ndis":
                eLinkMode = int(arLinkLayer[2])
                oLinkParms.eLinkType = ELinkType.NDIS
                oLinkParms.eLinkMode = ELinkMode.INTERRUPT if eLinkMode == 0 else ELinkMode.POLLING
                oLinkParms.dwInstance = 0
                oLinkParms.oNdis = DN_EC_T_LINK_PARMS_NDIS()
                oLinkParms.oNdis.abyIpAddress = EcDemoApp.str_to_ip_address(arLinkLayer[1])
                return oLinkParms
        
            if name == "simulator":
                szEniFilename = arLinkLayer[1]
                dwInstance = int(arLinkLayer[2])
                eLinkMode = int(arLinkLayer[3])
                oLinkParms.eLinkType = ELinkType.Simulator
                oLinkParms.eLinkMode = ELinkMode.INTERRUPT if eLinkMode == 0 else ELinkMode.POLLING
                oLinkParms.dwInstance = dwInstance
                oLinkParms.oSimulator = DN_EC_T_LINK_PARMS_SIMULATOR()
                oLinkParms.oSimulator.szEniFilename = szEniFilename
                oLinkParms.oSimulator.bJobsExecutedByApp = False
                oLinkParms.oSimulator.bConnectHcGroups = True
                return oLinkParms
        except Exception as error:
            self.logMsg(DN_EC_LOG_LEVEL.ERROR, "Invalid link layer settings: '{}'".format(error))    
            return None

        return None

    def initializeEtherCATmaster(self):
        if self.pAppParms.tRunMode == RunMode.Master:
            initMasterParams = DN_EC_T_INIT_MASTER_PARMS()
            initMasterParams.oLinkParms = self.createLinkParms()
            initMasterParams.dwSignature = CEcWrapperPython.s_ATECAT_SIGNATURE()   
            initMasterParams.dwBusCycleTimeUsec = self.pAppParms.dwBusCycleTimeUsec
            initMasterParams.dwMaxBusSlaves = EcDemoApp.c_MASTER_CFG_ECAT_MAX_BUS_SLAVES    
            initMasterParams.dwMaxAcycFramesQueued = EcDemoApp.c_MASTER_CFG_MAX_ACYC_FRAMES_QUEUED    
            initMasterParams.dwMaxAcycBytesPerCycle = EcDemoApp.c_MASTER_CFG_MAX_ACYC_BYTES_PER_CYC    
            initMasterParams.dwEcatCmdMaxRetries = EcDemoApp.c_MASTER_CFG_MAX_ACYC_CMD_RETRIES    

            initMasterParams.dwLogLevel = DN_EC_LOG_LEVEL(self.pAppParms.dwMasterLogLevel)    

            oRasParms = None
            if self.pAppParms.wRasServerPort != 0:
                oRasParms = DN_EC_T_INITRASPARAMS()
                oRasParms.wPort = self.pAppParms.wRasServerPort

            self.oEcWrapper = CEcWrapperPythonEx()
            self.onDbgMsgNotificationId = self.oEcWrapper.AddNotificationHandler("onDbgMsg", self.onDbgMsgNotification)
            self.onMasterNotificationId = self.oEcWrapper.AddNotificationHandler("onMaster", self.onMasterNotification)
            self.onRasNotificationId = self.oEcWrapper.AddNotificationHandler("onRas", self.onRasNotification)
            self.oEcWrapper.ThrottleNotification(DN_NotifyCode.CYCCMD_WKC_ERROR, 1000)    
            self.oEcWrapper.ThrottleNotification(DN_NotifyCode.NOT_ALL_DEVICES_OPERATIONAL, 1000)
            dwRes = self.oEcWrapper.InitWrapper(0, initMasterParams, oRasParms, None, False)    
            if dwRes != ECError.EC_NOERROR:
                self.logMasterError("myAppInit failed: ", dwRes)    
                return dwRes
            return ECError.EC_NOERROR

        if self.pAppParms.tRunMode == RunMode.Simulator:
            initSimulatorParams = DN_EC_T_SIMULATOR_INIT_PARMS()
            initSimulatorParams.oLinkParms = self.createLinkParms()
            initSimulatorParams.dwBusCycleTimeUsec = self.pAppParms.dwBusCycleTimeUsec
            initSimulatorParams.dwLogLevel = DN_EC_LOG_LEVEL(self.pAppParms.dwMasterLogLevel)

            oRasParms = None
            if self.pAppParms.wRasServerPort != 0:
                oRasParms = DN_EC_T_INITRASPARAMS()
                oRasParms.wPort = self.pAppParms.wRasServerPort

            self.oEcWrapper = CEcWrapperPythonEx()
            self.onDbgMsgNotificationId = self.oEcWrapper.AddNotificationHandler("onDbgMsg", self.onDbgMsgNotification)
            self.onMasterNotificationId = self.oEcWrapper.AddNotificationHandler("onMaster", self.onMasterNotification)
            self.onRasNotificationId = self.oEcWrapper.AddNotificationHandler("onRas", self.onRasNotification)
            self.oEcWrapper.ThrottleNotification(DN_NotifyCode.CYCCMD_WKC_ERROR, 1000)    
            self.oEcWrapper.ThrottleNotification(DN_NotifyCode.NOT_ALL_DEVICES_OPERATIONAL, 1000)    
            dwRes = self.oEcWrapper.InitWrapper(0, None, oRasParms, None, False, True, initSimulatorParams)    
            if dwRes != ECError.EC_NOERROR:
                self.logMasterError("Cannot initialize simulator: ", dwRes)    
                return dwRes
            return ECError.EC_NOERROR

        if self.pAppParms.tRunMode == RunMode.RasClient:
            oRasParms = DN_EC_T_INITRASPARAMS()
            oRasParms.abyIpAddr = [int(octet) for octet in self.pAppParms.abyRasServerIpAddress.split(".")]
            oRasParms.wPort = self.pAppParms.wRasServerPort

            self.oEcWrapper = CEcWrapperPythonEx()
            self.onDbgMsgNotificationId = self.oEcWrapper.AddNotificationHandler("onDbgMsg", self.onDbgMsgNotification)
            self.onMasterNotificationId = self.oEcWrapper.AddNotificationHandler("onMaster", self.onMasterNotification)
            self.onRasNotificationId = self.oEcWrapper.AddNotificationHandler("onRas", self.onRasNotification)
            dwRes = self.oEcWrapper.InitWrapper(0, None, oRasParms, None, False)    
            if dwRes != ECError.EC_NOERROR:
                self.logMasterError("Cannot initialize RAS client: ", dwRes)    
                return dwRes
            return ECError.EC_NOERROR

        if self.pAppParms.tRunMode == RunMode.MbxGateway:
            oMbxGatewayParms = DN_EC_T_INIT_MBXGATEWAY_PARMS()
            oMbxGatewayParms.abyIpAddr = [int(octet) for octet in self.pAppParms.abyRasServerIpAddress.split(".")]
            oMbxGatewayParms.wPort = self.pAppParms.wRasServerPort

            self.oEcWrapper = CEcWrapperPythonEx()
            self.onDbgMsgNotificationId = self.oEcWrapper.AddNotificationHandler("onDbgMsg", self.onDbgMsgNotification)
            self.onMasterNotificationId = self.oEcWrapper.AddNotificationHandler("onMaster", self.onMasterNotification)
            self.onRasNotificationId = self.oEcWrapper.AddNotificationHandler("onRas", self.onRasNotification)
            dwRes = self.oEcWrapper.InitWrapper(0, None, None, oMbxGatewayParms, False)    
            if dwRes != ECError.EC_NOERROR:
                self.logMasterError("Cannot initialize mailbox gateway: ", dwRes)    
                return dwRes
            return ECError.EC_NOERROR

        self.logMasterError("initializeEtherCATmaster failed ", ECError.EC_INVALIDPARM)    
        return ECError.EC_INVALIDPARM

    def onDbgMsgNotification(self, type_, severity, msg):
        self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "{0}".format(msg.rstrip()))
        return

    def onMasterNotification(self, type_, code, data, errMsgs):
        self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Master: Type={0}, Code={1}, Msg={2}".format(type_, code, errMsgs))
        return

    def onRasNotification(self, type_, code, data, errMsgs):
        self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "RAS: Type={0}, Code={1}".format(type_, code))
        return

    def deinitializeEtherCATmaster(self):
        if self.pAppParms.tRunMode != RunMode.Unknown:
            dwRes = self.oEcWrapper.UnregisterClient()
            if dwRes != ECError.EC_NOERROR:
                self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "Cannot unregister client: %s (0x%lx))\n", self.oEcWrapper.GetErrorText(dwRes), dwRes)
                return dwRes

        if self.pAppParms.tRunMode != RunMode.Unknown:
            if self.onDbgMsgNotificationId != -1:
                self.oEcWrapper.RemoveNotificationHandler(self.onDbgMsgNotificationId)
                self.onDbgMsgNotificationId = -1
            if self.onMasterNotificationId != -1:
                self.oEcWrapper.RemoveNotificationHandler(self.onMasterNotificationId)
                self.onMasterNotificationId = -1
            if self.onRasNotificationId != -1:
                self.oEcWrapper.RemoveNotificationHandler(self.onRasNotificationId)
                self.onRasNotificationId = -1

            dwRes = self.oEcWrapper.DeinitWrapper()
            if dwRes != ECError.EC_NOERROR:
                self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "Cannot de-initialize EtherCAT-Master: %s (0x%lx)\n", self.oEcWrapper.GetErrorText(dwRes), dwRes)    
                return ECError.EC_NOERROR
        return ECError.EC_NOERROR

    def tEcJobTask(self):
        self.m_bJobTaskRunning = True

        while not self.m_bJobTaskShutDown:
            try:
                bPrevCycProcessedArr = CEcWrapperPythonOutParam()
                self.oEcWrapper.ExecJobProcessAllRxFrames(bPrevCycProcessedArr)    
  
                if self.pAppParms.tRunMode == RunMode.Simulator:
                    self.myAppWorkpd()    

                    #/* run the simulator timer handler */
                    self.oEcWrapper.ExecJob(DN_EC_T_USER_JOB.SimulatorTimer)    
                else:
                    eMasterState = self.oEcWrapper.GetMasterState()    
                    if eMasterState in {DN_EC_T_STATE.SAFEOP, DN_EC_T_STATE.OP}:
                        self.myAppWorkpd()    

                    #/* write output values from current cycle, by sending all cyclic frames */
                    #/* send all cyclic frames (write new output values) */
                    self.oEcWrapper.ExecJob(DN_EC_T_USER_JOB.SendAllCycFrames)    

                    #/* run the master timer handler */
                    self.oEcWrapper.ExecJob(DN_EC_T_USER_JOB.MasterTimer)    

                    #/* send all queued acyclic EtherCAT frames */
                    self.oEcWrapper.ExecJob(DN_EC_T_USER_JOB.SendAcycFrames)    
            except CEcWrapperPythonException:
                pass

            #/* Wait for the next cycle */
            time.sleep(self.m_nCycleTime / 1000)

        self.m_bJobTaskRunning = False    


    def runDemo(self):
        endTimeInMs = 0
        if self.pAppParms.dwDemoDuration != 0:
            endTimeInMs = time.time()*1000.0 + self.pAppParms.dwDemoDuration
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "%s runtime: %ds ...\n", EC_DEMO_APP_NAME, self.pAppParms.dwDemoDuration / 1000)    
        try:
            while True:
                if endTimeInMs > 0 and time.time() * 1000.0 >= endTimeInMs:
                    break
                self.myAppDiagnosis()    
                time.sleep(5 / 1000)
        except KeyboardInterrupt:
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Stopped by user")    
        return ECError.EC_NOERROR


    @staticmethod
    def is_bit_set(value, bit):
        return (1 << bit) == (value & (1 << bit))


    def printSlaveInfos(self):
        #/* get information about all bus slaves */
        for i in range(65535, 0, -1):
            wAutoIncAddress = i + 1
            oBusSlaveInfoArr = CEcWrapperPythonOutParam()

            #/* get bus slave information */
            try:
                dwRes = self.oEcWrapper.GetBusSlaveInfo(False, wAutoIncAddress, oBusSlaveInfoArr)    
                if dwRes != ECError.EC_NOERROR:
                    break    
            except CEcWrapperPythonException as error:
                if error.code == ECError.EC_NOTFOUND:
                    break    
                raise

            oBusSlaveInfo = oBusSlaveInfoArr.value
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "******************************************************************************\n")    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Slave ID............: 0x%08X\n", oBusSlaveInfo.dwSlaveId)    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Bus Index...........: %d\n", (0 - wAutoIncAddress))    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Bus AutoInc Address.: 0x%04x (%4d)\n", oBusSlaveInfo.wAutoIncAddress, oBusSlaveInfo.wAutoIncAddress)    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Bus Station Address.: 0x%04x (%4d)\n", oBusSlaveInfo.wStationAddress, oBusSlaveInfo.wStationAddress)    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Bus Alias Address...: 0x%04x (%4d)\n", oBusSlaveInfo.wAliasAddress, oBusSlaveInfo.wAliasAddress)    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Vendor ID...........: 0x%08X = %s\n", oBusSlaveInfo.dwVendorId, CEcWrapperPython.SlaveVendorText(oBusSlaveInfo.dwVendorId))    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Product Code........: 0x%08X = %s\n", oBusSlaveInfo.dwProductCode, CEcWrapperPython.SlaveProdCodeText(oBusSlaveInfo.dwVendorId, oBusSlaveInfo.dwProductCode))    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Revision............: 0x%08X   Serial Number: %d\n", oBusSlaveInfo.dwRevisionNumber, oBusSlaveInfo.dwSerialNumber)    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "ESC Type............: %s (0x%x)  Revision: %d  Build: %d\n", CEcWrapperPython.ESCTypeText(oBusSlaveInfo.byESCType, True), oBusSlaveInfo.byESCType, oBusSlaveInfo.byESCRevision, oBusSlaveInfo.wESCBuild)    
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Connection at Port A: %s (to 0x%08X)\n", "yes" if self.is_bit_set(oBusSlaveInfo.wPortState, 0) else "no", oBusSlaveInfo.adwPortSlaveIds[0])
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Connection at Port D: %s (to 0x%08X)\n", "yes" if self.is_bit_set(oBusSlaveInfo.wPortState, 3) else "no", oBusSlaveInfo.adwPortSlaveIds[3])
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Connection at Port B: %s (to 0x%08X)\n", "yes" if self.is_bit_set(oBusSlaveInfo.wPortState, 1) else "no", oBusSlaveInfo.adwPortSlaveIds[1])
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Connection at Port C: %s (to 0x%08X)\n", "yes" if self.is_bit_set(oBusSlaveInfo.wPortState, 2) else "no", oBusSlaveInfo.adwPortSlaveIds[2])
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Line Crossed........: %s\n", "yes" if oBusSlaveInfo.bLineCrossed else "no")
            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Line Crossed Flags..: 0x%x\n", oBusSlaveInfo.wLineCrossedFlags)

            oCfgSlaveInfoArr = CEcWrapperPythonOutParam()

            #/* get cfg slave information (matching bus slave) */
            dwRes = self.oEcWrapper.GetCfgSlaveInfo(True, oBusSlaveInfo.wStationAddress, oCfgSlaveInfoArr)    
            if dwRes != ECError.EC_NOERROR:
                continue    

            oCfgSlaveInfo = oCfgSlaveInfoArr.value

            self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "Cfg Station Address.: 0x%04x (%4d)\n", oCfgSlaveInfo.wStationAddress, oCfgSlaveInfo.wStationAddress)    
            if oCfgSlaveInfo.dwPdSizeIn:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD IN    Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsIn // 8, oCfgSlaveInfo.dwPdOffsIn % 8, oCfgSlaveInfo.dwPdSizeIn)    
            if oCfgSlaveInfo.dwPdSizeOut:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD OUT   Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsOut // 8, oCfgSlaveInfo.dwPdOffsOut % 8, oCfgSlaveInfo.dwPdSizeOut)    

            if oCfgSlaveInfo.dwPdSizeIn2:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD IN  2 Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsIn2 // 8, oCfgSlaveInfo.dwPdOffsIn2 % 8, oCfgSlaveInfo.dwPdSizeIn2)    
            if oCfgSlaveInfo.dwPdSizeOut2:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD OUT 2 Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsOut2 // 8, oCfgSlaveInfo.dwPdOffsOut2 % 8, oCfgSlaveInfo.dwPdSizeOut2)    

            if oCfgSlaveInfo.dwPdSizeIn3:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD IN  3 Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsIn3 // 8, oCfgSlaveInfo.dwPdOffsIn3 % 8, oCfgSlaveInfo.dwPdSizeIn3)    
            if oCfgSlaveInfo.dwPdSizeOut3:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD OUT 3 Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsOut3 // 8, oCfgSlaveInfo.dwPdOffsOut3 % 8, oCfgSlaveInfo.dwPdSizeOut3)    
            if oCfgSlaveInfo.dwPdSizeIn4:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD IN  4 Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsIn4 // 8, oCfgSlaveInfo.dwPdOffsIn4 % 8, oCfgSlaveInfo.dwPdSizeIn4)    
            if oCfgSlaveInfo.dwPdSizeOut4:
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "PD OUT 4 Byte.Bit offset: %d.%d   Size: %d bits\n", oCfgSlaveInfo.dwPdOffsOut4 // 8, oCfgSlaveInfo.dwPdOffsOut4 % 8, oCfgSlaveInfo.dwPdSizeOut4)    

        self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "******************************************************************************\n")    
        return True

    #/***************************************************************************************************/
    #/**
    #\brief  Initialize Application
    #
    #\return EC_E_NOERROR on success, error code otherwise. todo update
    #*/
    def myAppInit(self):
        self.pMyAppDesc.wFlashSlaveAddr = self.pAppParms.wFlashSlaveAddr
        return ECError.EC_NOERROR

    #/***************************************************************************************************/
    #/**
    #\brief  Initialize Slave Instance.

    #Find slave parameters.
    #\return EC_E_NOERROR on success, error code otherwise. //todo
    #*/
    def myAppPrepare(self):

        if self.pMyAppDesc.wFlashSlaveAddr != 0xFFFF:
            #/* check if slave address is provided */
            if self.pMyAppDesc.wFlashSlaveAddr != 0:
                wFixedAddress = self.pMyAppDesc.wFlashSlaveAddr

                #/* now get the offset of this device in the process data buffer and some other infos */
                oCfgSlaveInfoArr = CEcWrapperPythonOutParam()
                dwRes = self.oEcWrapper.GetCfgSlaveInfo(True, wFixedAddress, oCfgSlaveInfoArr)    
                if dwRes != ECError.EC_NOERROR:
                    self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "ERROR: ecatGetCfgSlaveInfo() returns with error=0x%x, slave address=%d\n", dwRes, wFixedAddress)    
                else:
                    oCfgSlaveInfo = oCfgSlaveInfoArr.value
                    if oCfgSlaveInfo.dwPdSizeOut != 0:
                        self.pMyAppDesc.dwFlashPdBitSize = oCfgSlaveInfo.dwPdSizeOut    
                        self.pMyAppDesc.dwFlashPdBitOffs = oCfgSlaveInfo.dwPdOffsOut    
                    else:
                        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "Slave address=%d has no outputs, therefore flashing not possible\n", wFixedAddress)    
            #else:
            #    #/* get complete process data output size */
            #    EC_T_MEMREQ_DESC oPdMemorySize    
            #    OsMemset(&oPdMemorySize, 0, sizeof(EC_T_MEMREQ_DESC))    

            #    dwRes = ecatIoCtl(EC_IOCTL_GET_PDMEMORYSIZE, EC_NULL, 0, (EC_T_VOID*)&oPdMemorySize, sizeof(EC_T_MEMREQ_DESC), EC_NULL)    
            #    if (dwRes != ECError.EC_NOERROR):
            #        self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "ecatIoControl(EC_IOCTL_GET_PDMEMORYSIZE) returns with error=0x%x\n", dwRes)    
            #        return dwRes
            #    self.pMyAppDesc.dwFlashPdBitSize = oPdMemorySize.dwPDOutSize * 8    

            if self.pMyAppDesc.dwFlashPdBitSize > 0:
                self.pMyAppDesc.dwFlashInterval = 20000     #/* flash every 20 msec */
                self.pMyAppDesc.dwFlashBufSize = 0 #BIT2BYTE(self.pMyAppDesc.dwFlashPdBitSize)    
                self.pMyAppDesc.pbyFlashBuf = 0 #(EC_T_BYTE*)OsMalloc(self.pMyAppDesc.dwFlashBufSize)    
                #OsMemset(self.pMyAppDesc.pbyFlashBuf, 0 , self.pMyAppDesc.dwFlashBufSize)    


    #/***************************************************************************************************/
    #/**
    #\brief  Setup slave parameters (normally done in PREOP state

    #  - SDO up- and Downloads
    #  - Read Object Dictionary

    #\return EC_E_NOERROR on success, error code otherwise.
    #*/
    def myAppSetup(self):
        pass

    def myAppWorkpd(self):
        """
        demo application working process data function.
        This function is called in every cycle after the the master stack is started.
        """
        #/* demo code flashing */
        if self.pMyAppDesc.dwFlashPdBitSize != 0:

            self.pMyAppDesc.dwFlashTimer += self.pAppParms.dwBusCycleTimeUsec    
            if self.pMyAppDesc.dwFlashTimer >= self.pMyAppDesc.dwFlashInterval:
                self.pMyAppDesc.dwFlashTimer = 0    

                #/* flash with pattern */
                self.pMyAppDesc.byFlashVal = self.pMyAppDesc.byFlashVal + 1    
                #OsMemset(pMyAppDesc->pbyFlashBuf, pMyAppDesc->byFlashVal, pMyAppDesc->dwFlashBufSize)    

                #/* update PdOut */
                #EC_COPYBITS(pbyPdOut, pMyAppDesc->dwFlashPdBitOffs, pMyAppDesc->pbyFlashBuf, 0, pMyAppDesc->dwFlashPdBitSize)    

        return ECError.EC_NOERROR

    #/***************************************************************************************************/
    #/**
    #\brief  demo application doing some diagnostic tasks

    #  This function is called in sometimes from the main demo task
    #*/
    def myAppDiagnosis(self):
        return ECError.EC_NOERROR

    def startDemo(self):
        dwRes = ECError.EC_NOERROR
        try:
            self.setAppAndMasterLogLevel()
            if self.logger.initLogger(self.pAppParms.dwAppLogLevel, self.pAppParms.szLogFileprefix) == False:
                return None

            dwRes = self.myAppInit()
            if dwRes != ECError.EC_NOERROR:
                self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "myAppInit failed: %s (0x%lx))\n", self.oEcWrapper.GetErrorText(dwRes), dwRes)
                return dwRes
            dwRes = self.initializeEtherCATmaster()
            if dwRes != ECError.EC_NOERROR:
                return dwRes

            # /* print MAC address */
            oSrcMacAddressArr = CEcWrapperPythonOutParam()
            dwRes = self.oEcWrapper.GetSrcMacAddress(oSrcMacAddressArr)
            if dwRes != ECError.EC_NOERROR:
                self.logMasterError("Cannot get MAC address: ", dwRes)    
            else:
                oSrcMacAddress = oSrcMacAddressArr.value
                self.logger.logMsg(DN_EC_LOG_LEVEL.INFO, "EtherCAT network adapter MAC: %02X-%02X-%02X-%02X-%02X-%02X\n", *oSrcMacAddress.b)

            #/* create cyclic task to trigger jobs */
            if (self.pAppParms.tRunMode in {RunMode.Master, RunMode.Simulator}) and self.m_bJobTaskRunning == False:
                self.m_bJobTaskShutDown = False
                self.m_oJobTask = Thread(target=self.tEcJobTask)
                self.m_oJobTask.start()

            if self.pAppParms.szENIFilename:
                if self.pAppParms.tRunMode == RunMode.Master:
                    dwRes = self.oEcWrapper.ConfigureMaster(DN_EC_T_CNF_TYPE.Filename, self.pAppParms.szENIFilename, len(self.pAppParms.szENIFilename))
                    if dwRes != ECError.EC_NOERROR:
                        self.logMasterError("Cannot configure EtherCAT-Master: ", dwRes)    
                        return dwRes

                if self.pAppParms.tRunMode == RunMode.Simulator:
                    dwRes = self.oEcWrapper.ConfigureNetwork(DN_EC_T_CNF_TYPE.Filename, self.pAppParms.szENIFilename, len(self.pAppParms.szENIFilename))
                    if dwRes != ECError.EC_NOERROR:
                        self.logMasterError("Cannot configure EtherCAT-Simulator: ", dwRes)    
                        return dwRes

            oReg = CEcWrapperPythonOutParam()
            dwRes = self.oEcWrapper.RegisterClient(oReg)
            if dwRes != ECError.EC_NOERROR:
                self.logMasterError("Cannot register client: ", dwRes)    
                return dwRes

            #/* print found slaves */
            if self.pAppParms.dwAppLogLevel.value >= DN_EC_LOG_LEVEL.VERBOSE:
                if self.pAppParms.tRunMode == RunMode.Master:
                    dwRes = self.oEcWrapper.ScanBus(EcDemoApp.ETHERCAT_SCANBUS_TIMEOUT)
                if dwRes in {ECError.EC_NOERROR, ECError.EC_BUSCONFIG_MISMATCH, ECError.EC_LINE_CROSSED}:
                    self.printSlaveInfos()    
                else:
                    self.logMasterError("Cannot scan bus: ", dwRes)    

            if self.pAppParms.tRunMode == RunMode.Master and self.pAppParms.szENIFilename != "":
                dwRes = self.oEcWrapper.SetMasterState(EcDemoApp.ETHERCAT_STATE_CHANGE_TIMEOUT, DN_EC_T_STATE.INIT)
                if dwRes != ECError.EC_NOERROR:
                    self.logMasterError("Cannot set master state to INIT: ", dwRes)    
                    return dwRes

                self.myAppPrepare()

                dwRes = self.oEcWrapper.SetMasterState(EcDemoApp.ETHERCAT_STATE_CHANGE_TIMEOUT, DN_EC_T_STATE.PREOP)
                if dwRes != ECError.EC_NOERROR:
                    self.logMasterError("Cannot set master state to PREOP: ", dwRes)    
                    return dwRes

                self.myAppSetup()

                dwRes = self.oEcWrapper.SetMasterState(EcDemoApp.ETHERCAT_STATE_CHANGE_TIMEOUT, DN_EC_T_STATE.SAFEOP)
                if dwRes != ECError.EC_NOERROR:
                    self.logMasterError("Cannot set master state to SAFEOP: ", dwRes)    
                    return dwRes

                dwRes = self.oEcWrapper.SetMasterState(EcDemoApp.ETHERCAT_STATE_CHANGE_TIMEOUT, DN_EC_T_STATE.OP)
                if dwRes != ECError.EC_NOERROR:
                    self.logMasterError("Cannot set master state to OP: ", dwRes)    
                    return dwRes
                
            self.processImage.reload()    
            #self.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.set(1)
            #self.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.get()
        except CEcWrapperPythonException as e:
            self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, str(e))
        
        return dwRes


    def stopDemo(self):
        if self.pAppParms.tRunMode == RunMode.Master:
            dwRes = self.oEcWrapper.SetMasterState(EcDemoApp.ETHERCAT_STATE_CHANGE_TIMEOUT, DN_EC_T_STATE.INIT)
            if dwRes != ECError.EC_NOERROR:
                self.logger.logMsg(DN_EC_LOG_LEVEL.ERROR, "Cannot start set master state to INIT: %s (0x%lx))\n", self.oEcWrapper.GetErrorText(dwRes), dwRes)
                return dwRes
        #/* shutdown JobTask */
        if self.m_oJobTask != None:
            self.m_bJobTaskShutDown = True
            while self.m_bJobTaskRunning:
                time.sleep(50 / 1000)    
            self.m_oJobTask.join()
            self.m_oJobTask = None
        #/* deinitialize master */
        dwRes = self.deinitializeEtherCATmaster()
        if dwRes != ECError.EC_NOERROR:
            return dwRes

        return ECError.EC_NOERROR

    def help(self):
        print("Interactive help:")
        print("- demo.startDemo(): start demo")
        print("- demo.stopDemo(): stop demo")
        print("- demo.pAppParms: demo parameters")
        print("- demo.processImage: process image")
        print("  - e.g. write variable")
        print("    demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.set(1)")
        print("  - e.g. read variable")
        print("    demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.get()")
        return
       
    def main(self, argv):
        if self.parseCommandLine(argv) == False:
            return
        dwRes = self.startDemo()
        if dwRes != ECError.EC_NOERROR:
            return
        dwRes = self.runDemo()
        if dwRes != ECError.EC_NOERROR:
            return
        dwRes = self.stopDemo()
        if dwRes != ECError.EC_NOERROR:
            return

class EcMasterDemoPython(EcDemoApp):
    def __init__(self):
        EcDemoApp.__init__(self)

if __name__ == "__main__":
    CEcWrapperPython.EnableExceptionHandling = False # True, to throw exception in case of error
    demo = EcMasterDemoPython()
    demo.main(sys.argv[1:])
