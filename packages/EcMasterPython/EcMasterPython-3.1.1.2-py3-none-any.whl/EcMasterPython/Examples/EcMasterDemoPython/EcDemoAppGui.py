#/*-----------------------------------------------------------------------------
# * EcDemoAppGui.py
# * Copyright                acontis technologies GmbH, Ravensburg, Germany
# * Description              EC-Master demo GUI application for Python
# *---------------------------------------------------------------------------*/
# pylint: disable=unused-wildcard-import, wildcard-import, unused-argument
import os
import sys
import platform
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QSettings    
from PyQt5 import uic
from EcWrapperPython import *
from EcWrapperPythonTypes import *
from enum import Enum
from threading import Thread
import threading
import time

EC_DEMO_COMPANY = "acontis_technologies"
EC_DEMO_APP_NAME = "EcMasterDemoGuiPython"
EC_DEMO_SIMULATOR = False
LOG_LEVEL = DN_EC_LOG_LEVEL.WARNING #VERBOSE_CYC

class SlaveData:
    def __init__(self):
        self.StationAddress = 0
        self.SupportedMbxProtocols = 0 #(EMbxProtocol)
        self.Variables = []

class EcDemoAppGui(QMainWindow, uic.loadUiType(os.path.dirname(os.path.abspath(__file__)) + "/EcDemoAppGui.ui")[0]):
    c_MASTER_CFG_ECAT_MAX_BUS_SLAVES = 256
    c_MASTER_CFG_MAX_ACYC_FRAMES_QUEUED = 32    #/* max number of acyc frames queued, 127 = the absolute maximum number */
    c_MASTER_CFG_MAX_ACYC_BYTES_PER_CYC = 4096  #/* max number of bytes sent during eUsrJob_SendAcycFrames within one cycle */
    c_MASTER_CFG_MAX_ACYC_CMD_RETRIES = 3

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.geometry().width(),self.geometry().height())
        if CEcWrapperPython.ECWRAPPER_EVAL_VERSION:
            self.setWindowTitle(EC_DEMO_APP_NAME + " (Eval)")        
        else:
            self.setWindowTitle(EC_DEMO_APP_NAME)        
        self.slaves = []
        self.m_oEcWrapper = None
        self.onDbgMsgNotificationId = -1
        self.onMasterNotificationId = -1
        self.onRasNotificationId = -1
        self.m_oJobTask = None
        self.m_bJobTaskRunning = False
        self.m_bJobTaskShutDown = False
        self.m_nCycleTime = 4

        # timer for re-schedule master messages into gui thread
        self.m_oTimerLock = threading.Lock() 
        self.m_oTimerNotifications = []
        self.m_oTimer = QtCore.QTimer()
        self.m_oTimer.setInterval(300)
        self.m_oTimer.timeout.connect(self.onTimer)
        self.m_oTimer.start()

        # main
        self.btnStartMaster = self.findChild(QtWidgets.QPushButton, 'pushButton') 
        self.btnStartMaster.clicked.connect(self.onStartMasterClicked)
        self.btnStopMaster = self.findChild(QtWidgets.QPushButton, 'pushButton_2') 
        self.btnStopMaster.clicked.connect(self.onStopMasterClicked)
        self.btnClearLog = self.findChild(QtWidgets.QPushButton, 'pushButton_3') 
        self.btnClearLog.clicked.connect(self.onClearLogClicked)
        self.txtLog = self.findChild(QtWidgets.QTextEdit, 'textEdit') 
        self.tcMain = self.findChild(QtWidgets.QTabWidget, 'tabWidget') 
        self.tpConfiguration = self.findChild(QWidget, 'tab')
        self.tpDiagnosis = self.findChild(QWidget, 'tab_2')

        # configuration
        self.txtIpAddressBox = self.findChild(QtWidgets.QTextEdit, 'textEdit_3') 
        self.nudMasterCycleTime = self.findChild(QtWidgets.QSpinBox, 'spinBox') 
        self.cbRasServer = self.findChild(QtWidgets.QCheckBox, 'checkBox') 
        self.nudRasServerPort = self.findChild(QtWidgets.QSpinBox, 'spinBox_2') 
        self.cbRasClientEnabled = self.findChild(QtWidgets.QCheckBox, 'checkBox_2') 
        self.tbEniFilePath = self.findChild(QtWidgets.QTextEdit, 'textEdit_2') 
        self.btnBrowseEniFile = self.findChild(QtWidgets.QToolButton, 'toolButton') 
        self.btnBrowseEniFile.clicked.connect(self.onBrowseEniFileClicked)
        self.txtIpAddressBox.setText("127.0.0.1")

        # diagnosis
        self.tbCurMasterState = self.findChild(QtWidgets.QTextEdit, 'textEdit_5') 
        self.tbReqMasterState = self.findChild(QtWidgets.QTextEdit, 'textEdit_4') 
        self.btnSetMasterStateInit = self.findChild(QtWidgets.QPushButton, 'pushButton_10') 
        self.btnSetMasterStateInit.clicked.connect(self.onSetMasterStateInitClicked)
        self.btnSetMasterStatePreOp = self.findChild(QtWidgets.QPushButton, 'pushButton_5') 
        self.btnSetMasterStatePreOp.clicked.connect(self.onSetMasterStatePreOpClicked)
        self.btnSetMasterStateSafeOp = self.findChild(QtWidgets.QPushButton, 'pushButton_6') 
        self.btnSetMasterStateSafeOp.clicked.connect(self.onSetMasterStateSafeOpClicked)
        self.btnSetMasterStateOp = self.findChild(QtWidgets.QPushButton, 'pushButton_7') 
        self.btnSetMasterStateOp.clicked.connect(self.onSetMasterStateOpClicked)
        self.cbSlaves = self.findChild(QtWidgets.QComboBox, 'comboBox') 
        self.cbSlaves.currentIndexChanged.connect(self.onSlaveCurrentIndexChanged)
        self.cbVariables = self.findChild(QtWidgets.QComboBox, 'comboBox_2') 
        self.cbVariables.currentIndexChanged.connect(self.onVariablesCurrentIndexChanged)
        self.btnReadDeviceName = self.findChild(QtWidgets.QPushButton, 'pushButton_9') 
        self.btnReadDeviceName.clicked.connect(self.onReadDeviceNameClicked)
        self.tbReadDeviceName = self.findChild(QtWidgets.QTextEdit, 'textEdit_8') 
        self.btnReadPD = self.findChild(QtWidgets.QPushButton, 'pushButton_8') 
        self.btnReadPD.clicked.connect(self.onReadPDClicked)
        self.btnWritePD = self.findChild(QtWidgets.QPushButton, 'pushButton_4') 
        self.btnWritePD.clicked.connect(self.onWritePDClicked)
        self.nudReadPD = self.findChild(QtWidgets.QTextEdit, 'textEdit_7') 
        self.nudReadPD.setText("0")
        self.nudWritePD = self.findChild(QtWidgets.QTextEdit, 'textEdit_6') 
        self.nudWritePD.setText("0")

        # settings
        self.restoreSettings()

        if EC_DEMO_SIMULATOR:
            self.btnSetMasterStateInit.setEnabled(False)
            self.btnSetMasterStatePreOp.setEnabled(False)
            self.btnSetMasterStateSafeOp.setEnabled(False)
            self.btnSetMasterStateOp.setEnabled(False)

        if CEcWrapperPython.ECWRAPPER_EVAL_VERSION:
            self.cbRasServer.setChecked(False)
            self.cbRasServer.setEnabled(False)
            self.nudRasServerPort.setEnabled(False)
            self.cbRasClientEnabled.setChecked(False)
            self.cbRasClientEnabled.setEnabled(False)

        self.setDemoAppState(False)

    def closeEvent(self, event):
        self.saveSettings()
        super(EcDemoAppGui, self).closeEvent(event)

    def restoreSettings(self):
        settings = QSettings(EC_DEMO_COMPANY, EC_DEMO_APP_NAME)
        self.txtIpAddressBox.setText(settings.value('txtIpAddressBox', "127.0.0.1"))
        self.nudMasterCycleTime.setValue(int(settings.value('nudMasterCycleTime', 4000)))
        if settings.value('cbRasServer', False) == "true":
            self.cbRasServer.toggle()
        self.nudRasServerPort.setValue(int(settings.value('nudRasServerPort', 6000)))
        if settings.value('cbRasClient', False) == "true":
            self.cbRasClientEnabled.toggle()
        self.tbEniFilePath.setText(settings.value('tbEniFilePath', ""))

    def saveSettings(self):
        settings = QSettings(EC_DEMO_COMPANY, EC_DEMO_APP_NAME)
        settings.setValue('txtIpAddressBox', self.txtIpAddressBox.toPlainText())
        settings.setValue('nudMasterCycleTime', self.nudMasterCycleTime.text())
        settings.setValue('cbRasServer', self.cbRasServer.isChecked())
        settings.setValue('nudRasServerPort', self.nudRasServerPort.text())
        settings.setValue('cbRasClient', self.cbRasClientEnabled.isChecked())
        settings.setValue('tbEniFilePath', self.tbEniFilePath.toPlainText())

    def onDbgMsgNotificationNoGuiAccess(self, type_, severity, msg):
        self.m_oTimerLock.acquire() 
        self.m_oTimerNotifications.append(["dbg", type_, severity, msg])
        self.m_oTimerLock.release() 

    def onMasterNotificationNoGuiAccess(self, type_, code, data, errMsgs):
        self.m_oTimerLock.acquire() 
        self.m_oTimerNotifications.append(["master", type_, code, data, errMsgs])
        self.m_oTimerLock.release() 

    def onRasNotificationNoGuiAccess(self, type_, code, data, errMsgs):
        self.m_oTimerLock.acquire() 
        self.m_oTimerNotifications.append(["ras", type_, code, data, errMsgs])
        self.m_oTimerLock.release() 

    def onTimer(self):
        with self.m_oTimerLock:
            if len(self.m_oTimerNotifications) == 0:
                return
            notifications = self.m_oTimerNotifications
            self.m_oTimerNotifications = []

        for notification in notifications:
            if notification[0] == "dbg":
                self.onDbgMsgNotification(notification[1], notification[2], notification[3])
            if notification[0] == "master":
                self.onMasterNotification(notification[1], notification[2], notification[3], notification[4])
            if notification[0] == "ras":
                self.onRasNotification(notification[1], notification[2], notification[3], notification[4])

    def onDbgMsgNotification(self, type_, severity, msg):
        self.addLog("{0}".format(msg.rstrip()))

    def onMasterNotification(self, type_, code, data, errMsgs):
        self.addLog("Master: Type={0}, Code={1}".format(type_, code))

        if code == DN_NotifyCode.STATECHANGED:
            masterState = self.m_oEcWrapper.GetMasterState()
            self.updateMasterState(True, masterState)
        elif code == DN_NotifyCode.SB_STATUS:
            oData = data # DN_EC_T_SB_STATUS_NTFY_DESC
            self.ScanBusHandler(code, ECError(oData.dwResultCode), oData.dwSlaveCount)
        elif code == DN_NotifyCode.HC_TOPOCHGDONE:
            oData = data # UInt32
            self.TopoChangeHandler(code)

    def onRasNotification(self, type_, code, data, errMsgs):
        self.addLog("RAS: Type={0}, Code={1}".format(type_, code))

    def onStartMasterClicked(self):
        self.m_oEcWrapper = CEcWrapperPythonEx()

        # /* Add Notification handlers */
        self.onDbgMsgNotificationId = self.m_oEcWrapper.AddNotificationHandler("onDbgMsg", self.onDbgMsgNotificationNoGuiAccess)
        self.onMasterNotificationId = self.m_oEcWrapper.AddNotificationHandler("onMaster", self.onMasterNotificationNoGuiAccess)
        self.onRasNotificationId = self.m_oEcWrapper.AddNotificationHandler("onRas", self.onRasNotificationNoGuiAccess)

        # /* Throttle notifications */
        self.m_oEcWrapper.ThrottleNotification(DN_NotifyCode.CYCCMD_WKC_ERROR, 1000)
        self.m_oEcWrapper.ThrottleNotification(DN_NotifyCode.NOT_ALL_DEVICES_OPERATIONAL, 1000)

        oInitMaster = None
        bSimulator = False
        oInitSimulator = None
        oRasParms = None

        ipAddress = self.txtIpAddressBox.toPlainText()
        cycleTime = int(self.nudMasterCycleTime.text())
        rasServer = self.cbRasServer.isChecked()
        rasPort = self.nudRasServerPort.text()
        rasClient = self.cbRasClientEnabled.isChecked()
        eniFile = self.tbEniFilePath.toPlainText()

        if rasClient:
            ipAddressArr = ipAddress.split(".")
            oRasParms = DN_EC_T_INITRASPARAMS()
            oRasParms.abyIpAddr =  [ int(ipAddressArr[0]), int(ipAddressArr[1]), int(ipAddressArr[2]), int(ipAddressArr[3])]
            oRasParms.wPort = int(rasPort)
            oRasParms.dwLogLevel = LOG_LEVEL
        else:
            oLinkParms = DN_EC_T_LINK_PARMS()

            if platform.system() == "Windows":
                ipAddressArr = ipAddress.split(".")
                oLinkParms.eLinkType = ELinkType.WINPCAP
                oLinkParms.eLinkMode = ELinkMode.POLLING
                oLinkParms.dwInstance = 0
                oLinkParms.oWinPcap = DN_EC_T_LINK_PARMS_WINPCAP()
                oLinkParms.oWinPcap.abyIpAddress = [ int(ipAddressArr[0]), int(ipAddressArr[1]), int(ipAddressArr[2]), int(ipAddressArr[3])]
            else:
                oLinkParms.eLinkType = ELinkType.SOCKRAW
                oLinkParms.eLinkMode = ELinkMode.POLLING
                oLinkParms.dwInstance = 0
                oLinkParms.oSockRaw = DN_EC_T_LINK_PARMS_SOCKRAW()
                oLinkParms.oSockRaw.szAdapterName = ipAddress

            if EC_DEMO_SIMULATOR:
                bSimulator = True
                oInitSimulator = DN_EC_T_SIMULATOR_INIT_PARMS()
                oInitSimulator.oLinkParms = oLinkParms
                oInitSimulator.dwBusCycleTimeUsec = cycleTime
                oInitSimulator.dwLogLevel = LOG_LEVEL
            else:
                oInitMaster = DN_EC_T_INIT_MASTER_PARMS()
                oInitMaster.oLinkParms = oLinkParms
                oInitMaster.dwSignature = CEcWrapperPython.s_ATECAT_SIGNATURE()
                oInitMaster.dwBusCycleTimeUsec = cycleTime
                oInitMaster.dwMaxBusSlaves = EcDemoAppGui.c_MASTER_CFG_ECAT_MAX_BUS_SLAVES
                oInitMaster.dwMaxAcycFramesQueued = EcDemoAppGui.c_MASTER_CFG_MAX_ACYC_FRAMES_QUEUED
                oInitMaster.dwMaxAcycBytesPerCycle = EcDemoAppGui.c_MASTER_CFG_MAX_ACYC_BYTES_PER_CYC
                oInitMaster.dwEcatCmdMaxRetries = EcDemoAppGui.c_MASTER_CFG_MAX_ACYC_CMD_RETRIES
                oInitMaster.dwLogLevel = LOG_LEVEL

            # RAS Srv
            if rasServer:
                oRasParms = DN_EC_T_INITRASPARAMS()
                oRasParms.abyIpAddr = [ 0, 0, 0, 0 ]
                oRasParms.wPort = int(rasPort)
                oRasParms.dwLogLevel = LOG_LEVEL

        dwRes = ECError(self.m_oEcWrapper.InitWrapper(0, oInitMaster, oRasParms, None, False, bSimulator, oInitSimulator))
        if dwRes != ECError.EC_NOERROR:
            self.showMessageBox("Could not initialize Master! Error Text: " + self.m_oEcWrapper.GetErrorText(dwRes))
            return

        if rasClient == False and self.m_bJobTaskRunning == False:
            self.m_bJobTaskShutDown = False
            self.m_oJobTask = Thread(target=self.tEcJobTask)
            self.m_oJobTask.start()

        if rasClient == False:
            #/* now try to configure the master ...*/
            if EC_DEMO_SIMULATOR:
                if len(eniFile) > 0:
                    dwRes = self.m_oEcWrapper.ConfigureNetwork(DN_EC_T_CNF_TYPE.Filename, eniFile, len(eniFile))
                else:
                    dwRes = self.m_oEcWrapper.ConfigureNetwork(DN_EC_T_CNF_TYPE.GenOpENI, None, None)
            else:
                if len(eniFile) > 0:
                    dwRes = self.m_oEcWrapper.ConfigureMaster(DN_EC_T_CNF_TYPE.Filename, eniFile, len(eniFile))
                else:
                    dwRes = self.m_oEcWrapper.ConfigureMaster(DN_EC_T_CNF_TYPE.GenOpENI, None, None)

            #/* Note: EC-STA cannot be configured remotely with GenPreopENI, because it is ALWAYS configured on startup. */
            if dwRes != ECError.EC_NOERROR:
                self.showMessageBox("Could not configure master! Error text: " + self.m_oEcWrapper.GetErrorText(dwRes) + " Please check the set up ENI file path: " + eniFile)
                return

        oReg = CEcWrapperPythonOutParam()
        dwRes = self.m_oEcWrapper.RegisterClient(oReg)
        if dwRes != ECError.EC_NOERROR:
            self.showMasterError("Could not register client:", dwRes)
            return
        
        if self.m_oEcWrapper.GetNumConfiguredSlaves() == 0:
            self.m_oEcWrapper.RestartScanBus(0, False, False)
            return

        masterState = self.m_oEcWrapper.GetMasterState()
        self.updateMasterState(True, masterState)
        self.updateMasterState(False, masterState)
        self.setDemoAppState(True)

        if masterState == DN_EC_T_STATE.UNKNOWN:
            dwRes = self.m_oEcWrapper.SetMasterState(3000, DN_EC_T_STATE.INIT)
            if dwRes != ECError.EC_NOERROR:
                self.showMasterError("Could not set master state to INIT:", dwRes)
                return
            self.updateMasterState(False, DN_EC_T_STATE.INIT)

        self.updateSlaveList()

    def onBrowseEniFileClicked(self):
        files = QFileDialog.getOpenFileName(self, 'Open ENI file', 'eni.xml',"ENI Files (*.xml)")
        if len(files) > 0 and len(files[0]) > 0:
            self.tbEniFilePath.setText(files[0])

    def onStopMasterClicked(self):
        if self.m_oEcWrapper == None:
            return

        self.m_oEcWrapper.UnregisterClient()

        if self.m_oJobTask != None:
            self.m_bJobTaskShutDown = True
            while self.m_bJobTaskRunning:
                time.sleep(50 / 1000)
            self.m_oJobTask.join()
            self.m_oJobTask = None
            
        if self.onDbgMsgNotificationId != -1:
            self.m_oEcWrapper.RemoveNotificationHandler(self.onDbgMsgNotificationId)
            self.onDbgMsgNotificationId = -1
        if self.onMasterNotificationId != -1:
            self.m_oEcWrapper.RemoveNotificationHandler(self.onMasterNotificationId)
            self.onMasterNotificationId = -1
        if self.onRasNotificationId != -1:
            self.m_oEcWrapper.RemoveNotificationHandler(self.onRasNotificationId)
            self.onRasNotificationId = -1

        self.m_oEcWrapper.DeinitWrapper()
        self.m_oEcWrapper = None

        self.setDemoAppState(False)

    def onClearLogClicked(self):
        self.txtLog.setText("")

    def onSetMasterStateInitClicked(self):
        self.setMasterState(DN_EC_T_STATE.INIT)

    def onSetMasterStatePreOpClicked(self):
        self.setMasterState(DN_EC_T_STATE.PREOP)

    def onSetMasterStateSafeOpClicked(self):
        self.setMasterState(DN_EC_T_STATE.SAFEOP)

    def onSetMasterStateOpClicked(self):
        self.setMasterState(DN_EC_T_STATE.OP)

    def setMasterState(self, state):
        self.updateMasterState(False, state)
        eRetVal = self.m_oEcWrapper.SetMasterState(5000, state)
        if eRetVal != ECError.EC_NOERROR:
            self.showMasterError("Could set master state: ", eRetVal)

    def showMessageBox(self, text, icon = QMessageBox.Information):
        msgBox = QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setWindowTitle(EC_DEMO_APP_NAME)
        msgBox.setText(text)
        msgBox.exec()

    def showMasterError(self, text, eRetVal):
        msg = "{}\n{} (0x{:08X})".format(text, self.m_oEcWrapper.GetErrorText(eRetVal), eRetVal)
        self.showMessageBox(msg, QMessageBox.Critical)

    def addLog(self, text):
        self.txtLog.append(text)

    def setDemoAppState(self, running):
        if running:
            self.updateMasterState(True, self.m_oEcWrapper.GetMasterState())
            self.btnStopMaster.setEnabled(True)
            self.btnStartMaster.setEnabled(False)
            self.tpConfiguration.setEnabled(False)
            self.tpDiagnosis.setEnabled(True)
            self.tcMain.setCurrentIndex(1)
        else:
            self.updateMasterState(True, DN_EC_T_STATE.UNKNOWN)
            self.updateMasterState(False, DN_EC_T_STATE.UNKNOWN)
            self.btnStopMaster.setEnabled(False)
            self.btnStartMaster.setEnabled(True)
            self.tpConfiguration.setEnabled(True)
            self.tpDiagnosis.setEnabled(False)
            self.tcMain.setCurrentIndex(0)


    def ScanBusHandler(self, notifCode, eScanBusResult, dwSlaveCount):
        tb_bt_ScanResult_Text = eScanBusResult
        tb_bt_ConnectedSlaves_Text = dwSlaveCount
        tb_bt_ConfiguredSlaves_Text = self.m_oEcWrapper.GetNumConfiguredSlaves()
        self.addLog("ScanBusHandler: Result={0}, Connected={1}, Configured={2}".format(tb_bt_ScanResult_Text, tb_bt_ConnectedSlaves_Text, tb_bt_ConfiguredSlaves_Text))
        self.updateSlaveList()
        return
    
    def TopoChangeHandler(self, dwNotifCode):
        self.updateSlaveList()
        return

    def updateMasterState(self, bCurMasterState, eMasterState):
        if bCurMasterState:
            self.tbCurMasterState.setText(EcDemoAppGui.ecStateToStr(eMasterState))
        else:
            self.tbReqMasterState.setText(EcDemoAppGui.ecStateToStr(eMasterState))

    @staticmethod
    def ecStateToStr(state):
        if state == DN_EC_T_STATE.INIT:
            return "INIT"
        if state == DN_EC_T_STATE.BOOTSTRAP:
            return "BOOTSTRAP"
        if state == DN_EC_T_STATE.PREOP:
            return "PREOP"
        if state == DN_EC_T_STATE.SAFEOP:
            return "SAFEOP"
        if state == DN_EC_T_STATE.OP:
            return "OP"
        return "UNKNOWN"

    def updateSlaveList(self):
        self.slaves.clear()

        # /* Read amount of slaves from Master */
        oStatusArr = CEcWrapperPythonOutParam()
        self.m_oEcWrapper.GetScanBusStatus(oStatusArr)
        oStatus = oStatusArr.value
        if oStatus.dwResultCode == ECError.EC_BUSY: #ECScanBus.BUSY:
            return

        if 0 == oStatus.dwSlaveCount:
            return 

        ## /* Create slave nodes, if slaves are connected */
        for wIdx in range(0, oStatus.dwSlaveCount):
            oSlaveInfoArr = CEcWrapperPythonOutParam()

            # /* Request information about slave object */
            eRetVal = self.m_oEcWrapper.GetSlaveInfo(False, 0 - wIdx, oSlaveInfoArr)
            oSlaveInfo = oSlaveInfoArr.value
            if ECError.EC_NOERROR != eRetVal:
                self.logMasterError("Reading slave info failed: ", eRetVal)
                continue

            slaveData = SlaveData()
            slaveData.StationAddress = oSlaveInfo.wPhysAddress
            slaveData.SupportedMbxProtocols = oSlaveInfo.wSupportedMbxProtocols
            if EC_DEMO_SIMULATOR:
                slaveData.SupportedMbxProtocols = EMbxProtocol.COE # Not supported
            self.slaves.append(slaveData)

        for slaveData in self.slaves:
            inputVariables = self.ReadProcessVariablesFromSlave(slaveData.StationAddress, True)
            if inputVariables != None:
                slaveData.Variables.extend(inputVariables)
            outputVariables = self.ReadProcessVariablesFromSlave(slaveData.StationAddress, False)
            if outputVariables != None:
                slaveData.Variables.extend(outputVariables)

        self.cbSlaves.clear()
        for slaveData in self.slaves:
            self.cbSlaves.addItem(str(slaveData.StationAddress))
        if self.cbSlaves.count() > 0:
            self.cbSlaves.setCurrentIndex(0)

    #/// <summary>Reads all process variables of a slave</summary>
    def ReadProcessVariablesFromSlave(self, wSlaveAddress, input_):
        numOfVariablesArr = CEcWrapperPythonOutParam()
        eRes = ECError.EC_ERROR
        if input_:
            eRes = self.m_oEcWrapper.GetSlaveInpVarInfoNumOf(True, wSlaveAddress, numOfVariablesArr)
        else:
            eRes = self.m_oEcWrapper.GetSlaveOutpVarInfoNumOf(True, wSlaveAddress, numOfVariablesArr)
        numOfVariables = numOfVariablesArr.value
        if eRes != ECError.EC_NOERROR:
            self.logMasterError("Reading number of process variables failed: ", eRes)
            return None

        if numOfVariables == 0:
            return None

        numOfReadVariablesArr = CEcWrapperPythonOutParam()
        variablesArr = CEcWrapperPythonOutParam()
        if input_:
            eRes = self.m_oEcWrapper.GetSlaveInpVarInfo(True, wSlaveAddress, numOfVariables, variablesArr, numOfReadVariablesArr)
        else:
            eRes = self.m_oEcWrapper.GetSlaveOutpVarInfo(True, wSlaveAddress, numOfVariables, variablesArr, numOfReadVariablesArr)
        variables = variablesArr.value
        if eRes != ECError.EC_NOERROR:
            self.logMasterError("Reading process variables failed: ", eRes)
            return None

        return variables
   
    def getAddressOfSelectedSlave(self):     
        if self.cbSlaves.currentText() == "None":
            return 0
        if self.cbSlaves.currentText() == "":
            return 0
        return int(self.cbSlaves.currentText())

    def onSlaveCurrentIndexChanged(self, value):      
        self.cbVariables.clear()

        stationAddress = self.getAddressOfSelectedSlave()
        for slaveData in self.slaves:
            if stationAddress != slaveData.StationAddress:
                continue

            for variable in slaveData.Variables:
                self.cbVariables.addItem(variable.szName)

            if len(slaveData.Variables) == 0:
                self.cbVariables.addItem("None")
            self.cbVariables.setCurrentIndex(0)
            break
 
    def onVariablesCurrentIndexChanged(self, value):      
        self.btnReadDeviceName.setEnabled(False)
        self.cbVariables.setEnabled(False)
        self.btnReadPD.setEnabled(False)
        self.btnWritePD.setEnabled(False)
        self.nudReadPD.setEnabled(False)
        self.nudWritePD.setEnabled(False)

        if self.cbVariables.currentIndex() < 0:
            return

        stationAddress = self.getAddressOfSelectedSlave()
        for slaveData in self.slaves:
            if stationAddress != slaveData.StationAddress:
                continue

            if len(slaveData.Variables) > 0:
                self.cbVariables.setEnabled(True)
                self.btnReadPD.setEnabled(True)
                self.nudReadPD.setEnabled(True)

                variable = slaveData.Variables[self.cbVariables.currentIndex()]
                if not variable.bIsInputData:
                    self.nudWritePD.setEnabled(True)
                    self.btnWritePD.setEnabled(True)

            if (not CEcWrapperPython.ECWRAPPER_EVAL_VERSION and slaveData.SupportedMbxProtocols & EMbxProtocol.COE) != 0:
                self.btnReadDeviceName.setEnabled(True)

            break

    def onReadDeviceNameClicked(self):
        wSlaveAddress = self.getAddressOfSelectedSlave()
        oByteArray = [0] * 1000
        dwLenArr = CEcWrapperPythonOutParam()

        dwSlaveId = self.m_oEcWrapper.GetSlaveId(wSlaveAddress)
        eRes = self.m_oEcWrapper.CoeSdoUpload(dwSlaveId, 0x1008, 0x0, oByteArray, 1000, dwLenArr, 2000, EMailBoxFlags.NONE_)
        if eRes == ECError.EC_NOERROR:
            dwLen = dwLenArr.value
            out_value = CEcWrapperPythonOutParam()
            eRes = CEcWrapperPython.ReadValueFromBytes(oByteArray, 0, dwLen*8, DN_EC_T_DEFTYPE.VISIBLESTRING, out_value)
            if eRes == ECError.EC_NOERROR:
                value = out_value.value
                self.tbReadDeviceName.setText(str(value))
            else:
                self.showMasterError("ReadValueFromBytes failed:", eRes)
        else:
            self.showMasterError("Reading device name failed:", eRes)

    def onReadPDClicked(self):
        stationAddress = self.getAddressOfSelectedSlave()

        if self.cbVariables.currentIndex() == -1:
            return

        for slaveData in self.slaves:
            if stationAddress != slaveData.StationAddress:
                continue

            variable = slaveData.Variables[self.cbVariables.currentIndex()]

            pbyDataDst = [0] * ((variable.nBitSize + 8) // 8)
            dwRes = self.m_oEcWrapper.GetProcessDataBits(not variable.bIsInputData, variable.nBitOffs, pbyDataDst, variable.nBitSize, 2000)
            if dwRes != ECError.EC_NOERROR:
                self.self.showMasterError("Read process data failed:", dwRes)
                return

            out_dataRead = CEcWrapperPythonOutParam()
            eRes = CEcWrapperPython.ReadValueFromBytes(pbyDataDst, 0, variable.nBitSize, DN_EC_T_DEFTYPE(variable.wDataType), out_dataRead)
            if eRes != ECError.EC_NOERROR:
                self.showMasterError("ReadValueFromBytes failed:", dwRes)
                return

            dataRead = out_dataRead.value
            if type(out_dataRead.value) == bool:
                dataRead = 1 if out_dataRead.value == True else 0

            self.nudReadPD.setText(str(dataRead))
            return
    
    def onWritePDClicked(self):
        stationAddress = self.getAddressOfSelectedSlave()
      
        if self.cbVariables.currentIndex() == -1:
            return

        for slaveData in self.slaves:
            if stationAddress != slaveData.StationAddress:
                continue

            variable = slaveData.Variables[self.cbVariables.currentIndex()]
            out_valueAsBytes = CEcWrapperPythonOutParam()
            eRes = CEcWrapperPython.ConvValueToBytes(DN_EC_T_DEFTYPE(variable.wDataType), int(self.nudWritePD.toPlainText()), out_valueAsBytes)
            if eRes != ECError.EC_NOERROR:
                self.showMasterError("ConvValueToBytesfailed:", eRes)
                return

            valueAsBytes = out_valueAsBytes.value
            eRes = self.m_oEcWrapper.SetProcessDataBits(not variable.bIsInputData, variable.nBitOffs, valueAsBytes, variable.nBitSize, 2000)    
            if eRes != ECError.EC_NOERROR:
                self.showMasterError("Write process data failed:", eRes)
                return
            return

    def tEcJobTask(self):
        self.m_bJobTaskRunning = True

        while (self.m_bJobTaskShutDown != True):
            bPrevCycProcessedArr = CEcWrapperPythonOutParam()
            self.m_oEcWrapper.ExecJobProcessAllRxFrames(bPrevCycProcessedArr)

            if EC_DEMO_SIMULATOR:
                #/* run the master timer handler */
                self.m_oEcWrapper.ExecJob(DN_EC_T_USER_JOB.SimulatorTimer)
            else:
                #/* write output values from current cycle, by sending all cyclic frames */
                #/* send all cyclic frames (write new output values) */
                self.m_oEcWrapper.ExecJob(DN_EC_T_USER_JOB.SendAllCycFrames)

                #/* run the master timer handler */
                self.m_oEcWrapper.ExecJob(DN_EC_T_USER_JOB.MasterTimer)

                #/* send all queued acyclic EtherCAT frames */
                self.m_oEcWrapper.ExecJob(DN_EC_T_USER_JOB.SendAcycFrames)

            #/* Wait for the next cycle */
            time.sleep(self.m_nCycleTime / 1000)

        self.m_bJobTaskRunning = False

    def logMasterError(self, message, eRes):
        self.addLog(message + self.m_oEcWrapper.GetErrorText(eRes))


class EcMasterDemoGuiPython(EcDemoAppGui):
    def __init__(self):
        EcDemoAppGui.__init__(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = EcMasterDemoGuiPython()
    mainWin.show()
    sys.exit( app.exec_() )