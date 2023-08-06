#/*-----------------------------------------------------------------------------
# * EcWrapperPython.py
# * Copyright                acontis technologies GmbH, Ravensburg, Germany
# * Description              EC-Master Python Interface
# *---------------------------------------------------------------------------*/
# pylint: disable=anomalous-backslash-in-string, unused-wildcard-import, wildcard-import
from EcWrapperPythonTypes import *
from EcWrapperTypes import *
from EcWrapper import *
import os
import sys
import platform
import datetime
import threading
import inspect

# Native internal function pointers
NativeEcEventNotif = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p)
NativeRapiNotif = ctypes.CFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p)
NativePerfNotif = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint)
NativeTranslateNotif = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_uint, SDN_EC_STRING_HLP)
NativeDbgMsgNotif = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p)


class ThrottleElem:
    def __init__(self):
        self.tNotifyCode = DN_NotifyCode.STATECHANGED # DN_NotifyCode
        self.nLastSeen = 0 # long
        self.dwTimeout = 0 # uint


class CEcWrapperPython:
    REMOTE_CYCLE_TIME = 2
    REMOTE_WD_TO_LIMIT = 10000
    REMOTE_RECV_THREAD_PRIO = 0 #//((EC_T_DWORD) THREAD_PRIORITY_NORMAL)
    MAIN_THREAD_PRIO = 0 #//((EC_T_DWORD) THREAD_PRIORITY_NORMAL)
    ECWRAPPER_EVAL_VERSION = True
    ECWRAPPER_API_VERSION = 1612540388
    EnableExceptionHandling = False
    m_dwRasConnectionCounter = 0
    m_dwMbxGatewayConnectionCounter = 0
    m_szInstallDir = ""
    DATE_SINCE_1970 = datetime.datetime(1970,1,1)
    m_oInstances = []
    m_oInstancesLock = threading.Lock()
    
    @staticmethod
    def s_ATECAT_VERSION():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_ATECAT_VERSION)
    
    @staticmethod
    def s_ATECAT_SIGNATURE():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_ATECAT_SIGNATURE)
    
    @staticmethod
    def s_INVALID_SLAVE_ID():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_INVALID_SLAVE_ID)
    
    @staticmethod
    def s_MASTER_SLAVE_ID():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_MASTER_SLAVE_ID)
    
    @staticmethod
    def s_MAX_NUMOF_MASTER_INSTANCES():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_MAX_NUMOF_MASTER_INSTANCES)
    
    @staticmethod
    def s_MASTER_RED_SLAVE_ID():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_MASTER_RED_SLAVE_ID)
    
    @staticmethod
    def s_EL9010_SLAVE_ID():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_EL9010_SLAVE_ID)
    
    @staticmethod
    def s_FRAMELOSS_SLAVE_ID():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_FRAMELOSS_SLAVE_ID)
    
    @staticmethod
    def s_JUNCTION_RED_FLAG():
        return CEcWrapper.Get().ecGetDefaultValue(EC_T_DEFALT_VALUE.EC_T_DEFALT_VALUE_JUNCTION_RED_FLAG)

    def __init__(self):
        self.notificationHandlers = []
        self.notificationHandlerId = 0
        self.m_bRasClient = False

        self.m_dwClientId = 0
        self.m_dwRasCookie = 0
        self.m_dwMasterInstanceId = ctypes.c_uint(0)
        self.m_eLastScanBusRes = ECError.EC_NOTFOUND
        self.m_tRunMode = EcRunMode.None_

        self.m_pRemoteApiSrvHandle = ctypes.c_void_p(None)
        self.m_pMbxGatewaySrvHandle = ctypes.c_void_p(None)
        self.m_pvRasConnectionHandle = ctypes.c_void_p(None)
        self.m_pSimulatorRemoteApiSrvHandle = ctypes.c_void_p(None)

        self.m_pvTimingEvent = None
        self.m_pEoe = ctypes.c_void_p(None)
        self.m_pTscMeasDesc = ctypes.c_void_p(None)

        self.onEcNotificationId = self.AddNotificationHandler("onMaster", self.OnHandleEcNotification)
        self.onRasNotificationId = self.AddNotificationHandler("onRas", self.OnHandleRasNotification)

        self.m_pfNativEcEvent = ctypes.cast(NativeEcEventNotif(self.ThrowEcEvent), ctypes.c_void_p)
        self.m_pfNativRasEvent = ctypes.cast(NativeRapiNotif(self.ThrowRasEvent), ctypes.c_void_p)
        self.m_pfNativTranslateEvent = ctypes.cast(NativeTranslateNotif(self.ThrowTranslateEvent), ctypes.c_void_p)
        self.m_pfNativPerfEvent = ctypes.cast(NativePerfNotif(self.ThrowPerfEvent), ctypes.c_void_p)
        self.m_pfNativDbgMsgEvent = ctypes.cast(NativeDbgMsgNotif(self.ThrowDbgMsgEvent), ctypes.c_void_p)

        self.m_cThrottleQueue = [] #List<ThrottleElem>();
        #self.IntPtr pfTranslationCallback = Marshal.GetFunctionPointerForDelegate(m_pfNativTranslateEvent);
        #self.CEcWrapper.Get().ecEnableTranslation(pfTranslationCallback);

    def AddNotificationHandler(self, name, cb):
        if name not in {"onMaster", "onRas", "onTranslate", "onPerf", "onDbgMsg", "onApp"}:
            return -1
        self.notificationHandlerId = self.notificationHandlerId + 1
        notificationHandler = {
          "id": self.notificationHandlerId,
          "name": name,
          "cb": cb,
        }
        self.notificationHandlers.append(notificationHandler)
        return self.notificationHandlerId

    def RemoveNotificationHandler(self, id_):
        for i in range(len(self.notificationHandlers)):
            if self.notificationHandlers[i]["id"] == id_:
                self.notificationHandlers.pop(i)
                return True
        return False

    def OnNotificationHandler(self, name, *args):
        for notificationHandler in self.notificationHandlers:
            if notificationHandler["name"] == name:
                notificationHandler["cb"](*args)

    def HasNotificationHandler(self, name):
        for notificationHandler in self.notificationHandlers:
            if notificationHandler["name"] == name:
                return True
        return False


    def ThrowEcEvent(self, dwCode, unmParms):
        """
        Throws the EtherCAT-Notifications. The Type of the event depends on the notification code.
        """
        try:
            EC_NOTIFY_APP = 0x00080000 # const uint
            EC_NOTIFY_APP_MAX_CODE = 0x0000FFFF # const uint
            code = DN_NotifyCode.UNDEFINED if dwCode >= EC_NOTIFY_APP and dwCode <= EC_NOTIFY_APP + EC_NOTIFY_APP_MAX_CODE else DN_NotifyCode(dwCode)
            if self.IsThrottledNotification(code):
                return 0

            unmParamType = NotificationDataType(CEcWrapperTypes.GetNotificationDataType(code)) #CEcWrapperTypes.NotificationDataType

            pbyInBuf = ctypes.c_void_p(None) # IntPtr
            dwInBufSize = ctypes.c_uint(0)
            eRes = CEcWrapper.Get().ecGetNotificationData(dwCode, unmParamType.value, ctypes.c_void_p(unmParms), ctypes.byref(pbyInBuf), ctypes.byref(dwInBufSize))
            if eRes != ECError.EC_NOERROR:
                return 0

            if dwCode >= EC_NOTIFY_APP and dwCode <= EC_NOTIFY_APP + EC_NOTIFY_APP_MAX_CODE:
                if self.HasNotificationHandler("onApp"):
                    out_inData = CEcWrapperPythonOutParam()
                    CEcWrapperTypes.ReadPdByteFromAddress(pbyInBuf, 0, dwInBufSize, out_inData)
                    inData = out_inData.value

                    out_outData = CEcWrapperPythonOutParam()

                    #// Notify application synchronously!
                    self.OnNotificationHandler("onApp", dwCode - EC_NOTIFY_APP, inData, out_outData)

                    outData = out_outData.value # byte[]
                    if outData is not None:
                        pOutData = CEcWrapperTypes.Conv_IntArrayToBytePtr(outData) # IntPtr
                        CEcWrapper.Get().ecSetNotificationData(unmParms, pOutData, len(outData))

                return 0

            obj = CEcWrapperTypes.ConvNotificationData(code, pbyInBuf) # object
            errMsgs = self.GetNotificationErrMsg(False, dwCode, unmParms)

            if self.HasNotificationHandler("onMaster"):
                notifyType = DN_NotifyType(CEcWrapper.Get().ecParseNotificationType(dwCode))
                self.OnNotificationHandler("onMaster", notifyType, code, obj, errMsgs)
        except:
            self.ReportException("ThrowEcEvent(dwCode={0})".format(DN_NotifyCode(dwCode)), DN_EC_LOG_TYPE.MASTER, sys.exc_info()[0])
        return 0


    def ThrowRasEvent(self, dwCode, unmParms):
        """
        Throws the RAS Events. The Type of the event depends on the notification code.
        """
        try:
            pbyInBuf = ctypes.c_void_p(None) # IntPtr
            dwInBufSize = ctypes.c_uint(0)
            eRes = CEcWrapper.Get().ecGetNotificationData(dwCode, NotificationDataType.Default.value, ctypes.c_void_p(unmParms), ctypes.byref(pbyInBuf), ctypes.byref(dwInBufSize))
            if eRes != ECError.EC_NOERROR:
                return 0

            code = DN_RasNotifyCode(dwCode)
            obj = CEcWrapperTypes.ConvRasNotificationData(code, pbyInBuf)
            errMsgs = self.GetNotificationErrMsg(True, dwCode, unmParms)

            notifyType = DN_NotifyType(CEcWrapper.Get().ecParseNotificationType(dwCode))

            with CEcWrapperPython.m_oInstancesLock:
                dwRasCookie = self.GetRasNotificationCookie(code, obj)
                for instance in CEcWrapperPython.m_oInstances:
                    if instance.HasNotificationHandler("onRas"):
                        if not dwRasCookie:
                            instance.OnNotificationHandler("onRas", notifyType, code, obj, errMsgs)
                            continue

                        if not self.m_dwRasCookie and code == DN_RasNotifyCode.CONNECTION:
                            self.m_dwRasCookie = dwRasCookie

                        elif self.m_dwRasCookie and self.m_dwRasCookie != dwRasCookie:
                            continue

                        instance.OnNotificationHandler("onRas", notifyType, code, obj, errMsgs)

        except:
            self.ReportException("ThrowRasEvent(dwCode={0})".format(DN_RasNotifyCode(dwCode)), DN_EC_LOG_TYPE.RASCLIENT, sys.exc_info()[0])
        return 0


    def GetRasNotificationCookie(self, code, obj):
        if obj is None:
            return 0

        if code == DN_RasNotifyCode.CONNECTION:
            return obj.dwCookie #DN_ATEMRAS_T_CONNOTIFYDESC
        if code in {DN_RasNotifyCode.CONNECTION, DN_RasNotifyCode.UNREGISTER}:
            return obj.dwCookie # DN_ATEMRAS_T_REGNOTIFYDESC
        if code == DN_RasNotifyCode.MARSHALERROR:
            return obj.dwCookie # DN_ATEMRAS_T_MARSHALERRORDESC
        if code in {DN_RasNotifyCode.NONOTIFYMEMORY, DN_RasNotifyCode.STDNOTIFYMEMORYSMALL, DN_RasNotifyCode.MBXNOTIFYMEMORYSMALL}:
            return obj.dwCookie # DN_ATEMRAS_T_NONOTIFYMEMORYDESC

        return 0

    def GetNotificationErrMsg(self, bRas, dwCode, unmParms):
        msg = [] # List<string>
        data = ctypes.c_void_p(None) #IntPtr
        eRes = ECError.EC_NOERROR
        if bRas:
            eRes = CEcWrapper.Get().ecParseRasNotificationErrMsg(self.m_dwMasterInstanceId, dwCode, ctypes.c_void_p(unmParms), ctypes.byref(data))
        else:
            eRes = CEcWrapper.Get().ecParseNotificationErrMsg(self.m_dwMasterInstanceId, dwCode, ctypes.c_void_p(unmParms), ctypes.byref(data))

        if eRes == ECError.EC_NOERROR:
            i = 0 # uint
            m = SDN_EC_STRING_HLP()
            eRes2 = self.ConvResAsError(CEcWrapper.Get().ecGetNotificationErrMsg(data, i, ctypes.byref(m)), True)
            while eRes2 == ECError.EC_NOERROR:
                msg.append(CEcWrapperTypes.Conv_StrFromCharPtr(m.Data))
                i += 1
                eRes2 = self.ConvResAsError(CEcWrapper.Get().ecGetNotificationErrMsg(data, i, ctypes.byref(m)), True)

            CEcWrapper.Get().ecFreeNotificationErrMsg(data)
        return msg

    def ThrowPerfEvent(self, pszFktName, dwTime):
        """
        Throws the performance monitoring events.
        """
        if self.HasNotificationHandler("onPerf"):
            self.OnNotificationHandler("onPerf", CEcWrapperTypes.Conv_StrFromCharPtr(pszFktName), dwTime)


    def ThrowTranslateEvent(self, _code, msg):
        """
        Throws the performance monitoring events.
        """
        if self.HasNotificationHandler("onTranslate"):
            self.OnNotificationHandler("onTranslate", CEcWrapperTypes.Conv_StrFromCharPtr(msg))


    def ThrowDbgMsgEvent(self, type_, severity, msg):
        """
        Throws the debug message events.
        """
        if self.HasNotificationHandler("onDbgMsg"):
            self.OnNotificationHandler("onDbgMsg", DN_EC_LOG_TYPE(type_), DN_EC_LOG_LEVEL(severity), CEcWrapperTypes.Conv_StrFromCharPtr(msg))


    def ReportException(self, fname, type_, e):
        if self.HasNotificationHandler("onDbgMsg"):
            self.OnNotificationHandler("onDbgMsg", type_, DN_EC_LOG_LEVEL.CRITICAL, "Exception in '{0}':\n  StackTrace: ".format(fname) + str(e))


    def GetRunMode(self):
        """
        Return run mode

        Returns:
            Run mode
        """
        return self.m_tRunMode


    def OnHandleEcNotification(self, _type_, code, data, _errMsgs):
        """
        Callback function that will be called after the scan bus has been finished.
        The scan bus result will be stored in m_eLastScanBusRes.

        Args:
            type_: Type
            code: Code
            data: Data
            errMsgs: Error messages

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        if code == DN_NotifyCode.SB_STATUS:
            self.m_eLastScanBusRes = ECError(data.dwResultCode)


    def OnHandleRasNotification(self, _type_, code, data, _errMsgs):
        """
        Callback function that will be called after the scan bus has been finished.
        The scan bus result will be stored in m_eLastScanBusRes.

        Args:
            type_: Type
            code: Code
            data: Data
            errMsgs: Error messages

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        if code == DN_RasNotifyCode.CONNECTION:
            if self.m_pvRasConnectionHandle is not None:
                if data.dwCause == ECError.EMRAS_SERVERSTOPPED:
                    self.RasClntRemoveConnection(1000)


    def RegisterClient(self, out_pRegRes):
        """
        Register a client with the EtherCAT Master

        Args:
            out_pRegRes: out Registration results, a pointer to a structure of type REGISTERRESULTS

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pRegRes.value = None
        self.m_dwClientId = 0

        pRegParams = SDN_EC_T_REGISTERPARMS(
            pCallerData=None,
            pfnNotify=self.m_pfNativEcEvent
        )

        gen_pRegRes = SDN_EC_T_REGISTERRESULTS()
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecRegisterClient2(self.m_dwMasterInstanceId, ctypes.byref(pRegParams), ctypes.byref(gen_pRegRes)))
        out_pRegRes.value = CEcWrapperTypes.Conv(gen_pRegRes)

        if gen_dwRetVal == ECError.EC_NOERROR:
            self.m_dwClientId = out_pRegRes.value.dwClntId

        return self.ReportErrorCode(gen_dwRetVal)


    def UnregisterClient(self):
        """
        Unregister a client from the EtherCAT master

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        return self.ConvResAsError(CEcWrapper.Get().ecUnregisterClient2(self.m_dwMasterInstanceId, self.m_dwClientId))


    def RasSrvStart(self, oParms):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def RasSrvStop(self, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SimulatorRasSrvStart(self, oParms):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SimulatorRasSrvStop(self, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def MbxGatewaySrvStart(self, dwMasterInstanceId, oParms):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def MbxGatewaySrvStop(self, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def RasClntAddConnection(self, oRasParms):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def RasClntRemoveConnection(self, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def RasGetConnectionInfo(self, out_pConInfo):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    @staticmethod
    def IsRemoteServerUp(abyIpAddr, wPort):
        """
        Checks if remote server is up by sending a "ping"

        Args:
            abyIpAddr: IPAddress
            wPort:     Port

        Returns:
            bool: True, if server is up, False otherwise
        """
        #// Special: For CeWin, we must skip Port 3, because they use not a "real" IP address!
        if wPort == 3:
            return True

        try:
            hostname = "{}.{}.{}.{}".format(abyIpAddr[0], abyIpAddr[1], abyIpAddr[2], abyIpAddr[3])

            if platform.system() == "Windows":
                response = os.system("ping " + hostname + " -n 1")
            else:
                response = os.system("ping -c 1 " + hostname)

            return response == 0
        except:
            return False


    def MbxGatewayClntAddConnection(self, oMbxGatewayParms):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def MbxGatewayClntRemoveConnection(self):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def MbxGatewayCoeSdoDownload(self, wAddress, wObIndex, byObSubIndex, pbyData, dwDataLen, dwTimeout, dwFlags):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def MbxGatewayCoeSdoUpload(self, wAddress, wObIndex, byObSubIndex, pbyData, dwDataLen, pdwOutDataLen, dwTimeout, dwFlags):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def EnablePerformanceMeasuring(self, bEnable):
        """
        Enables performance monitoring. For every master function, the notification "PerfNotification" will be called.

        Args:
            bEnable: True = Enables performance monitoring
        """
        pfPerfCallback = self.m_pfNativPerfEvent
        CEcWrapper.Get().ecEnablePerformanceMeasuring(pfPerfCallback if bEnable else ctypes.c_void_p(None))


    def EnableTranslation(self, bEnable):
        """
        Enables translation. For every master string, the notification "TranslateNotification" will be called.

        Args:
            bEnable: True = Enables translation
        """
        pfTranslationCallback = self.m_pfNativTranslateEvent
        CEcWrapper.Get().ecEnableTranslation(pfTranslationCallback if bEnable else ctypes.c_void_p(None))


    @classmethod
    def GetErrorText(cls, eErrorCode):
        """
        Return text tokens by Error code from master stack.

        Args:
            eErrorCode: Error code

        Returns:
            str: Error text for supplied error code
        """
        data = SDN_EC_STRING_HLP()
        eRes = ECError(CEcWrapper.Get().ecGetText2(eErrorCode.value, ctypes.byref(data)))
        if eRes == ECError.EC_NOERROR:
            return CEcWrapperTypes.Conv_StrFromCharPtr(data.Data)
        return "Unknown Error 0x{:08X}".format(eErrorCode)


    def ExecJob(self, eUserJob):
        """
        Execute or initiate the requested master job.

        Args:
            eUserJob: Requested job.

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        data = ctypes.c_uint(0)
        return self.ConvResAsError(CEcWrapper.Get().ecExecDefaultJob(self.m_dwMasterInstanceId, eUserJob.value, ctypes.byref(data)), True)


    def ExecJobProcessAllRxFrames(self, out_bPrevCycProcessed):
        """
        calls the process all rx frame job

        Args:
            bPrevCycProcessed: True: previous send frame was received and processed, False: otherwise

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        bPrevCycProcessedUnm = ctypes.c_uint(0)
        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecExecDefaultJob(self.m_dwMasterInstanceId, DN_EC_T_USER_JOB.ProcessAllRxFrames, ctypes.byref(bPrevCycProcessedUnm)), True)
        out_bPrevCycProcessed.value = bPrevCycProcessedUnm.value == 1
        return dwRetVal


    def ExecJobSendCycFramesByTaskId(self, dwTaskId):
        """
        sends a cycle frame by its task id

        Args:
            dwTaskId: task id of the cyclic frame

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        dwTaskIdUnm = ctypes.c_uint(dwTaskId)
        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecExecDefaultJob(self.m_dwMasterInstanceId, DN_EC_T_USER_JOB.SendCycFramesByTaskId, ctypes.byref(dwTaskIdUnm)), True)
        return dwRetVal


    @staticmethod
    def ConvertMasterStringFromBytes(byData, dwOffset, dwLen):
        """
        Converts a master string into UTF8 format

        Args:
            abyData: Byte array to convert
            dwOffset: Offset
            dwLen: Length

        Returns:
            str: Converted string
        """
        out_value = CEcWrapperPythonOutParam()
        eRes = CEcWrapperPython.ReadValueFromBytes(byData, dwOffset, dwLen*8, DN_EC_T_DEFTYPE.VISIBLESTRING, out_value)
        if eRes != ECError.EC_NOERROR:
            return ""
        return CEcWrapperPython.ConvertMasterString(str(out_value.value))

    @staticmethod
    def ConvertMasterString(val):
        return CEcWrapperPython.PatchString(val)

    @staticmethod
    def PatchString(str_):
        #//str->Replace("\0", String::Empty); // Doesn't work e.g. for BK1120, Coe-OD-Index 0x4000
        if not str_:
            return str_

        idx = str_.find('\0')
        if idx != -1:
            str_ = str_[0:idx]

        return str_


    def WaitForAuxClock(self):
        """
        Waits for AuxClock

        Returns:
            bool: Wait event was triggered
        """
        if self.m_pvTimingEvent is None:
            return False

        #// Wait for next cycle (event from scheduler task)
        return CEcWrapper.Get().ecOsWaitForEvent2(self.m_pvTimingEvent)


    def IsAuxClockEnabled(self):
        """
        Checks if AuxClock is enabled

        Returns:
            bool: AuxClock enabled or disabled
        """
        return self.m_pvTimingEvent is not None


    def EoeInstallEndpoint(self, bCreateTxEvent, strInterfaceName, strInterfaceGuid):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def EoeUninstallEndpoint(self):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def EoeTriggerTxEvent(self):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    @classmethod
    def ESCTypeText(cls, byEscType, bLong):
        """
        Gets the text of corresponding 	ESC type

        Args:
            byEscType: ESC type
            bLong: True: long text version, False: short text version
            strInterfaceGuid: Interface guid (optional)

        Returns:
            str: Text of corresponding ESC type
        """
        data = SDN_EC_STRING_HLP()
        eRes = cls.ConvResAsError(CEcWrapper.Get().ecESCTypeText(byEscType, bLong, ctypes.pointer(data)))
        if eRes == ECError.EC_NOERROR:
            return CEcWrapperTypes.Conv_StrFromCharPtr(data.Data)
        return ""


    @classmethod
    def SlaveVendorText(cls, dwVendorId):
        """
        Gets the text of slave vendor

        Args:
            dwVendorId: Vendor ID

        Returns:
            str: Text of slave vendor
        """
        data = SDN_EC_STRING_HLP()
        eRes = cls.ConvResAsError(CEcWrapper.Get().ecSlaveVendorText(dwVendorId, ctypes.pointer(data)))
        if eRes == ECError.EC_NOERROR:
            return CEcWrapperTypes.Conv_StrFromCharPtr(data.Data)
        return ""


    @classmethod
    def SlaveProdCodeText(cls, dwVendorId, dwProductCode):
        """
        Gets the text of slave product code

        Args:
            dwVendorId: Vendor ID
            dwProductCode: Product code

        Returns:
            str: Text of slave product code
        """
        data = SDN_EC_STRING_HLP()
        eRes = cls.ConvResAsError(CEcWrapper.Get().ecSlaveProdCodeText(dwVendorId, dwProductCode, ctypes.pointer(data)))
        if eRes == ECError.EC_NOERROR:
            return CEcWrapperTypes.Conv_StrFromCharPtr(data.Data)
        return ""


    def SetBusCnfReadProp(self, eEscSiiReg, dwTimeout):
        """
        Sets read property for bus configuration

        Args:
            eEscSiiReg: SII register
            dwTimeout: Time out of bus scan

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_eEscSiiReg = CEcWrapperTypes.Conv(eEscSiiReg, "DN_ESC_SII_REG")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        return self.ConvResAsError(CEcWrapper.Get().ecSetBusCnfReadProp(self.m_dwMasterInstanceId, gen_eEscSiiReg, gen_dwTimeout))


    def RestartScanBus(self, dwTimeout, bReadRevisionNo, bReadSerialNo):
        """
        Trigger Bus Scan

        Args:
            dwTimeout: Time out of bus scan
            bReadRevisionNo: Read revision number
            bReadSerialNo: Read serial number

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_bReadRevisionNo = CEcWrapperTypes.Conv(bReadRevisionNo, "bool")
        gen_bReadSerialNo = CEcWrapperTypes.Conv(bReadSerialNo, "bool")
        return self.ConvResAsError(CEcWrapper.Get().ecRestartScanBus(self.m_dwMasterInstanceId, gen_dwTimeout, gen_bReadRevisionNo, gen_bReadSerialNo))


    def GetBusScanSlaveInfoDesc(self, wAutoIncAddr, out_oSlaveInfoDesc):
        """
        This call will return the basic slave info determined in the last bus scan

        Args:
            wAutoIncAddr: Auto increment address of the slave
            oSlaveInfoDesc: Out parameter that contains different slave information after the call

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_oSlaveInfoDesc.value = None
        oSlaveInfoDesc = DN_EC_T_SB_SLAVEINFO_DESC()
        gen_wAutoIncAddr = CEcWrapperTypes.Conv(wAutoIncAddr, "short")
        gen_oSlaveInfoDesc = CEcWrapperTypes.Conv(oSlaveInfoDesc, "SDN_EC_T_SB_SLAVEINFO_DESC")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetBusScanSlaveInfoDesc(self.m_dwMasterInstanceId, gen_wAutoIncAddr, ctypes.byref(gen_oSlaveInfoDesc)))
        out_oSlaveInfoDesc.value = CEcWrapperTypes.Conv(gen_oSlaveInfoDesc, "DN_EC_T_SB_SLAVEINFO_DESC")
        return self.ReportErrorCode(gen_dwRetVal)


    def GetScanBusStatus(self, out_oSbStatus):
        """
        Gets the status of the last bus scan.

        Args:
            oSbStatus: The last bus scan status

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_oSbStatus.value = None
        gen_oSbStatus = SDN_EC_T_SB_STATUS_NTFY_DESC()
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetScanBusStatus(self.m_dwMasterInstanceId, ctypes.byref(gen_oSbStatus)))
        out_oSbStatus.value = CEcWrapperTypes.Conv(gen_oSbStatus)
        return self.ReportErrorCode(gen_dwRetVal)


    def CoeGetODList2(self, dwSlaveId, eListType, out_pList, dwLen, out_pdwOutLen, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeGetObjectDesc2(self, dwSlaveId, wIndex, out_oObjDesc, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeGetObjectDescReq(self, pMbxTfer, dwSlaveId, wIndex, out_oObjDesc, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeGetEntryDesc2(self, dwSlaveId, wIndex, bySubIndex, byValueInfoType, out_oEntryDesc, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeGetEntryDescReq(self, pMbxTfer, dwSlaveId, wIndex, bySubIndex, byValueInfoType, out_oEntryDesc, dwTimeout):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def MbxTferCreate(self, dwTferId, dwBufferSize, out_pMbxTfer):
        """
        Creates a mailbox transfer object

        Args:
            dwTferId: transfer ID (optional, can be 0)
            dwBufferSize: buffer size
            out_pMbxTfer: out mailbox transfer object

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint", "uint")
        gen_dwBufferSize = CEcWrapperTypes.Conv(dwBufferSize, "uint", "uint")
        pMbxTfer = None
        gen_pMbxTfer = CEcWrapperTypes.Conv(pMbxTfer, "IntPtr")
        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecMbxTferCreate2(self.m_dwMasterInstanceId, self.m_dwClientId, gen_dwTferId, gen_dwBufferSize, ctypes.pointer(gen_pMbxTfer)))
        out_pMbxTfer.value = CEcWrapperTypes.Conv(gen_pMbxTfer, "IntPtr")
        return dwRetVal


    def MbxTferWait(self, pMbxTfer):
        """
        Waits until mailbox transfer is finished

        Args:
            pMbxTfer: mailbox transfer object

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_pMbxTfer = CEcWrapperTypes.Conv(pMbxTfer, "IntPtr")
        return self.ConvResAsError(CEcWrapper.Get().ecMbxTferWait(self.m_dwMasterInstanceId, gen_pMbxTfer))


    def MbxTferCopyTo(self, pMbxTfer, abyData, dwDataLen):
        """
        Copies data to the mailbox transfer buffer

        Args:
            pMbxTfer: mailbox transfer object
            abyData: abyData
            dwDataLen: dwDataLen

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_pMbxTfer = CEcWrapperTypes.Conv(pMbxTfer, "IntPtr")
        gen_abyData = CEcWrapperTypes.Conv_IntArrayToBytePtr(abyData)
        gen_dwDataLen = CEcWrapperTypes.Conv(dwDataLen, "uint")
        return self.ConvResAsError(CEcWrapper.Get().ecMbxTferCopyTo(self.m_dwMasterInstanceId, gen_pMbxTfer, gen_abyData, gen_dwDataLen))


    def MbxTferCopyFrom(self, pMbxTfer, abyData, dwDataLen, out_pdwOutDataLen):
        """
        Copies data from the mailbox transfer buffer

        Args:
            pMbxTfer: mailbox transfer object
            abyData: abyData
            dwDataLen: dwDataLen
            out_pdwOutDataLen: pdwOutDataLen

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pdwOutDataLen.value = 0
        gen_pMbxTfer = CEcWrapperTypes.Conv(pMbxTfer, "IntPtr")
        gen_abyData = CEcWrapperTypes.Conv_IntArrayToBytePtr(abyData)
        gen_dwDataLen = CEcWrapperTypes.Conv(dwDataLen, "uint")
        gen_pdwOutDataLen = ctypes.c_uint(0)
        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecMbxTferCopyFrom(self.m_dwMasterInstanceId, gen_pMbxTfer, gen_abyData, gen_dwDataLen, ctypes.byref(gen_pdwOutDataLen)))
        out_pdwOutDataLen.value = gen_pdwOutDataLen.value
        for i in range(out_pdwOutDataLen.value):
            abyData[i] = CEcWrapperTypes.Conv_IntFromBytes(gen_abyData[i])
        return dwRetVal


    def NotifyApp(self, dwCode, pInData, wDataLen, out_pOutData, wOutLen, out_pdwOutDataLen):
        """
        Notifies the master application

        Args:
            dwCode: Code
            pInData: Input data
            wDataLen: Length of in data
            out_pOutData: Output data
            wOutLen: Length of output data field
            out_pdwOutDataLen: Length of actual out data

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_dwCode = CEcWrapperTypes.Conv(dwCode, "uint")
        gen_pInData = CEcWrapperTypes.Conv(pInData, "byte[]")
        gen_wDataLen = CEcWrapperTypes.Conv(wDataLen, "ushort")
        pOutData = [0] * wOutLen
        gen_pOutData = CEcWrapperTypes.Conv(pOutData, "byte[]")
        gen_wOutLen = CEcWrapperTypes.Conv(wOutLen, "ushort")
        gen_pdwOutDataLen = ctypes.c_uint(0)
        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecNotifyApp2(self.m_dwMasterInstanceId, gen_dwCode, gen_pInData, gen_wDataLen, gen_pOutData, gen_wOutLen, gen_pdwOutDataLen))
        out_pdwOutDataLen.value = gen_pdwOutDataLen.value
        for i in range(out_pdwOutDataLen.value):
            pOutData[i] = CEcWrapperTypes.Conv_IntFromBytes(gen_pOutData[i])
        out_pOutData.value = pOutData
        return dwRetVal


    def ReadIdentifyObj(self, wFixedAddr):
        """
        Reads the identify object of a slave

        Args:
            wFixedAddr: Fixed station address
        """
        CEcWrapper.Get().ecReadIdentifyObj(self.m_dwMasterInstanceId, wFixedAddr)


    def AddDbgMsg(self, strDbgMsg):
        """
        Adds a debug message to the print message queue

        Args:
            strDbgMsg: debug message

        Returns:
            returns True: if success; otherwise False
        """
        gen_strDbgMsg = CEcWrapperTypes.Conv(strDbgMsg, "string")
        CEcWrapper.Get().ecOsDbgMsg(gen_strDbgMsg)
        return True


    def GetSlaveInfoEx(self, oReq, out_oRes):
        """
        Gets the extended slave info determined in the last bus scan.

        Args:
            oReq: Request parameter
            out_oRes: The extended slave information structure

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        oRes = DN_EC_T_SB_SLAVEINFO_RES_DESC()
        gen_oReq = CEcWrapperTypes.Conv(oReq, "DN_EC_T_SB_SLAVEINFO_REQ_DESC") 
        gen_oRes = CEcWrapperTypes.Conv(oRes, "DN_EC_T_SB_SLAVEINFO_RES_DESC")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveInfoEx(self.m_dwMasterInstanceId, ctypes.byref(gen_oReq), ctypes.byref(gen_oRes)))
        out_oRes.value = CEcWrapperTypes.Conv(gen_oRes, "SDN_EC_T_SB_SLAVEINFO_RES_DESC")
        return self.ReportErrorCode(gen_dwRetVal)


    def ForceSlvStatCollection(self):
        """
        Sends datagrams to collect slave statistics counters.

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        return self.ConvResAsError(CEcWrapper.Get().ecForceSlvStatCollection(self.m_dwMasterInstanceId))


    def GetSlvStatistics(self, dwSlaveId, out_oStatistics):
        """
        Returns slave statistics counters.

        Args:
            dwSlaveId: Slave ID
            oStatistics: out Statistics counters

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        oStatistics = DN_EC_T_SLVSTATISTICS_DESC()
        gen_oStatistics = CEcWrapperTypes.Conv(oStatistics, "SDN_EC_T_SLVSTATISTICS_DESC")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlvStatistics(self.m_dwMasterInstanceId, dwSlaveId, ctypes.byref(gen_oStatistics)))
        out_oStatistics.value = CEcWrapperTypes.Conv(gen_oStatistics, "DN_EC_T_SLVSTATISTICS_DESC")
        return self.ReportErrorCode(gen_dwRetVal)


    def GetCyclicConfigInfo(self, out_oCyclicConfigInfo):
        """
        Returns an array of cyclic tasks.

        Args:
            out_oCyclicConfigInfo: out Array of cyclic tasks

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_oCyclicConfigInfo.value = None

        oCyclicConfigInfo = None
        eRes = ECError.EC_INVALIDPARM # ECError
        dwCycEntryIndex = 0 # uint
        while True:
            tConfigDesc = SDN_EC_T_CYC_CONFIG_DESC()

            eRes = self.ConvResAsError(CEcWrapper.Get().ecGetCyclicConfigInfo(self.m_dwMasterInstanceId, dwCycEntryIndex, ctypes.byref(tConfigDesc)), True)
            if eRes == ECError.EC_NOERROR:
                if oCyclicConfigInfo is None:
                    oCyclicConfigInfo = (DN_EC_T_CYC_CONFIG_DESC * tConfigDesc.dwNumCycEntries)()
                oCyclicConfigInfo[dwCycEntryIndex] = CEcWrapperTypes.Conv(tConfigDesc, "DN_EC_T_CYC_CONFIG_DESC")
                dwCycEntryIndex = dwCycEntryIndex + 1

            if eRes == ECError.EC_INVALIDINDEX:
                out_oCyclicConfigInfo.value = oCyclicConfigInfo
                return ECError.EC_NOERROR

            if eRes != ECError.EC_NOERROR:
                break

        return self.ReportErrorCode(eRes)


    def SetAllSlavesMustReachState(self, bAllSlavesMustReachState):
        """
        Sets flag that all slaves must reach the requested master state

        Args:
            bAllSlavesMustReachState: True: All slaves must reach the requested master state

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        return self.ConvResAsError(CEcWrapper.Get().ecSetAllSlavesMustReachState(self.m_dwMasterInstanceId, bAllSlavesMustReachState))

    def SetAdditionalVariablesForSpecificDataTypesEnabled(self, bAdditionalVariablesForSpecificDataTypes):
        return self.ConvResAsError(CEcWrapper.Get().ecSetAdditionalVariablesForSpecificDataTypesEnabled(self.m_dwMasterInstanceId, bAdditionalVariablesForSpecificDataTypes))


    def EnableNotification(self, dwClientId, tNotifyCode, bEnable):
        """
        Enables notification

        Args:
            tNotifyCode: Code of notification, which should be enabled
            bEnable: True: Enables notification

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        return self.ConvResAsError(CEcWrapper.Get().ecEnableNotification(self.m_dwMasterInstanceId, dwClientId, tNotifyCode.value, bEnable))


    def ThrottleNotification(self, tNotifyCode, dwTimeout):
        """
        Throttles notification

        Args:
            tNotifyCode: Code of notification, which should be throttled
            dwTimeout: 0 = Not throttled, > 0 = Throttle timeout in ms

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        for i in range(len(self.m_cThrottleQueue)):
            elem = self.m_cThrottleQueue[i] # ThrottleElem
            if elem.tNotifyCode == tNotifyCode:
                self.m_cThrottleQueue.pop(elem)
                break

        e = ThrottleElem()
        e.tNotifyCode = tNotifyCode
        e.nLastSeen = 0
        e.dwTimeout = dwTimeout
        self.m_cThrottleQueue.append(e)
        return ECError.EC_NOERROR


    def IsThrottledNotification(self, tNotifyCode):
        """
        Checks if notification is throttled

        Returns:
            True, if notification is throttled
        """
        for elem in self.m_cThrottleQueue:
            if elem.tNotifyCode != tNotifyCode:
                continue

            now = int((datetime.datetime.now() - CEcWrapperPython.DATE_SINCE_1970).total_seconds() * 1000) #long
            last = elem.nLastSeen # long

            if last + elem.dwTimeout > now:
                return True

            elem.nLastSeen = now
            break

        return False


    def IoControl(self, dwCode, pbyInBuf, dwInBufSize, out_pbyOutBuf, dwOutBufSize, out_pdwNumOutData):
        """
        Executes an IO control

        Args:
            dwCode: Control code
            pbyInBuf: input data buffer
            dwInBufSize: size of input data buffer in byte
            out_pbyOutBuf: output data buffer
            dwOutBufSize: size of output data buffer in byte
            out_pdwNumOutData: out number of output data bytes stored in output data buffer

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pbyOutBuf.value = [0] * dwOutBufSize
        out_pdwNumOutData.value = 0
        gen_dwCode = CEcWrapperTypes.Conv(dwCode, "uint")
        gen_pbyInBuf = CEcWrapperTypes.Conv_IntArrayToBytePtr(pbyInBuf[0])
        gen_dwInBufSize = CEcWrapperTypes.Conv(dwInBufSize, "uint")
        gen_pbyOutBuf = CEcWrapperTypes.Conv_IntArrayToBytePtr(out_pbyOutBuf.value)
        gen_dwOutBufSize = CEcWrapperTypes.Conv(dwOutBufSize, "uint")
        gen_pdwNumOutData = CEcWrapperTypes.Conv(out_pdwNumOutData.value, "uint")
        res = self.ConvResAsError(CEcWrapper.Get().ecIoControl2(self.m_dwMasterInstanceId, gen_dwCode, ctypes.byref(gen_pbyInBuf), gen_dwInBufSize, ctypes.byref(gen_pbyOutBuf), gen_dwOutBufSize, ctypes.byref(gen_pdwNumOutData)))
        out_pbyOutBuf.value = CEcWrapperTypes.Conv(gen_pbyOutBuf)
        out_pdwNumOutData.value = CEcWrapperTypes.Conv(gen_pdwNumOutData)
        return res


    def SdoUploadMasterOd(self, wObIndex, dwTimeout, out_pobjMasterOd):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    @staticmethod
    def CreateObjectFromBytes(bytes_, ref_obj):
        """
        Creates object from byte array

        Args:
            bytes_: Object data as byte array
            ref_obj: Object which should be filled

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        obj = ref_obj.value

        if not obj.__class__.__name__.startswith("DN_"):
            return ECError.EC_INVALIDPARM

        sobj = CEcWrapperTypes.Conv(obj)
        if sobj is None:
            return ECError.EC_NOTFOUND

        size = CEcWrapperTypes.GetSizeOfStructure(sobj)
        if len(bytes_) < size:
            return ECError.EC_NOMEMORY

        bytes2 = (ctypes.c_uint8 * len(bytes_))()
        for i, b in enumerate(bytes_):
            if isinstance(b, bytes):
                bytes2[i] = int.from_bytes(b, "little")
            else:
                bytes2[i] = b
        sobj2 = CEcWrapperTypes.ConvBytesToStructure(bytes2, sobj)
        if sobj2 is None:
            return ECError.EC_INVALIDPARM

        res = CEcWrapperTypes.Conv(sobj2)
        if res is None:
            return ECError.EC_NOTFOUND

        ref_obj.value = res
        return ECError.EC_NOERROR


    @staticmethod
    def GetSizeOfObject(obj, out_size):
        """
        Get byte size of object (as required from CoeSdoUpload)

        Args:
            obj: Object
            out_size: Byte size of object

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_size.value = 0

        if not obj.__class__.__name__.startswith("DN_"):
            return ECError.EC_INVALIDPARM

        sobj = CEcWrapperTypes.Conv(obj)
        if sobj is None:
            return ECError.EC_NOTFOUND

        out_size.value = CEcWrapperTypes.GetSizeOfStructure(sobj)
        return ECError.EC_NOERROR

    @staticmethod
    def GetBitLenOfDataType(type_):
        if type_ == DN_EC_T_DEFTYPE.BOOLEAN:
            return 1
        if DN_EC_T_DEFTYPE.BIT1 <= type_.value <= DN_EC_T_DEFTYPE.BIT8:
            return 8
        if DN_EC_T_DEFTYPE.BIT9 <= type_.value <= DN_EC_T_DEFTYPE.BIT16:
            return 16
        if type_ == DN_EC_T_DEFTYPE.INTEGER8:
            return 8
        if type_ == DN_EC_T_DEFTYPE.INTEGER16:
            return 16
        if type_ in {DN_EC_T_DEFTYPE.INTEGER24, DN_EC_T_DEFTYPE.INTEGER32}:
            return 32
        if type_ in {DN_EC_T_DEFTYPE.INTEGER40, DN_EC_T_DEFTYPE.INTEGER48, DN_EC_T_DEFTYPE.INTEGER56, DN_EC_T_DEFTYPE.INTEGER64}:
            return 64
        if type_ in {DN_EC_T_DEFTYPE.UNSIGNED8, DN_EC_T_DEFTYPE.BYTE, DN_EC_T_DEFTYPE.BITARR8}:
            return 8
        if type_ in {DN_EC_T_DEFTYPE.UNSIGNED16, DN_EC_T_DEFTYPE.WORD, DN_EC_T_DEFTYPE.BITARR16}:
            return 16
        if type_ in {DN_EC_T_DEFTYPE.UNSIGNED24, DN_EC_T_DEFTYPE.UNSIGNED32, DN_EC_T_DEFTYPE.DWORD, DN_EC_T_DEFTYPE.BITARR32}:
            return 32
        if type_ in {DN_EC_T_DEFTYPE.UNSIGNED40, DN_EC_T_DEFTYPE.UNSIGNED48, DN_EC_T_DEFTYPE.UNSIGNED56, DN_EC_T_DEFTYPE.UNSIGNED64}:
            return 64
        if type_ == DN_EC_T_DEFTYPE.REAL32:
            return 32
        if type_ == DN_EC_T_DEFTYPE.REAL64:
            return 64
        return SDN_EC_T_VARIANT.MaxBufferSize * 8


    @staticmethod
    def ConvValueToBytes(type_, value, out_bytes):
        """
        Converts value to bytes

        Args:
            type_: Data type
            value: Value
            out_bytes: Bytes

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_bytes.value = None

        variant = SDN_EC_T_VARIANT()
        variant.nBufferSize = (CEcWrapperPython.GetBitLenOfDataType(type_) + 7) // 8

        if type_ == DN_EC_T_DEFTYPE.BOOLEAN:
            variant.uVariant.nUnsigned8 = 1 if (str(value) == "1" or str(value).lower() == "true") else 0
        elif DN_EC_T_DEFTYPE.BIT1 <= type_.value <= DN_EC_T_DEFTYPE.BIT8:
            variant.uVariant.nUnsigned8 = int(str(value))
        elif DN_EC_T_DEFTYPE.BIT9 <= type_.value <= DN_EC_T_DEFTYPE.BIT16:
            variant.uVariant.nUnsigned16 = int(str(value))
        elif type_ == DN_EC_T_DEFTYPE.INTEGER8:
            variant.uVariant.nInteger8 = int(str(value))
        elif type_ == DN_EC_T_DEFTYPE.INTEGER16:
            variant.uVariant.nInteger16 = int(str(value))
        elif type_ in {DN_EC_T_DEFTYPE.INTEGER24, DN_EC_T_DEFTYPE.INTEGER32}:
            variant.uVariant.nInteger32 = int(str(value))
        elif type_ in {DN_EC_T_DEFTYPE.INTEGER40, DN_EC_T_DEFTYPE.INTEGER48, DN_EC_T_DEFTYPE.INTEGER56, DN_EC_T_DEFTYPE.INTEGER64}:
            variant.uVariant.nInteger64 = int(str(value))
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED8, DN_EC_T_DEFTYPE.BYTE, DN_EC_T_DEFTYPE.BITARR8}:
            variant.uVariant.nUnsigned8 = int(str(value))
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED16, DN_EC_T_DEFTYPE.WORD, DN_EC_T_DEFTYPE.BITARR16}:
            variant.uVariant.nUnsigned16 = int(str(value))
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED24, DN_EC_T_DEFTYPE.UNSIGNED32, DN_EC_T_DEFTYPE.DWORD, DN_EC_T_DEFTYPE.BITARR32}:
            variant.uVariant.nUnsigned32 = int(str(value))
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED40, DN_EC_T_DEFTYPE.UNSIGNED48, DN_EC_T_DEFTYPE.UNSIGNED56, DN_EC_T_DEFTYPE.UNSIGNED64}:
            variant.uVariant.nUnsigned64 = int(str(value))
        elif type_ == DN_EC_T_DEFTYPE.REAL32:
            variant.uVariant.nReal32 = float(str(value))
        elif type_ == DN_EC_T_DEFTYPE.REAL64:
            variant.uVariant.nReal64 = float(str(value))
        elif type_ == DN_EC_T_DEFTYPE.VISIBLESTRING:
            bytes_ = str.encode(value, 'utf-8')
            variant.SetBuffer(bytes_)
        elif type_ == DN_EC_T_DEFTYPE.UNICODESTRING:
            bytes_ = str.encode(value, 'utf-16')
            variant.SetBuffer(bytes_)
        else:
            return ECError.EC_NOTSUPPORTED

        out_bytes.value = variant.GetBuffer()
        return ECError.EC_NOERROR


    @staticmethod
    def ConvValueFromBytes(bytes_, type_, out_value):
        """
        Converts value to bytes

        Args:
            bytes_: Bytes
            type_: Data type
            out_value: Value

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_value.value = None
        value = None

        variant = SDN_EC_T_VARIANT()
        variant.nBufferSize = (CEcWrapperPython.GetBitLenOfDataType(type_) + 7) // 8
        variant.SetBuffer(bytes_)

        if type_ == DN_EC_T_DEFTYPE.BOOLEAN:
            value = variant.uVariant.nUnsigned8 == 1
        elif DN_EC_T_DEFTYPE.BIT1 <= type_.value <= DN_EC_T_DEFTYPE.BIT8:
            value = variant.uVariant.nUnsigned8
        elif DN_EC_T_DEFTYPE.BIT9 <= type_.value <= DN_EC_T_DEFTYPE.BIT16:
            value = variant.uVariant.nUnsigned16
        elif type_ == DN_EC_T_DEFTYPE.INTEGER8:
            value = variant.uVariant.nInteger8
        elif type_ == DN_EC_T_DEFTYPE.INTEGER16:
            value = variant.uVariant.nInteger16
        elif type_ in {DN_EC_T_DEFTYPE.INTEGER24, DN_EC_T_DEFTYPE.INTEGER32}:
            value = variant.uVariant.nInteger32
        elif type_ in {DN_EC_T_DEFTYPE.INTEGER40, DN_EC_T_DEFTYPE.INTEGER48, DN_EC_T_DEFTYPE.INTEGER56, DN_EC_T_DEFTYPE.INTEGER64}:
            value = variant.uVariant.nInteger64
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED8, DN_EC_T_DEFTYPE.BYTE, DN_EC_T_DEFTYPE.BITARR8}:
            value = variant.uVariant.nUnsigned8
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED16, DN_EC_T_DEFTYPE.WORD, DN_EC_T_DEFTYPE.BITARR16}:
            value = variant.uVariant.nUnsigned16
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED24, DN_EC_T_DEFTYPE.UNSIGNED32, DN_EC_T_DEFTYPE.DWORD, DN_EC_T_DEFTYPE.BITARR32}:
            value = variant.uVariant.nUnsigned32
        elif type_ in {DN_EC_T_DEFTYPE.UNSIGNED40, DN_EC_T_DEFTYPE.UNSIGNED48, DN_EC_T_DEFTYPE.UNSIGNED56, DN_EC_T_DEFTYPE.UNSIGNED64}:
            value = variant.uVariant.nUnsigned64
        elif type_ == DN_EC_T_DEFTYPE.REAL32:
            value = variant.uVariant.nReal32
        elif type_ == DN_EC_T_DEFTYPE.REAL64:
            value = variant.uVariant.nReal64
        elif type_ == DN_EC_T_DEFTYPE.VISIBLESTRING:
            bytes_ = variant.GetBuffer()
            value = CEcWrapperPython.PatchString(bytearray(bytes_).decode('utf-8'))
        elif type_ == DN_EC_T_DEFTYPE.UNICODESTRING:
            bytes_ = variant.GetBuffer()
            value = CEcWrapperPython.PatchString(bytearray(bytes_).decode('utf-16'))
        else:
            return ECError.EC_NOTSUPPORTED

        out_value.value = value
        return ECError.EC_NOERROR


    @staticmethod
    def ReadValueFromBytes(bytes_, bitOffset, bitLength, type_, out_value):
        """
        Read value from bytes

        Args:
            bytes_: Bytes
            bitOffset: Bit offset
            bitLength: Bit length
            type_: Data type
            out_value: Value

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_value.value = None

        if bitLength >= 8 and (bitOffset % 8 > 0 or bitLength % 8 > 0):
            return ECError.EC_INVALIDPARM

        bytes2 = []
        if bitLength < 8:
            out_bytes2 = CEcWrapperPythonOutParam()
            CEcWrapperTypes.ReadPdBitsFromBytes(bytes_, bitOffset, bitLength, out_bytes2)
            bytes2 = out_bytes2.value
        else:
            byteOffset = (bitOffset + 7) // 8
            byteLength = (bitLength + 7) // 8
            out_bytes2 = CEcWrapperPythonOutParam()
            CEcWrapperTypes.ReadPdByteFromBytes(bytes_, byteOffset, byteLength, out_bytes2)
            bytes2 = out_bytes2.value

        return CEcWrapperPython.ConvValueFromBytes(bytes2, type_, out_value)


    @staticmethod
    def ReadValueFromAddress(address, bitOffset, bitLength, type_, out_value):
        """
        Read value from address

        Args:
            address: Address
            bitOffset: Bit offset
            bitLength: Bit length
            type_: Data type
            out_value: Value

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_value.value = None

        if bitLength >= 8 and (bitOffset % 8 > 0 or bitLength % 8 > 0):
            return ECError.EC_INVALIDPARM
        
        bytes2 = []
        if bitLength < 8:
            out_bytes2 = CEcWrapperPythonOutParam()
            CEcWrapperTypes.ReadPdBitsFromAddress(address, bitOffset, bitLength, out_bytes2)
            bytes2 = out_bytes2.value
        else:
            byteOffset = (bitOffset + 7) // 8
            byteLength = (bitLength + 7) // 8
            out_bytes2 = CEcWrapperPythonOutParam()
            CEcWrapperTypes.ReadPdByteFromAddress(address, byteOffset, byteLength, out_bytes2)
            bytes2 = out_bytes2.value

        return CEcWrapperPython.ConvValueFromBytes(bytes2, type_, out_value)


    @staticmethod
    def WriteValueToBytes(bytes_, bitOffset, bitLength, type_, value):
        """
        Write value to bytes

        Args:
            bytes_: Bytes
            bitOffset: Bit offset
            bitLength: Bit length
            type_: Data type
            value: Value

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        if bitLength >= 8 and (bitOffset % 8 > 0 or bitLength % 8 > 0):
            return ECError.EC_INVALIDPARM

        out_bytes2 = CEcWrapperPythonOutParam()
        eRes = CEcWrapperPython.ConvValueToBytes(type_, value, out_bytes2)
        if eRes != ECError.EC_NOERROR:
            return eRes

        bytes2 = out_bytes2.value
        if bitLength < 8:
            CEcWrapperTypes.WritePdBitsToBytes(bytes_, bitOffset, bytes2, bitLength)
        else:
            byteOffset = (bitOffset + 7) // 8
            CEcWrapperTypes.WritePdByteToBytes(bytes_, byteOffset, bytes2)

        return ECError.EC_NOERROR


    @staticmethod
    def WriteValueToAddress(address, bitOffset, bitLength, type_, value):
        """
        Write value to address

        Args:
            address: Address
            bitOffset: Bit offset
            bitLength: Bit length
            type_: Data type
            value: Value

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        if bitLength >= 8 and (bitOffset % 8 > 0 or bitLength % 8 > 0):
            return ECError.EC_INVALIDPARM

        out_bytes2 = CEcWrapperPythonOutParam()
        eRes = CEcWrapperPython.ConvValueToBytes(type_, value, out_bytes2)
        if eRes != ECError.EC_NOERROR:
            return eRes

        bytes2 = out_bytes2.value
        if bitLength < 8:
            CEcWrapperTypes.WritePdBitsToAddress(address, bitOffset, bytes2, bitLength)
        else:
            byteOffset = (bitOffset + 7) // 8
            CEcWrapperTypes.WritePdByteToAddress(address, byteOffset, bytes2)

        return ECError.EC_NOERROR


    def ReadSlaveEEPRom(self, bFixedAddressing, wSlaveAddress, wEEPRomStartOffset, pwReadData, dwReadLen, out_pdwNumOutData, dwTimeout):
        """
        Read EEPRom data from slave

        Args:
            bFixedAddressing: True: use station addressing, False: use auto increment addressing
            wSlaveAddress: Slave Address, station or auto increment address depending on bFixedAddressing
            wEEPRomStartOffset: Address to start EEPRom Read from
            pwReadData: Pointer to ushort array to carry the read data
            dwReadLen: Size of the ushort array provided at pwReadData (in ushorts)
            out_pdwNumOutData: out Pointer to uint carrying actually read data (in ushorts) after completion
            dwTimeout: Timeout in milliseconds. The function will block at most for this time.
              The timeout value must not be set to EC_NOWAIT

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pdwNumOutData.value = 0
        if pwReadData is None or len(pwReadData) == 0 or len(pwReadData) < dwReadLen:
            return ECError.EC_INVALIDPARM

        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wEEPRomStartOffset = CEcWrapperTypes.Conv(wEEPRomStartOffset, "ushort")
        gen_pwReadData = CEcWrapperTypes.Conv_IntArrayToBytePtr(pwReadData)
        gen_dwReadLen = CEcWrapperTypes.Conv((dwReadLen + 1) // 2, "uint")
        gen_pdwNumOutData = CEcWrapperTypes.Conv(out_pdwNumOutData.value, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")

        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReadSlaveEEPRom(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wEEPRomStartOffset, gen_pwReadData, gen_dwReadLen, ctypes.byref(gen_pdwNumOutData), gen_dwTimeout))
        out_pdwNumOutData.value = gen_pdwNumOutData.value * 2 if gen_pdwNumOutData.value * 2 < dwReadLen else dwReadLen
        for i in range(out_pdwNumOutData.value):
            pwReadData[i] = CEcWrapperTypes.Conv_IntFromBytes(gen_pwReadData[i])
        return dwRetVal


    def WriteSlaveEEPRom(self, bFixedAddressing, wSlaveAddress, wEEPRomStartOffset, pwWriteData, dwWriteLen, dwTimeout):
        """
        Write EEPRom data from slave

        Args:
            bFixedAddressing: True: use station addressing, False: use auto increment addressing
            wSlaveAddress: Slave Address, station or auto increment address depending on bFixedAddressing
            wEEPRomStartOffset: Address to start EEPRom Read from
            pwWriteData: Pointer to WORD array carrying the write data.
            dwWriteLen: Sizeof Write Data WORD array (in WORDS)
            dwTimeout: Timeout in milliseconds. The function will block at most for this time.
              The timeout value must not be set to EC_NOWAIT

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        if pwWriteData is None or len(pwWriteData) == 0:
            return ECError.EC_INVALIDPARM

        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wEEPRomStartOffset = CEcWrapperTypes.Conv(wEEPRomStartOffset, "ushort")
        gen_pwWriteData = CEcWrapperTypes.Conv_IntArrayToBytePtr(pwWriteData)
        gen_dwWriteLen = CEcWrapperTypes.Conv((dwWriteLen + 1) // 2, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecWriteSlaveEEPRom(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wEEPRomStartOffset, gen_pwWriteData, gen_dwWriteLen, gen_dwTimeout))
        return dwRetVal


    def GetSlaveInpVarInfo(self, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, out_pSlaveProcVarInfoEntries, out_pwReadEntries):
        """
        Gets the number of input variables of a specific slave. This function mainly will be used in connection with emGetSlaveInpVarInfo.

        Args:
            bFixedAddressing: True: use station addressing, False: use auto increment addressing
            wSlaveAddress: Slave Address, station or auto increment address depending on bFixedAddressing
            wNumOfVarsToRead: Number of found process variables
            out_pSlaveProcVarInfoEntries: out Entries read
            out_pwReadEntries: out Number of entries read

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pSlaveProcVarInfoEntries.value = None
        out_pwReadEntries.value = 0

        wReadEntries = ctypes.c_ushort(0)
        oSlaveProcVarInfoEntries = (SDN_EC_T_PROCESS_VAR_INFO * wNumOfVarsToRead)()

        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveInpVarInfo(self.m_dwMasterInstanceId, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, ctypes.pointer(oSlaveProcVarInfoEntries), ctypes.byref(wReadEntries)))
        if dwRetVal == ECError.EC_NOERROR:
            pSlaveProcVarInfoEntries = [CEcWrapperTypes.Conv(oSlaveProcVarInfoEntries[i]) for i in range(wReadEntries.value)]

            out_pSlaveProcVarInfoEntries.value = pSlaveProcVarInfoEntries
            out_pwReadEntries.value = wReadEntries.value

        return dwRetVal


    def GetSlaveOutpVarInfo(self, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, out_pSlaveProcVarInfoEntries, out_pwReadEntries):
        """
        Gets the number of output variables of a specific slave. This function mainly will be used in connection with emGetSlaveOutpVarInfo.

        Args:
            bFixedAddressing: True: use station addressing, False: use auto increment addressing
            wSlaveAddress: Slave Address, station or auto increment address depending on bFixedAddressing
            wNumOfVarsToRead: Number of found process variables
            out_pSlaveProcVarInfoEntries: out Entries read
            out_pwReadEntries: out Number of entries read

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pSlaveProcVarInfoEntries.value = None
        out_pwReadEntries.value = 0

        wReadEntries = ctypes.c_ushort(0)
        oSlaveProcVarInfoEntries = (SDN_EC_T_PROCESS_VAR_INFO * wNumOfVarsToRead)()

        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveOutpVarInfo(self.m_dwMasterInstanceId, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, ctypes.pointer(oSlaveProcVarInfoEntries), ctypes.byref(wReadEntries)))
        if dwRetVal == ECError.EC_NOERROR:
            pSlaveProcVarInfoEntries = [CEcWrapperTypes.Conv(oSlaveProcVarInfoEntries[i]) for i in range(wReadEntries.value)]

            out_pSlaveProcVarInfoEntries.value = pSlaveProcVarInfoEntries
            out_pwReadEntries.value = wReadEntries.value

        return dwRetVal


    def GetSlaveInpVarInfoEx(self, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, out_pSlaveProcVarInfoEntries, out_pwReadEntries):
        """
        Gets the number of input variables of a specific slave. This function mainly will be used in connection with emGetSlaveInpVarInfo.

        Args:
            bFixedAddressing: True: use station addressing, False: use auto increment addressing
            wSlaveAddress: Slave Address, station or auto increment address depending on bFixedAddressing
            wNumOfVarsToRead: Number of found process variables
            out_pSlaveProcVarInfoEntries: out Entries read
            out_pwReadEntries: out Number of entries read

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pSlaveProcVarInfoEntries.value = None
        out_pwReadEntries.value = 0

        wReadEntries = ctypes.c_uint(0)
        oSlaveProcVarInfoEntries = (SDN_EC_T_PROCESS_VAR_INFO_EX * wNumOfVarsToRead)()

        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveInpVarInfoEx(self.m_dwMasterInstanceId, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, ctypes.pointer(oSlaveProcVarInfoEntries), ctypes.byref(wReadEntries)))
        if dwRetVal == ECError.EC_NOERROR:
            pSlaveProcVarInfoEntries = [CEcWrapperTypes.Conv(oSlaveProcVarInfoEntries[i]) for i in range(wReadEntries.value)]

            out_pSlaveProcVarInfoEntries.value = pSlaveProcVarInfoEntries
            out_pwReadEntries.value = wReadEntries.value

        return dwRetVal


    def GetSlaveOutpVarInfoEx(self, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, out_pSlaveProcVarInfoEntries, out_pwReadEntries):
        """
        Gets the number of output variables of a specific slave. This function mainly will be used in connection with emGetSlaveOutpVarInfo.

        Args:
            bFixedAddressing: True: use station addressing, False: use auto increment addressing
            wSlaveAddress: Slave Address, station or auto increment address depending on bFixedAddressing
            wNumOfVarsToRead: Number of found process variables
            out_pSlaveProcVarInfoEntries: out Entries read
            out_pwReadEntries: out Number of entries read

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        out_pSlaveProcVarInfoEntries.value = None
        out_pwReadEntries.value = 0

        wReadEntries = ctypes.c_ushort(0)
        oSlaveProcVarInfoEntries = (SDN_EC_T_PROCESS_VAR_INFO_EX * wNumOfVarsToRead)()

        dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveOutpVarInfoEx(self.m_dwMasterInstanceId, bFixedAddress, wSlaveAddress, wNumOfVarsToRead, ctypes.pointer(oSlaveProcVarInfoEntries), ctypes.byref(wReadEntries)))
        if dwRetVal == ECError.EC_NOERROR:
            pSlaveProcVarInfoEntries = [CEcWrapperTypes.Conv(oSlaveProcVarInfoEntries[i]) for i in range(wReadEntries.value)]

            out_pSlaveProcVarInfoEntries.value = pSlaveProcVarInfoEntries
            out_pwReadEntries.value = wReadEntries.value

        return dwRetVal

    @classmethod
    def GetInstallDir(cls):
        if cls.m_szInstallDir == "":
            cls.m_szInstallDir = os.path.dirname(__file__) + os.path.sep
            pathEntries = os.environ["PATH"].split(os.pathsep)
            for pathEntry in pathEntries:
                pathEntry = pathEntry.rstrip(os.path.sep) + os.path.sep
                libPath = pathEntry + CEcWrapper.GetEcWrapperName()
                if os.path.isfile(libPath):
                    cls.m_szInstallDir = pathEntry
                    break
        return cls.m_szInstallDir

    @classmethod
    def SetInstallDir(cls, path):
        cls.m_szInstallDir = path
        return True


    def InitInstance(self, oParms):
        """
        Initializes EtherCAT wrapper

        Args:
            oParms: Parameters

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        with CEcWrapperPython.m_oInstancesLock:
            CEcWrapperPython.m_oInstances.append(self)

        eRetVal = self.ReportErrorCode(self.InitInstanceInt(oParms))
        if eRetVal != ECError.EC_NOERROR:
            with CEcWrapperPython.m_oInstancesLock:
                CEcWrapperPython.m_oInstances.remove(self)

        return self.ReportErrorCode(eRetVal)

    def InitInstanceInt(self, oParms):
        installDir = CEcWrapperPython.GetInstallDir()
        CEcWrapper.ecSetInstallDir(installDir)

        apiVer = CEcWrapper.Get().ecGetApiVer()
        if CEcWrapperPython.ECWRAPPER_API_VERSION != apiVer:
            return ECError.EC_INVALIDPARM

        # Necessary, because without EcMaster is not able to find link layer
        os.environ["PATH"] += os.pathsep + installDir

        if self.m_tRunMode != EcRunMode.None_:
            self.DeinitInstance()

        dwMasterInstanceId = 0
        oInitMaster = None #DN_EC_T_INIT_MASTER_PARMS
        oRasParmsClient = None #DN_EC_T_INITRASPARAMS
        oMasterRasParmsServer = None #DN_EC_T_INITRASPARAMS
        oSimulatorRasParmsServer = None #DN_EC_T_INITRASPARAMS
        oMbxGatewayParmsClient = None #DN_EC_T_INIT_MBXGATEWAY_PARMS
        oMbxGatewayParmsServer = None #DN_EC_T_INIT_MBXGATEWAY_PARMS
        bUseAuxClock = False
        bSimulator = False
        oSimulatorParams = None #DN_EC_T_SIMULATOR_INIT_PARMS

        if isinstance(oParms, DN_EC_T_INIT_PARMS_MASTER):
            dwMasterInstanceId = oParms.dwMasterInstanceId
            oInitMaster = oParms.oMaster
            bUseAuxClock = oParms.bUseAuxClock

        if isinstance(oParms, DN_EC_T_INIT_PARMS_MASTER_RAS_SERVER):
            oMasterRasParmsServer = oParms.oRas

        if isinstance(oParms, DN_EC_T_INIT_PARMS_RAS_CLIENT):
            dwMasterInstanceId = oParms.dwMasterInstanceId
            oRasParmsClient = oParms.oRas

        if isinstance(oParms, DN_EC_T_INIT_PARMS_MBXGATEWAY_CLIENT):
            oMbxGatewayParmsClient = oParms.oMbxGateway

        if isinstance(oParms, DN_EC_T_INIT_PARMS_MBXGATEWAY_SERVER):
            dwMasterInstanceId = oParms.dwMasterInstanceId
            oMbxGatewayParmsServer = oParms.oMbxGateway

        if isinstance(oParms, DN_EC_T_INIT_PARMS_SIMULATOR):
            bSimulator = True
            dwMasterInstanceId = oParms.dwSimulatorInstanceId
            oSimulatorParams = oParms.oSimulator

        if isinstance(oParms, DN_EC_T_INIT_PARMS_SIMULATOR_RAS_SERVER):
            oSimulatorRasParmsServer = oParms.oRas

        if bSimulator:
            dwInternalID = ctypes.c_uint(0)
            eErrCode = self.ConvResAsError(CEcWrapper.Get().ecSimulatorInit(dwMasterInstanceId, ctypes.byref(dwInternalID)))
            if eErrCode != ECError.EC_NOERROR:
                return eErrCode

            if oSimulatorParams is not None:
                gen_oSimulatorParams = CEcWrapperTypes.Conv(oSimulatorParams)
                gen_oSimulatorParams.pfLogMsgCallBack = self.m_pfNativDbgMsgEvent
                eErrCode = self.ConvResAsError(CEcWrapper.Get().ecInitSimulator(dwInternalID, ctypes.byref(gen_oSimulatorParams)))
                if eErrCode != ECError.EC_NOERROR:
                    self.ConvResAsError(CEcWrapper.Get().ecSimulatorDeinit(dwInternalID))
                    return eErrCode

                self.m_tRunMode = EcRunMode.SimulatorHil
            else:
                self.m_tRunMode = EcRunMode.SimulatorSil

            self.m_dwMasterInstanceId = dwInternalID
            return ECError.EC_NOERROR

        if oMasterRasParmsServer is not None:
            self.m_tRunMode = EcRunMode.RasServer
            return self.RasSrvStart(oMasterRasParmsServer)

        if oSimulatorRasParmsServer is not None:
            self.m_tRunMode = EcRunMode.SimulatorRasServer
            return self.SimulatorRasSrvStart(oSimulatorRasParmsServer)

        if oMbxGatewayParmsServer is not None:
            self.m_tRunMode = EcRunMode.MbxGatewaySrv
            return self.MbxGatewaySrvStart(dwMasterInstanceId, oMbxGatewayParmsServer)

        if oInitMaster is not None:
            self.m_tRunMode = EcRunMode.Master

            dwInternalID = ctypes.c_uint(0)
            self.m_dwMasterInstanceId = dwMasterInstanceId
            eRetVal = self.ConvResAsError(CEcWrapper.Get().ecInit(self.m_dwMasterInstanceId, False, ctypes.byref(dwInternalID)))
            if eRetVal != ECError.EC_NOERROR:
                return eRetVal

            self.m_dwMasterInstanceId = dwInternalID

            if bUseAuxClock:
                dwCpuIndex = 0
                dwBusCycleTimeUsec = oInitMaster.dwBusCycleTimeUsec
                if dwBusCycleTimeUsec < 10:
                    dwBusCycleTimeUsec = 10

                #// Create timing event to trigger the job task
                self.m_pvTimingEvent = CEcWrapper.Get().ecOsCreateEvent()
                if self.m_pvTimingEvent is None:
                    CEcWrapper.Get().ecOsDbgMsg("ERROR: insufficient memory to create timing event!\n")
                    CEcWrapper.Get().ecDone(self.m_dwMasterInstanceId)
                    return ECError.EC_NOMEMORY

                eErrCode = self.ConvResAsError(CEcWrapper.Get().ecOsAuxClkInit(dwCpuIndex, 1000000 / dwBusCycleTimeUsec, self.m_pvTimingEvent))
                if ECError.EC_NOERROR != eErrCode:
                    CEcWrapper.Get().ecOsDbgMsg("ERROR at auxiliary clock initialization!\n")
                    CEcWrapper.Get().ecDone(self.m_dwMasterInstanceId)
                    return eErrCode

            gen_oInitMaster = CEcWrapperTypes.Conv(oInitMaster)
            gen_oInitMaster.pfLogMsgCallBack = self.m_pfNativDbgMsgEvent
            eRetVal = self.ConvResAsError(CEcWrapper.Get().ecInitMaster2(self.m_dwMasterInstanceId, ctypes.byref(gen_oInitMaster)))

            return eRetVal

        if oRasParmsClient is not None:
            self.m_tRunMode = EcRunMode.RasClient
            self.m_dwMasterInstanceId = dwMasterInstanceId

            #// Initialize the native Remote API
            CEcWrapperPython.m_dwRasConnectionCounter = CEcWrapperPython.m_dwRasConnectionCounter + 1
            if CEcWrapperPython.m_dwRasConnectionCounter == 1:
                umClntParms = SDN_ATEMRAS_T_CLNTPARMS(
                    dwKeepAliveTrigger=100,
                    dwAdmPrio=1,
                    dwAdmStackSize=0x1000,
                    pvNotifCtxt=None,
                    pfNotification=self.m_pfNativRasEvent,
                    dwLogLevel=oRasParmsClient.dwLogLevel.value,
                    pfLogMsgCallBack=self.m_pfNativDbgMsgEvent
                )

                eRetVal2 = self.ConvResAsError(CEcWrapper.Get().ecRasClntInit(umClntParms, False))
                if eRetVal2 != ECError.EC_NOERROR:
                    return eRetVal2

            dwInternalID = ctypes.c_uint(0)
            self.m_dwMasterInstanceId = dwMasterInstanceId
            eRetVal = self.ConvResAsError(CEcWrapper.Get().ecInit(self.m_dwMasterInstanceId, True, ctypes.byref(dwInternalID)))
            if eRetVal != ECError.EC_NOERROR:
                return eRetVal

            self.m_dwMasterInstanceId = dwInternalID

            #/* Establish a RAS connection to the remote EtherCAT master */
            return self.RasClntAddConnection(oRasParmsClient)

        if oMbxGatewayParmsClient is not None:
            self.m_tRunMode = EcRunMode.MbxGateway
            self.m_dwMasterInstanceId = dwMasterInstanceId

            #// Initialize the mailbox gateway Remote API
            CEcWrapperPython.m_dwMbxGatewayConnectionCounter = CEcWrapperPython.m_dwMbxGatewayConnectionCounter + 1
            if CEcWrapperPython.m_dwMbxGatewayConnectionCounter == 1:
                umClntParms = SDN_EC_T_MBX_GATEWAY_CLNT_PARMS(
                    dwLogLevel=oMbxGatewayParmsClient.dwLogLevel.value,
                    pfLogMsgCallBack=self.m_pfNativDbgMsgEvent
                )

                eRetVal2 = self.ConvResAsError(CEcWrapper.Get().ecMbxGatewayClntInit(umClntParms))
                if eRetVal2 != ECError.EC_NOERROR:
                    return eRetVal2

            dwInternalID = ctypes.c_uint(0)
            self.m_dwMasterInstanceId = dwMasterInstanceId
            eRetVal = self.ConvResAsError(CEcWrapper.Get().ecInit2(self.m_dwMasterInstanceId, False, True, ctypes.byref(dwInternalID)))
            if eRetVal != ECError.EC_NOERROR:
                return eRetVal

            self.m_dwMasterInstanceId = dwInternalID

            #/* Establish a mailbox gateway connection */
            return self.MbxGatewayClntAddConnection(oMbxGatewayParmsClient)

        return ECError.EC_INVALIDPARM


    def DeinitInstance(self):
        """
        Deinitialize EtherCAT wrapper

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        eRetVal = ECError.EC_NOERROR

        if self.m_tRunMode == EcRunMode.RasClient:
            #// RasClient

            #/* remove the ras client connection */
            eRetVal = self.RasClntRemoveConnection(2000)
            if eRetVal != ECError.EC_NOERROR:
                return self.ReportErrorCode(eRetVal)

            if CEcWrapperPython.m_dwRasConnectionCounter > 0:
                CEcWrapperPython.m_dwRasConnectionCounter = CEcWrapperPython.m_dwRasConnectionCounter - 1

                if CEcWrapperPython.m_dwRasConnectionCounter == 0:
                    CEcWrapper.Get().ecRasClntClose(2000)

        if self.m_tRunMode == EcRunMode.MbxGateway:
            #// MbxGateway

            #/* remove the mailbox gateway client connection */
            eRetVal = self.MbxGatewayClntRemoveConnection()
            if eRetVal != ECError.EC_NOERROR:
                return self.ReportErrorCode(eRetVal)

            if CEcWrapperPython.m_dwMbxGatewayConnectionCounter > 0:
                CEcWrapperPython.m_dwMbxGatewayConnectionCounter = CEcWrapperPython.m_dwMbxGatewayConnectionCounter - 1

                if CEcWrapperPython.m_dwMbxGatewayConnectionCounter == 0:
                    CEcWrapper.Get().ecMbxGatewayClntDeinit(2000)

        if self.m_tRunMode == EcRunMode.MbxGatewaySrv:
            #// MbxGateway Server
            eRetVal = self.MbxGatewaySrvStop(3000)
            if eRetVal != ECError.EC_NOERROR:
                return self.ReportErrorCode(eRetVal)

        if self.m_tRunMode == EcRunMode.Master:
            #// Local
            eRetVal = self.ConvResAsError(
                CEcWrapper.Get().ecDeinitMaster(self.m_dwMasterInstanceId))

            if self.m_pvTimingEvent is not None:
                CEcWrapper.Get().ecOsAuxClkDeinit()

                CEcWrapper.Get().ecOsDeleteEvent(self.m_pvTimingEvent)
                self.m_pvTimingEvent = None

        if self.m_tRunMode == EcRunMode.SimulatorSil or self.m_tRunMode == EcRunMode.SimulatorHil:
            #// Simulator

            if self.m_tRunMode == EcRunMode.SimulatorHil:
                eRetVal = self.ConvResAsError(
                    CEcWrapper.Get().ecDeinitSimulator(self.m_dwMasterInstanceId))
                if eRetVal != ECError.EC_NOERROR:
                    return self.ReportErrorCode(eRetVal)

            eRetVal = self.ConvResAsError(
                CEcWrapper.Get().ecSimulatorDeinit(self.m_dwMasterInstanceId))
            if eRetVal != ECError.EC_NOERROR:
                return self.ReportErrorCode(eRetVal)

        if self.m_tRunMode == EcRunMode.RasServer:
            #// RasServer
            eRetVal = self.RasSrvStop(3000)
            if eRetVal != ECError.EC_NOERROR:
                return self.ReportErrorCode(eRetVal)

        if self.m_tRunMode == EcRunMode.SimulatorRasServer:
            #// SimulatorRasServer
            eRetVal = self.SimulatorRasSrvStop(3000)
            if eRetVal != ECError.EC_NOERROR:
                return self.ReportErrorCode(eRetVal)

        CEcWrapper.Get().ecDone(self.m_dwMasterInstanceId)

        with CEcWrapperPython.m_oInstancesLock:
            CEcWrapperPython.m_oInstances.remove(self)

        self.m_tRunMode = EcRunMode.None_

        #//delete this
        return self.ReportErrorCode(eRetVal)


    @classmethod
    def ConvResAsError(cls, obj, skipThrow = False):
        return cls.ReportErrorCode(ECError(obj), skipThrow)


    @classmethod
    def ReportErrorCode(cls, eErrCode, skipThrow = False):
        if cls.EnableExceptionHandling and eErrCode != ECError.EC_NOERROR and skipThrow == False:
            text = cls.GetErrorText(eErrCode)
            raise CEcWrapperPythonException(eErrCode, text, cls.FormatExceptionMessage(eErrCode, text))
        return eErrCode


    @classmethod
    def FormatExceptionMessage(cls, eErrCode, text):
        frame = inspect.stack()[2][0]
        if frame.f_code.co_name == "ConvResAsError":
            frame = inspect.stack()[3][0]
        func = frame.f_code.co_name
        args, _, _, values = inspect.getargvalues(frame)

        errMsg = "{} (0x{:08X})".format(text, eErrCode)
        if func == "InitInstance" and text == "Unknown Error 0x9811000B":
            apiVer = CEcWrapper.Get().ecGetApiVer()
            return "Python wrapper and native wrapper are incompatible ({} != {}).".format(CEcWrapperPython.ECWRAPPER_API_VERSION, apiVer)
        if func == "SetMasterState":
            return "Cannot set master state to {}: {}.".format(str(values["eReqState"]), errMsg)
        if func == "RegisterClient":
            return "Cannot register client: {}.".format(errMsg)
        if func == "ConfigureMaster":
            return "Cannot configure EtherCAT-Master: {}.".format(errMsg)
        if func == "ConfigureNetwork":
            return "Cannot configure EtherCAT-Simulator: {}.".format(errMsg)

        return "{} failed: {}.".format(func, errMsg)


    def PerfMeasInit(self, dwlFreqSet, dwNumMeas):
        """
        Initialize performance measurement

        Args:
            dwlFreqSet: TSC frequency, 0: auto-calibrate
            dwNumMeas: Number of elements to be allocated in in pTscMeasDesc->aTscTime
        """
        if self.m_pTscMeasDesc != ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasInit(ctypes.byref(self.m_pTscMeasDesc), dwlFreqSet, dwNumMeas)


    def PerfMeasDeinit(self):
        """
        Deinitialize performance measurement
        """
        if self.m_pTscMeasDesc != ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasDeinit(self.m_pTscMeasDesc)
        self.m_pTscMeasDesc = ctypes.c_void_p(None)


    def PerfMeasEnable(self):
        """
        Enable performance measurement
        """
        if self.m_pTscMeasDesc == ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasEnable(self.m_pTscMeasDesc)


    def PerfMeasStart(self, dwIndex):
        """
        Start measurement

        Args:
            dwIndex: Measurement index, 0xFFFFFFFF: all indexes
        """
        if self.m_pTscMeasDesc == ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasStart(self.m_pTscMeasDesc, dwIndex)


    def PerfMeasEnd(self, dwIndex):
        """
        End measurement

        Args:
            dwIndex: Measurement index, 0xFFFFFFFF: all indexes
        """
        if self.m_pTscMeasDesc == ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasEnd(self.m_pTscMeasDesc, dwIndex)


    def PerfMeasReset(self, dwIndex):
        """
        Reset measurement

        Args:
            dwIndex: Measurement index, 0xFFFFFFFF: all indexes
        """
        if self.m_pTscMeasDesc == ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasReset(self.m_pTscMeasDesc, dwIndex)


    def PerfMeasDisable(self):
        """
        Disable performance measurement
        """
        if self.m_pTscMeasDesc == ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasDisable(self.m_pTscMeasDesc)


    def PerfMeasShow(self, dwIndex, aszMeasCaption):
        """
        Show measurement results

        Args:
            dwIndex: Measurement index, 0xFFFFFFFF: all indexes
            aszMeasCaption: Measurement caption
        """
        if self.m_pTscMeasDesc == ctypes.c_void_p(None): return
        gen_aszMeasCaption = CEcWrapperTypes.Conv(aszMeasCaption, "string")
        CEcWrapper.Get().ecPerfMeasShow(self.m_pTscMeasDesc, dwIndex, gen_aszMeasCaption)


    def PerfMeasSetIrqCtlEnabled(self, bEnabled):
        """
        PerfMeasSetIrqCtlEnabled

        Args:
            bEnabled: True, to enable
        """
        if self.m_pTscMeasDesc == ctypes.c_void_p(None): return
        CEcWrapper.Get().ecPerfMeasSetIrqCtlEnabled(bEnabled)
        

    def ConnectPorts(self, wCfgFixedAddress1, byPort1, wCfgFixedAddress2, byPort2):
        """
        Connect a slave ESC port to another slave ESC port or to a network adapter.

        Args:
            wCfgFixedAddress1:
            byPort1:
            wCfgFixedAddress2:
            byPort2:

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_wCfgFixedAddress1 =  CEcWrapperTypes.Conv(wCfgFixedAddress1, "ushort")
        gen_byPort1 =  CEcWrapperTypes.Conv(byPort1, "byte")
        gen_wCfgFixedAddress2 =  CEcWrapperTypes.Conv(wCfgFixedAddress2, "ushort")
        gen_byPort2 = CEcWrapperTypes.Conv(byPort2, "byte")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConnectPorts(self.m_dwMasterInstanceId, gen_wCfgFixedAddress1, gen_byPort1, gen_wCfgFixedAddress2, gen_byPort2))
        return self.ReportErrorCode(gen_dwRetVal)


    def DisconnectPort(self, wCfgFixedAddress, byPort):
        """
        Disconnect a slave ESC port or a network adapter.

        Args:
            wCfgFixedAddress:
            byPort:

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        gen_wCfgFixedAddress = CEcWrapperTypes.Conv(wCfgFixedAddress, "ushort")
        gen_byPort = CEcWrapperTypes.Conv(byPort, "byte")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDisconnectPort(self.m_dwMasterInstanceId, gen_wCfgFixedAddress, gen_byPort))
        return self.ReportErrorCode(gen_dwRetVal)


    def PowerSlave(self, wCfgFixedAddress, bOn):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def DeleteSlaveCoeObject(self, wCfgFixedAddress, wIndex):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def ClearSlaveCoeObjectDictionary(self, wCfgFixedAddress):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def ResetSlaveCoeObjectDictionary(self, wCfgFixedAddress):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def ConfigureNetwork(self, eCnfType, pbyCnfData, dwCnfDataLen):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SetErrorAtSlavePort(self, wCfgFixedAddress, byPort, bOutgoing):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SetErrorGenerationAtSlavePort(self, wCfgFixedAddress, byPort, bOutgoing, dwLikelihoodPpm, dwFixedGoodFramesCnt, dwFixedErroneousFramesCnt):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def ResetErrorGenerationAtSlavePorts(self, wCfgFixedAddress):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SetLinkDownAtSlavePort(self, wCfgFixedAddress, byPort, bDown, dwLinkDownTimeMs):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SetLinkDownGenerationAtSlavePort(self, wCfgFixedAddress, byPort, dwLikelihoodPpm, dwFixedLinkDownTimeMs, dwFixedLinkUpTimeMs):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def ResetLinkDownGenerationAtSlavePorts(self, wCfgFixedAddress):
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SetMasterParms(self, pParms): # ret: ECError
        """
        Change Master Init Parameters.
        
        \note Currently OS parms, Main Link parms, Red Link parms, dwMaxBusSlaves, dwMaxAcycFramesQueued, dwAdditionalEoEEndpoints, bVLANEnable, wVLANId, byVLANPrio cannot be changed.

        Args:
            pParms: New Master parameters

        Returns:
            - EC_E_NOERROR on success
            - EC_E_INVALIDSTATE if master isn't initialized
            - EC_E_INVALIDPARM if buffer pParms is too small
        """
        gen_pParms = CEcWrapperTypes.Conv(pParms, "EC_T_INIT_MASTER_PARMS")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetMasterParms(self.m_dwMasterInstanceId, gen_pParms))
        return gen_dwRetVal

    def SetMasterRedStateReq(self, bActive): # ret: ECError
        """
        Requests Master Redundancy State ACTIVE / INACTIVE.

        Args:
            bActive: 

        Returns:
            - EC_E_NOERROR or error code
            - EC_E_INVALIDSTATE if MasterRedParms.bEnabled = EC_FALSE or Master not initialized
            - EC_E_NOTSUPPORTED if EC-Master stack does not include Master Redundancy support
        """
        gen_bActive = CEcWrapperTypes.Conv(bActive, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetMasterRedStateReq(self.m_dwMasterInstanceId, gen_bActive))
        return gen_dwRetVal

    def GetMasterRedState(self, pbActive): # ret: ECError
        """
        Gets Master Redundancy State (ACTIVE / INACTIVE).

        Args:
            pbActive: Pointer to variable of type EC_T_BOOL. Contains Master Redundancy State on success.

        Returns:
            - EC_E_NOERROR or error code
            - EC_E_INVALIDSTATE if MasterRedParms.bEnabled = EC_FALSE or Master not initialized
            - EC_E_NOTSUPPORTED if EC-Master stack does not include Master Redundancy support
        """
        gen_pbActive = CEcWrapperTypes.Conv(pbActive, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetMasterRedState(self.m_dwMasterInstanceId, ctypes.pointer(gen_pbActive)))
        return gen_dwRetVal

    def GetMasterRedProcessImageInputPtr(self): # ret: byte[]
        """
        Gets the Master Redundancy process data input image pointer

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetMasterRedProcessImageInputPtr(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def GetMasterRedProcessImageOutputPtr(self): # ret: byte[]
        """
        Gets the Master Redundancy process data output image pointer

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetMasterRedProcessImageOutputPtr(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def ScanBus(self, dwTimeout): # ret: ECError
        """
        Scans all connected slaves.
        
        \note Does not close ports. This function should not be called from within the JobTask's context.

        Args:
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecScanBus(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def RescueScan(self, dwTimeout): # ret: ECError
        """
        Scans all connected slaves. Closes and open ports on the network to rule out slaves which permanently discard frames.
        The Master notifies every slave port which permanently discard frames with EC_NOTIFY_FRAMELOSS_AFTER_SLAVE.
        
        \note  Due to port opening and closing the scanning time is increased about 2 seconds per slave.
        The Master will not automatically re-open this port. The application can force to open the port again.
        This function may not be called from within the JobTask's context.

        Args:
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecRescueScan(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def GetMasterInfo(self, pMasterInfo): # ret: ECError
        """
        Get generic information on the Master Instance.

        Args:
            pMasterInfo: 

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pMasterInfo = CEcWrapperTypes.Conv(pMasterInfo, "EC_T_MASTER_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetMasterInfo(self.m_dwMasterInstanceId, gen_pMasterInfo))
        return gen_dwRetVal

    def ConfigureMaster(self, eCnfType, pbyCnfData, dwCnfDataLen): # ret: ECError
        """
        Configure the Master.
        
        \note This function must be called after the master has been initialized. Among others the EtherCAT topology defined in the given XML configuration file will be stored internally.
        Analyzing the network including Mailbox communication like CoE can be done without given ENI file using eCnfType_GenPreopENI, this is mainly used for configuration tools to get information about the slaves in order to create the ENI file.
        
        \remark A client must not be registered prior to calling this function. In such a case the client registration will be lost.

        Args:
            eCnfType: Enum type of configuration data provided
            pbyCnfData: Filename / configuration data, or EC_NULL if eCnfType is eCnfType_GenPreopENI
            dwCnfDataLen: Length of configuration data in byte, or zero if eCnfType is eCnfType_GenPreopENI

        Returns:
            EC_E_NOERROR or error code
        """
        gen_eCnfType = CEcWrapperTypes.Conv(eCnfType, "EC_T_CNF_TYPE")
        gen_pbyCnfData = CEcWrapperTypes.Conv(pbyCnfData, "byte[]")
        gen_dwCnfDataLen = CEcWrapperTypes.Conv(dwCnfDataLen, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigureMaster(self.m_dwMasterInstanceId, gen_eCnfType, gen_pbyCnfData, gen_dwCnfDataLen))
        return gen_dwRetVal

    def ConfigLoad(self, eCnfType, pbyCnfData, dwCnfDataLen): # ret: ECError
        """
        Load the master configuration.
        
        This function, in combination with ecatConfigApply, replaces ecatConfigureMaster and has to be called after ecatInitMaster and prior to calling ecatSetMasterState. Among others the EtherCAT topology defined in the given XML configuration file will be stored internally.
        
        \remark A client must not be registered prior to calling this function. In such a case the client registration will be lost.

        Args:
            eCnfType: Enum type of configuration data provided
            pbyCnfData: Configuration data
            dwCnfDataLen: Length of configuration data in byte

        Returns:
            EC_E_NOERROR or error code
        """
        gen_eCnfType = CEcWrapperTypes.Conv(eCnfType, "EC_T_CNF_TYPE")
        gen_pbyCnfData = CEcWrapperTypes.Conv(pbyCnfData, "byte[]")
        gen_dwCnfDataLen = CEcWrapperTypes.Conv(dwCnfDataLen, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigLoad(self.m_dwMasterInstanceId, gen_eCnfType, gen_pbyCnfData, gen_dwCnfDataLen))
        return gen_dwRetVal

    def ConfigExcludeSlave(self, wStationAddress): # ret: ECError
        """
        Exclude a slave from the master configuration.
        
        \note This function has to be called after ecatConfigLoad and prior to calling ecatConfigApply.

        Args:
            wStationAddress: Station address of the slave to be excluded. A value of 0 excludes all slaves.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_wStationAddress = CEcWrapperTypes.Conv(wStationAddress, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigExcludeSlave(self.m_dwMasterInstanceId, gen_wStationAddress))
        return gen_dwRetVal

    def ConfigIncludeSlave(self, wStationAddress): # ret: ECError
        """
        Include a slave in the master configuration, previously excluded by ecatConfigExcludeSlave.
        
        \note This function has to be called after ecatConfigLoad and prior to calling ecatConfigApply.

        Args:
            wStationAddress: Station address of the slave to be included. A value of 0 includes all slaves.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_wStationAddress = CEcWrapperTypes.Conv(wStationAddress, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigIncludeSlave(self.m_dwMasterInstanceId, gen_wStationAddress))
        return gen_dwRetVal

    def ConfigSetPreviousPort(self, wStationAddress, wStationAddressPrev, wPortPrev): # ret: ECError
        """
        Set previous port information of a slave
        
        \note This function has to be called after ecatConfigLoad and prior to calling ecatConfigApply.

        Args:
            wStationAddress: Station address of the slave
            wStationAddressPrev: Previous slave station address
            wPortPrev: Previous port

        Returns:
            EC_E_NOERROR or error code
        """
        gen_wStationAddress = CEcWrapperTypes.Conv(wStationAddress, "ushort")
        gen_wStationAddressPrev = CEcWrapperTypes.Conv(wStationAddressPrev, "ushort")
        gen_wPortPrev = CEcWrapperTypes.Conv(wPortPrev, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigSetPreviousPort(self.m_dwMasterInstanceId, gen_wStationAddress, gen_wStationAddressPrev, gen_wPortPrev))
        return gen_dwRetVal

    def ConfigAddJunctionRedundancyConnection(self, wHeadStationAddress, wHeadRedPort, wTailStationAddress, wTailRedPort): # ret: ECError
        """
        Since there is no mechanism to configure junction redundancy in the ENI, this API allows adding junction redundancy connections which will be validated by the EC-Master stack.
        
        \note This API can only be called between ecatConfigLoad() and ecatConfigApply(). Calling this API enables junction redundancy support implicitly.

        Args:
            wHeadStationAddress: Station address of the junction redundancy head slave. Typically this is an EtherCAT junction.
            wHeadRedPort: Port at head slave to which the junction redundancy cable is connected. Must be ESC_PORT_B
            wTailStationAddress: Station address of the junction redundancy tail slave
            wTailRedPort: Port at tail slave to which the junction redundancy cable is connected. May not be ESC_PORT_A.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_wHeadStationAddress = CEcWrapperTypes.Conv(wHeadStationAddress, "ushort")
        gen_wHeadRedPort = CEcWrapperTypes.Conv(wHeadRedPort, "ushort")
        gen_wTailStationAddress = CEcWrapperTypes.Conv(wTailStationAddress, "ushort")
        gen_wTailRedPort = CEcWrapperTypes.Conv(wTailRedPort, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigAddJunctionRedundancyConnection(self.m_dwMasterInstanceId, gen_wHeadStationAddress, gen_wHeadRedPort, gen_wTailStationAddress, gen_wTailRedPort))
        return gen_dwRetVal

    def ConfigApply(self): # ret: ECError
        """
        Apply the master configuration.
        
        \note This function has to be called after ecatConfigLoad.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigApply(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def ConfigExtend(self, bResetConfig, dwTimeout): # ret: ECError
        """
        This function extends the existing configuration described in the ENI to allow mailbox communication with unexpected slaves. After this function was called, unexpected slaves can reach PREOP state.
        
        \note After the configuration was extended, disconnecting any slave will generate a bus mismatch because all the slaves are part of the configuration. Recalling this function with bResetConfig set to EC_FALSE will extend the configuration again by any new connected unexpected slaves. The previous extension is not deleted.
        Calling the function with bResetConfig set to EC_TRUE, reset all the previous extensions.
        This function may not be called from within the JobTask's context.

        Args:
            bResetConfig: EC_TRUE: Extended configuration will be removed
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bResetConfig = CEcWrapperTypes.Conv(bResetConfig, "bool")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecConfigExtend(self.m_dwMasterInstanceId, gen_bResetConfig, gen_dwTimeout))
        return gen_dwRetVal

    def IsConfigured(self, pbIsConfigured): # ret: ECError
        """
        Returns if configuration has been applied

        Args:
            pbIsConfigured: EC_TRUE if configuration has been applied

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pbIsConfigured = CEcWrapperTypes.Conv(pbIsConfigured, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecIsConfigured(self.m_dwMasterInstanceId, ctypes.pointer(gen_pbIsConfigured)))
        return gen_dwRetVal

    def SetMasterState(self, dwTimeout, eReqState): # ret: ECError
        """
        Set the EtherCAT master (and all slaves) into the requested state.
        
        \note If the function is called with EC_NOWAIT, the client may wait for reaching the requested state using the notification callback (EC_NOTIFY_STATECHANGED).\n
        Master by default will just change to a higher state, if all slaves have reached the requested state. It may happen that some slaves are in higher state at network than Master, e.g.:
        - Master and all slaves are in PREOP
        - Application requests SAFEOP
        - Master starts transition for all slaves
        - Some slaves changed to SAFEOP, but some fail and therefore stay in PREOP
        - Master state stays in PREOP, function returns with error
        \n
        The application can request SAFEOP again to re-request state of previously failed slaves.
        Transition to lower state: The master changes to lower state, even if one slave is not able to follow.
        This function may not be called from within the JobTask's context with dwTimeout other than EC_NOWAIT.

        Args:
            dwTimeout: Timeout [ms] This function will block until the requested state is reached or the timeout elapsed. If the timeout value is set to EC_NOWAIT the function will return immediately.
            eReqState: Requested System state

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_eReqState = CEcWrapperTypes.Conv(eReqState, "EC_T_STATE")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetMasterState(self.m_dwMasterInstanceId, gen_dwTimeout, gen_eReqState))
        return gen_dwRetVal

    def GetMasterState(self): # ret: DN_EC_T_STATE
        """
        Get the EtherCAT master current state.

        Args:

        Returns:
            EtherCAT master state
        """
        gen_dwRetVal = DN_EC_T_STATE(CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetMasterState(self.m_dwMasterInstanceId)))
        return gen_dwRetVal

    def Start(self, dwTimeout): # ret: ECError
        """
        The EtherCAT master and all slaves will be set into the OPERATIONAL state
        
        \deprecated Use emSetMasterState() instead
        
        \note If the function is called with EC_NOWAIT, the client may wait for reaching the OPERATIONAL state using the notification callback (EC_NOTIFY_STATECHANGED).
        This function may not be called from within the JobTask's context.

        Args:
            dwTimeout: Timeout [ms] This function will block until the OPERATIONAL state is reached or the timeout elapsed. If the timeout value is set to EC_NOWAIT the function will return immediately.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecStart(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def Stop(self, dwTimeout): # ret: ECError
        """
        The EtherCAT master and all slaves will be set back into the INIT state.
        
        \deprecated Use emSetMasterState() instead
        
        \note If the function is called with EC_NOWAIT, the client may wait for reaching the INIT state using the notification callback (ECAT_NOTIFY_STATECHANGE).
        This function may not be called from within the JobTask's context.

        Args:
            dwTimeout: Timeout [ms] This function will block until the INIT state is reached or the timeout elapsed. If the timeout value is set to EC_NOWAIT the function will return immediately.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecStop(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def GetSlaveId(self, wStationAddress): # ret: uint
        """
        Determines the slave ID using the slave station address.

        Args:
            wStationAddress: Station address of the slave

        Returns:
            Slave ID or INVALID_SLAVE_ID if the slave could not be found or stack is not initialized
        """
        gen_wStationAddress = CEcWrapperTypes.Conv(wStationAddress, "ushort")
        gen_dwRetVal = CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetSlaveId(self.m_dwMasterInstanceId, gen_wStationAddress))
        return gen_dwRetVal

    def GetSlaveFixedAddr(self, dwSlaveId, out_pwFixedAddr): # ret: ECError
        """
        Determine slave station address according to its slave ID.

        Args:
            dwSlaveId: Slave ID
            pwFixedAddr: Corresponding fixed address

        Returns:
            - EC_E_NOERROR or error code
            - EC_E_NOTFOUND if slave not found
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        pwFixedAddr = 0
        gen_pwFixedAddr = CEcWrapperTypes.Conv(pwFixedAddr, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveFixedAddr(self.m_dwMasterInstanceId, gen_dwSlaveId, ctypes.pointer(gen_pwFixedAddr)))
        out_pwFixedAddr.value = CEcWrapperTypes.Conv(gen_pwFixedAddr, "ushort")
        return gen_dwRetVal

    def GetSlaveIdAtPosition(self, wAutoIncAddress): # ret: uint
        """
        Determines the slave ID using the slave auto increment address.

        Args:
            wAutoIncAddress: Auto increment address of the slave

        Returns:
            Slave ID or INVALID_SLAVE_ID if the slave could not be found
        """
        gen_wAutoIncAddress = CEcWrapperTypes.Conv(wAutoIncAddress, "ushort")
        gen_dwRetVal = CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetSlaveIdAtPosition(self.m_dwMasterInstanceId, gen_wAutoIncAddress))
        return gen_dwRetVal

    def GetSlaveProp(self, dwSlaveId, out_pSlaveProp): # ret: bool
        """
        Determines the properties of the slave device.
        
        \deprecated Use emGetCfgSlaveInfo instead

        Args:
            dwSlaveId: Slave ID
            pSlaveProp: Slave properties

        Returns:
            EC_TRUE if the slave exists, EC_FALSE if the slave id is invalid
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        pSlaveProp = DN_EC_T_SLAVE_PROP()
        gen_pSlaveProp = CEcWrapperTypes.Conv(pSlaveProp, "EC_T_SLAVE_PROP")
        gen_dwRetVal = CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetSlaveProp(self.m_dwMasterInstanceId, gen_dwSlaveId, ctypes.pointer(gen_pSlaveProp)))
        out_pSlaveProp.value = CEcWrapperTypes.Conv(gen_pSlaveProp, "DN_EC_T_SLAVE_PROP")
        return gen_dwRetVal

    def GetSlavePortState(self, dwSlaveId, pwPortState): # ret: ECError
        """
        Returns the state of the slave ports.

        Args:
            dwSlaveId: Slave ID
            pwPortState: Slave port state.\n Format: wwww xxxx yyyy zzzz (each nibble : port 3210)\n

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_INVALIDSTATE if master is not initialized
            - EC_E_NOTFOUND if the slave with ID dwSlaveId does not exist
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_pwPortState = CEcWrapperTypes.Conv(pwPortState, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlavePortState(self.m_dwMasterInstanceId, gen_dwSlaveId, ctypes.pointer(gen_pwPortState)))
        return gen_dwRetVal

    def GetSlaveState(self, dwSlaveId, out_pwCurrDevState, out_pwReqDevState): # ret: ECError
        """
        Get the slave's state.
        
        \note The slave state is always read automatically from the AL_STATUS register whenever necessary. It is not forced by calling this function.
        This function may be called from within the JobTask's context.

        Args:
            dwSlaveId: Slave ID
            pwCurrDevState: Current slave state.
            pwReqDevState: Requested slave state

        Returns:
            - EC_E_NOERROR on success.
            - EC_E_SLAVE_NOT_PRESENT if the slave is not present on bus.
            - EC_E_NOTFOUND if the slave with ID dwSlaveId does not exist in the XML file.
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        pwCurrDevState = 0
        gen_pwCurrDevState = CEcWrapperTypes.Conv(pwCurrDevState, "ushort")
        pwReqDevState = 0
        gen_pwReqDevState = CEcWrapperTypes.Conv(pwReqDevState, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveState(self.m_dwMasterInstanceId, gen_dwSlaveId, ctypes.pointer(gen_pwCurrDevState), ctypes.pointer(gen_pwReqDevState)))
        out_pwReqDevState.value = CEcWrapperTypes.Conv(gen_pwReqDevState, "ushort")
        out_pwCurrDevState.value = CEcWrapperTypes.Conv(gen_pwCurrDevState, "ushort")
        return gen_dwRetVal

    def SetSlaveState(self, dwSlaveId, wNewReqDevState, dwTimeout): # ret: ECError
        """
        Set a specified slave into the requested state.
        
        \note The requested state shall not be higher than the overall operational state.
        DEVICE_STATE_BOOTSTRAP can only be requested if the slave's state is INIT.
        This function may not be called from within the JobTask's context.

        Args:
            dwSlaveId: Slave ID
            wNewReqDevState: Requested state
            dwTimeout: Timeout [ms] May not be EC_NOWAIT!

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_BUSY if the master cannot execute the request at this time, the function has to be called at a later time
            - EC_E_NOTFOUND if the slave does not exist
            - EC_E_NOTREADY if the working counter was not set when requesting the slave's state (slave may not be connected or did not respond)
            - EC_E_TIMEOUT if the slave did not enter the requested state in time
            - EC_E_INVALIDSTATE if the master denies the requested state, see comments below
            - EC_E_INVALIDPARM if BOOTSTRAP was requested for a slave that does not support it
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_wNewReqDevState = CEcWrapperTypes.Conv(wNewReqDevState, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetSlaveState(self.m_dwMasterInstanceId, gen_dwSlaveId, gen_wNewReqDevState, gen_dwTimeout))
        return gen_dwRetVal

    def TferSingleRawCmd(self, byCmd, dwMemoryAddress, pbyData, wLen, dwTimeout): # ret: ECError
        """
        Transfers a single raw EtherCAT command to one or multiple slaves and waits for the result. Using this function it is possible exchange arbitrary data between the master and the slaves.
        When the master receives the response to the queued frame it raises EC_NOTIFY_RAWCMD_DONE to all clients.
        
        \note This function blocks until the command is completely processed.
        In case of read commands the slave data will be written back into the given memory area.
        If a timeout occurs (e.g. due to a bad line quality) the corresponding frame will be sent again.
        The timeout value and retry counter can be set using the master configuration parameters dwEcatCmdTimeout and dwEcatCmdMaxRetries. The call will return in any case (without waiting for the number of retries specified in dwEcatCmdMaxRetries) if the time determined with the dwTimeout parameter elapsed.
        Caveat: Using auto increment addressing (APRD, APWR, APRW) may lead to unexpected results in case the selected slave does not increment the working counter. In such cases the EtherCAT command would be handled by the slave directly behind the selected one.
        This function may not be called from within the JobTask's context.

        Args:
            byCmd: EtherCAT command type. EC_CMD_TYPE_...
            dwMemoryAddress: Slave memory address, depending on the command to be sent this is either a physical or logical address.
            pbyData: [in, out] Buffer containing or receiving transfered data
            wLen: Number of bytes to transfer
            dwTimeout: Timeout [ms]

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_BUSY another transfer request is already pending
            - EC_E_NOTFOUND if the slave with ID dwSlaveId does not exist
            - EC_E_NOTREADY if the working counter was not set when sending the command (slave may not be connected or did not respond)
            - EC_E_TIMEOUT if the slave did not respond to the command
            - EC_E_BUSY if the master or the corresponding slave is currently changing its operational state
            - EC_E_INVALIDPARM if the command is not supported or the timeout value is set to EC_NOWAIT
            - EC_E_INVALIDSIZE if the size of the complete command does not fit into a single Ethernet frame. The maximum amount of data to transfer must not exceed 1486 bytes
        """
        gen_byCmd = CEcWrapperTypes.Conv(byCmd, "byte")
        gen_dwMemoryAddress = CEcWrapperTypes.Conv(dwMemoryAddress, "uint")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_wLen = CEcWrapperTypes.Conv(wLen, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecTferSingleRawCmd(self.m_dwMasterInstanceId, gen_byCmd, gen_dwMemoryAddress, gen_pbyData, gen_wLen, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def ReadSlaveRegister(self, bFixedAddressing, wSlaveAddress, wRegisterOffset, pbyData, wLen, dwTimeout): # ret: ECError
        """
        Reads data from the ESC memory of a specified slave.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wRegisterOffset: Register offset. I.e. use 0x0130 to read the AL Status register.
            pbyData: Buffer receiving transfered data
            wLen: Number of bytes to receive
            dwTimeout: Timeout [ms]

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_SLAVE_NOT_PRESENT if slave not present
            - EC_E_BUSY another transfer request is already pending
            - EC_E_NOTFOUND if the slave with the given address does not exist
            - EC_E_NOTREADY if the working counter was not set when sending the command (slave may not be connected or did not respond)
            - EC_E_TIMEOUT if the slave did not respond to the command
            - EC_E_BUSY if the master or the corresponding slave is currently changing its operational state
            - EC_E_INVALIDPARM if the command is not supported or the timeout value is set to EC_NOWAIT
            - EC_E_INVALIDSIZE if the size of the complete command does not fit into a single Ethernet frame. The maximum amount of data to transfer must not exceed 1486 bytes
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wRegisterOffset = CEcWrapperTypes.Conv(wRegisterOffset, "ushort")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_wLen = CEcWrapperTypes.Conv(wLen, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReadSlaveRegister(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wRegisterOffset, gen_pbyData, gen_wLen, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def ReadSlaveRegisterReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, wRegisterOffset, pbyData, wLen): # ret: ECError
        """
        Requests data read transfer from the ESC memory of a specified slave and returns immediately.
        
        \note This function may be called from within the JobTask's context.
        A notification EC_NOTIFY_SLAVE_REGISTER_TRANSFER is given on completion.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wRegisterOffset: Register offset, e.g. use 0x0130 to read the AL Status register.
            pbyData: Buffer receiving transfered data
            wLen: Number of bytes to receive

        Returns:
            - EC_E_NOERROR if successful.
            - EC_E_SLAVE_NOT_PRESENT if slave not present.
            - EC_E_NOTFOUND if the slave with the given address does not exist.
            - EC_E_INVALIDPARM if the command is not supported or the timeout value is set to EC_NOWAIT.
            - EC_E_INVALIDSIZE if the size of the complete command does not fit into a single Ethernet frame. The maximum amount of data to transfer must not exceed 1486 bytes.
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wRegisterOffset = CEcWrapperTypes.Conv(wRegisterOffset, "ushort")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_wLen = CEcWrapperTypes.Conv(wLen, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReadSlaveRegisterReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wRegisterOffset, gen_pbyData, gen_wLen))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def WriteSlaveRegister(self, bFixedAddressing, wSlaveAddress, wRegisterOffset, pbyData, wLen, dwTimeout): # ret: ECError
        """
        Writes data into the ESC memory of a specified slave.
        
        \warning Changing contents of ESC registers may lead to unpredictiable behavior of the slaves and/or the master.
        
        \note This function may not be called from within the JobTask's context

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wRegisterOffset: Register offset, e.g. use 0x0120 to write to the AL Control register.
            pbyData: Buffer containing transfered data
            wLen: Number of bytes to send
            dwTimeout: Timeout [ms]

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_SLAVE_NOT_PRESENT if slave not present
            - EC_E_BUSY another transfer request is already pending
            - EC_E_NOTFOUND if the slave with the given address does not exist
            - EC_E_NOTREADY if the working counter was not set when sending the command (slave may not be connected or did not respond)
            - EC_E_TIMEOUT if the slave did not respond to the command
            - EC_E_BUSY if the master or the corresponding slave is currently changing its operational state
            - EC_E_INVALIDPARM if the command is not supported or the timeout value is set to EC_NOWAIT
            - EC_E_INVALIDSIZE if the size of the complete command does not fit into a single Ethernet frame. The maximum amount of data to transfer must not exceed 1486 bytes
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wRegisterOffset = CEcWrapperTypes.Conv(wRegisterOffset, "ushort")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_wLen = CEcWrapperTypes.Conv(wLen, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecWriteSlaveRegister(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wRegisterOffset, gen_pbyData, gen_wLen, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def WriteSlaveRegisterReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, wRegisterOffset, pbyData, wLen): # ret: ECError
        """
        Requests a data write transfer into the ESC memory of a specified slave and returns immediately.
        
        \warning Changing contents of ESC registers may lead to unpredictiable behavior of the slaves and/or the master.
        
        \note This function may be called from within the JobTask's context.
        A notification EC_NOTIFY_SLAVE_REGISTER_TRANSFER is given on completion.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wRegisterOffset: Register offset. I.e. use 0x0120 to write to the AL Control register
            pbyData: Buffer containing transfered data
            wLen: Number of bytes to send

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_SLAVE_NOT_PRESENT if slave not present
            - EC_E_NOTFOUND if the slave with the given address does not exist
            - EC_E_INVALIDPARM if the command is not supported or the timeout value is set to EC_NOWAIT
            - EC_E_INVALIDSIZE if the size of the complete command does not fit into a single Ethernet frame. The maximum amount of data to transfer must not exceed 1486 bytes
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wRegisterOffset = CEcWrapperTypes.Conv(wRegisterOffset, "ushort")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_wLen = CEcWrapperTypes.Conv(wLen, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecWriteSlaveRegisterReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wRegisterOffset, gen_pbyData, gen_wLen))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def QueueRawCmd(self, wInvokeId, byCmd, dwMemoryAddress, pbyData, wLen): # ret: ECError
        """
        Transfers a raw EtherCAT command to one or multiple slaves. All registered clients will be notified.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            wInvokeId: Invoke ID to reassign the results to the sent cmd.
            byCmd: EtherCAT command
            dwMemoryAddress: Slave memory address, depending on the command to be sent this is either a physical or logical address.
            pbyData: [in, out] Buffer containing or receiving transfered data In case a read-only command is queued (e.g. APRD) this pointer should be set to a value of EC_NULL
            wLen: Number of bytes to transfer.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_wInvokeId = CEcWrapperTypes.Conv(wInvokeId, "ushort")
        gen_byCmd = CEcWrapperTypes.Conv(byCmd, "byte")
        gen_dwMemoryAddress = CEcWrapperTypes.Conv(dwMemoryAddress, "uint")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_wLen = CEcWrapperTypes.Conv(wLen, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecQueueRawCmd(self.m_dwMasterInstanceId, gen_wInvokeId, gen_byCmd, gen_dwMemoryAddress, gen_pbyData, gen_wLen))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def ClntQueueRawCmd(self, dwClntId, wInvokeId, byCmd, dwMemoryAddress, pbyData, wLen): # ret: ECError
        """
        Transfers a raw EtherCAT command to one or multiple slaves. Using this function it is possible to exchange data between the master and the slaves.
        When the response to the queued frame is received, the notification EC_NOTIFY_RAWCMD_DONE is given for the appropriate client.
        
        \note This function queues a single EtherCAT command. Queued raw commands will be sent after sending cyclic process data values.
        If a timeout occurs the corresponding frame will be sent again, the timeout value and retry counter can be set using the master configuration parameters EC_T_INIT_MASTER_PARMS.dwEcatCmdTimeout and EC_T_INIT_MASTER_PARMS.dwEcatCmdMaxRetries.\n
        Using auto increment addressing (APRD, APWR, APRW) may lead to unexpected results in case the selected slave does not increment the working counter. In such cases the EtherCAT command would be handled by the slave directly behind the selected one.
        This function may not be called from within the JobTask's context.

        Args:
            dwClntId: Client ID to be notified (0 if all registered clients shall be notified).
            wInvokeId: Invoke ID to reassign the results to the sent cmd
            byCmd: EtherCAT command
            dwMemoryAddress: Slave memory address, depending on the command to be sent this is either a physical or logical address
            pbyData: [in, out] Buffer containing or receiving transfered data. In case a read-only command is queued (e.g. APRD) this pointer should be set to a value of EC_NULL.
            wLen: Number of bytes to transfer.

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_NOTFOUND if the slave with ID dwSlaveId does not exist
            - EC_E_BUSY if the master or the corresponding slave is currently changing its operational state
            - EC_E_INVALIDPARM  if the command is not supported
            - EC_E_INVALIDSIZE if the size of the complete command does not fit into a single Ethernet frame. The maximum amount of data to transfer must not exceed 1486 bytes
        """
        gen_dwClntId = CEcWrapperTypes.Conv(dwClntId, "uint")
        gen_wInvokeId = CEcWrapperTypes.Conv(wInvokeId, "ushort")
        gen_byCmd = CEcWrapperTypes.Conv(byCmd, "byte")
        gen_dwMemoryAddress = CEcWrapperTypes.Conv(dwMemoryAddress, "uint")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_wLen = CEcWrapperTypes.Conv(wLen, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecClntQueueRawCmd(self.m_dwMasterInstanceId, gen_dwClntId, gen_wInvokeId, gen_byCmd, gen_dwMemoryAddress, gen_pbyData, gen_wLen))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def GetNumConfiguredSlaves(self): # ret: uint
        """
        Returns number of slaves which are configured in the ENI.

        Args:

        Returns:
            Number of slaves
        """
        gen_dwRetVal = CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetNumConfiguredSlaves(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def MbxTferAbort(self, pMbxTfer): # ret: ECError
        """
        Abort a running mailbox transfer.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            pMbxTfer: Mailbox transfer object created with emMbxTferCreate

        Returns:
            EC_E_NOERROR if successful
        """
        gen_pMbxTfer = CEcWrapperTypes.Conv(pMbxTfer, "IntPtr")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecMbxTferAbort(self.m_dwMasterInstanceId, gen_pMbxTfer))
        return gen_dwRetVal

    def MbxTferDelete(self, pMbxTfer): # ret: void
        """
        Deletes a mailbox transfer object.
        
        \note A transfer object may only be deleted if it is in the Idle state.

        Args:
            pMbxTfer: Mailbox transfer object created with emMbxTferCreate
        """
        gen_pMbxTfer = CEcWrapperTypes.Conv(pMbxTfer, "IntPtr")
        CEcWrapper.Get().ecMbxTferDelete(self.m_dwMasterInstanceId, gen_pMbxTfer)
        return

    def ClntSendRawMbx(self, dwClntId, pbyMbxCmd, dwMbxCmdLen, dwTimeout): # ret: ECError
        """
        Send a raw mailbox command

        Args:
            dwClntId: Client ID
            pbyMbxCmd: Buffer containing the raw mbx cmd starting with mailbox header
            dwMbxCmdLen: Length of pbyMbxCmd buffer
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClntId = CEcWrapperTypes.Conv(dwClntId, "uint")
        gen_pbyMbxCmd = CEcWrapperTypes.Conv(pbyMbxCmd, "byte[]")
        gen_dwMbxCmdLen = CEcWrapperTypes.Conv(dwMbxCmdLen, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecClntSendRawMbx(self.m_dwMasterInstanceId, gen_dwClntId, gen_pbyMbxCmd, gen_dwMbxCmdLen, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyMbxCmd, pbyMbxCmd)
        return gen_dwRetVal

    def CoeSdoDownloadReq(self, pMbxTfer, dwSlaveId, wObIndex, byObSubIndex, dwTimeout, dwFlags): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeSdoDownload(self, dwSlaveId, wObIndex, byObSubIndex, pbyData, dwDataLen, dwTimeout, dwFlags): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeSdoUploadReq(self, pMbxTfer, dwSlaveId, wObIndex, byObSubIndex, dwTimeout, dwFlags): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeSdoUpload(self, dwSlaveId, wObIndex, byObSubIndex, pbyData, dwDataLen, out_pdwOutDataLen, dwTimeout, dwFlags): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeGetODList(self, pMbxTfer, dwSlaveId, eListType, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeGetObjectDesc(self, pMbxTfer, dwSlaveId, wObIndex, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeGetEntryDesc(self, pMbxTfer, dwSlaveId, wObIndex, byObSubIndex, byValueInfo, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def CoeRxPdoTfer(self, pMbxTfer, dwSlaveId, dwNumber, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def FoeFileUpload(self, dwSlaveId, achFileName, dwFileNameLen, pbyData, dwDataLen, out_pdwOutDataLen, dwPassword, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def FoeFileDownload(self, dwSlaveId, achFileName, dwFileNameLen, pbyData, dwDataLen, dwPassword, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def FoeUploadReq(self, pMbxTfer, dwSlaveId, achFileName, dwFileNameLen, dwPassword, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def FoeSegmentedUploadReq(self, pMbxTfer, dwSlaveId, szFileName, dwFileNameLen, dwFileSize, dwPassword, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def FoeDownloadReq(self, pMbxTfer, dwSlaveId, achFileName, dwFileNameLen, dwPassword, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def FoeSegmentedDownloadReq(self, pMbxTfer, dwSlaveId, szFileName, dwFileNameLen, dwFileSize, dwPassword, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SoeWrite(self, dwSlaveId, byDriveNo, pbyElementFlags, wIDN, pbyData, dwDataLen, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SoeRead(self, dwSlaveId, byDriveNo, pbyElementFlags, wIDN, pbyData, dwDataLen, out_pdwOutDataLen, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SoeAbortProcCmd(self, dwSlaveId, byDriveNo, pbyElementFlags, wIDN, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SoeWriteReq(self, pMbxTfer, dwSlaveId, byDriveNo, pbyElementFlags, wIDN, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def SoeReadReq(self, pMbxTfer, dwSlaveId, byDriveNo, pbyElementFlags, wIDN, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def AoeGetSlaveNetId(self, dwSlaveId, out_poAoeNetId): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def AoeRead(self, dwSlaveId, poTargetNetId, wTargetPort, dwIndexGroup, dwIndexOffset, dwDataLen, pbyData, out_pdwDataOutLen, out_pdwErrorCode, out_pdwCmdResult, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def AoeReadReq(self, pMbxTfer, dwSlaveId, poTargetNetId, wTargetPort, dwIndexGroup, dwIndexOffset, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def AoeWrite(self, dwSlaveId, poTargetNetId, wTargetPort, dwIndexGroup, dwIndexOffset, dwDataLen, pbyData, out_pdwErrorCode, out_pdwCmdResult, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def AoeWriteReq(self, pMbxTfer, dwSlaveId, poTargetNetId, wTargetPort, dwIndexGroup, dwIndexOffset, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def AoeReadWrite(self, dwSlaveId, poTargetNetId, wTargetPort, dwIndexGroup, dwIndexOffset, dwReadDataLen, dwWriteDataLen, pbyData, out_pdwDataOutLen, out_pdwErrorCode, out_pdwCmdResult, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def AoeWriteControl(self, dwSlaveId, poTargetNetId, wTargetPort, wAoEState, wDeviceState, dwDataLen, pbyData, pdwErrorCode, pdwCmdResult, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def VoeRead(self, dwSlaveId, pbyData, dwDataLen, out_pdwOutDataLen, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def VoeWrite(self, dwSlaveId, pbyData, dwDataLen, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def VoeWriteReq(self, pMbxTfer, dwSlaveId, dwTimeout): # ret: ECError
        # eval limitation
        # pylint: disable=unused-argument
        return self.ReportErrorCode(ECError.EC_NOTSUPPORTED)


    def GetProcessData(self, bOutputData, dwOffset, pbyData, dwLength, dwTimeout): # ret: ECError
        """
        Retrieve Process data synchronized. If process data are required outside the cyclic master job task (which is calling ecatExecJob), direct access to the process data is not recommended as data consistency cannot be guaranteed. A call to this function will send a data read request to the master stack and then check every millisecond whether new data are provided. The master stack will provide new data after calling ecatExecJob(eUsrJob_ MasterTimer) within the job task. This function is usually only called remotely (using the Remote API).
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bOutputData: EC_TRUE: read output data, EC_FALSE: read input data.
            dwOffset: Byte offset in Process data to read from.
            pbyData: Buffer receiving transfered data
            dwLength: 
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bOutputData = CEcWrapperTypes.Conv(bOutputData, "bool")
        gen_dwOffset = CEcWrapperTypes.Conv(dwOffset, "uint")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_dwLength = CEcWrapperTypes.Conv(dwLength, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetProcessData(self.m_dwMasterInstanceId, gen_bOutputData, gen_dwOffset, gen_pbyData, gen_dwLength, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def SetProcessData(self, bOutputData, dwOffset, pbyData, dwLength, dwTimeout): # ret: ECError
        """
        Write Process data synchronized. If process data shall be set outside the cyclic master job task (which is calling ecatExecJob), direct access to the process data is not recommended as data consistency cannot be guaranteed.
        A call to this function will send a data write request to the master stack and then check every millisecond whether new data is written.
        The master stack will copy the data after calling ecatExecJob(eUsrJob_ MasterTimer) within the job task. This function is usually only called remotely (using the Remote API).
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bOutputData: EC_TRUE: write output data, EC_FALSE: write input data.
            dwOffset: Byte offset in Process data to write to.
            pbyData: Buffer containing transfered data
            dwLength: 
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bOutputData = CEcWrapperTypes.Conv(bOutputData, "bool")
        gen_dwOffset = CEcWrapperTypes.Conv(dwOffset, "uint")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_dwLength = CEcWrapperTypes.Conv(dwLength, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetProcessData(self.m_dwMasterInstanceId, gen_bOutputData, gen_dwOffset, gen_pbyData, gen_dwLength, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def SetProcessDataBits(self, bOutputData, dwBitOffsetPd, pbyDataSrc, dwBitLengthSrc, dwTimeout): # ret: ECError
        """
        Writes a specific number of bits from a given buffer to the process image with a bit offset (synchronized).
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bOutputData: EC_TRUE: write output data, EC_FALSE: write input data.
            dwBitOffsetPd: Bit offset in Process data image.
            pbyDataSrc: 
            dwBitLengthSrc: 
            dwTimeout: Timeout [ms] The timeout value must not be set to EC_NOWAIT.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bOutputData = CEcWrapperTypes.Conv(bOutputData, "bool")
        gen_dwBitOffsetPd = CEcWrapperTypes.Conv(dwBitOffsetPd, "uint")
        gen_pbyDataSrc = CEcWrapperTypes.Conv(pbyDataSrc, "byte[]")
        gen_dwBitLengthSrc = CEcWrapperTypes.Conv(dwBitLengthSrc, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetProcessDataBits(self.m_dwMasterInstanceId, gen_bOutputData, gen_dwBitOffsetPd, gen_pbyDataSrc, gen_dwBitLengthSrc, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyDataSrc, pbyDataSrc)
        return gen_dwRetVal

    def GetProcessDataBits(self, bOutputData, dwBitOffsetPd, pbyDataDst, dwBitLengthDst, dwTimeout): # ret: ECError
        """
        Reads a specific number of bits from the process image to the given buffer with a bit offset (synchronized).
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bOutputData: EC_TRUE: read output data, EC_FALSE: write input data.
            dwBitOffsetPd: Bit offset in Process data image.
            pbyDataDst: 
            dwBitLengthDst: 
            dwTimeout: Timeout [ms] The timeout value must not be set to EC_NOWAIT.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bOutputData = CEcWrapperTypes.Conv(bOutputData, "bool")
        gen_dwBitOffsetPd = CEcWrapperTypes.Conv(dwBitOffsetPd, "uint")
        gen_pbyDataDst = CEcWrapperTypes.Conv(pbyDataDst, "byte[]")
        gen_dwBitLengthDst = CEcWrapperTypes.Conv(dwBitLengthDst, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetProcessDataBits(self.m_dwMasterInstanceId, gen_bOutputData, gen_dwBitOffsetPd, gen_pbyDataDst, gen_dwBitLengthDst, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyDataDst, pbyDataDst)
        return gen_dwRetVal

    def ForceProcessDataBits(self, dwClientId, bOutputData, dwBitOffsetPd, wBitLength, pbyData, dwTimeout): # ret: ECError
        """
        Force a specific number of bits from a given buffer to the process image with a bit offset.
        All output data set by this API are overwriting the values set by the application. All input data set by this API are overwriting the values read from the slaves.
        Forcing will be terminiated by calling the corresponding functions.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            bOutputData: EC_TRUE: write output data, EC_FALSE: write input data.
            dwBitOffsetPd: Bit offset in Process data image
            wBitLength: 
            pbyData: Buffer containing transfered data
            dwTimeout: Timeout [ms] The timeout value must not be set to EC_NOWAIT.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_bOutputData = CEcWrapperTypes.Conv(bOutputData, "bool")
        gen_dwBitOffsetPd = CEcWrapperTypes.Conv(dwBitOffsetPd, "uint")
        gen_wBitLength = CEcWrapperTypes.Conv(wBitLength, "ushort")
        gen_pbyData = CEcWrapperTypes.Conv(pbyData, "byte[]")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecForceProcessDataBits(self.m_dwMasterInstanceId, gen_dwClientId, gen_bOutputData, gen_dwBitOffsetPd, gen_wBitLength, gen_pbyData, gen_dwTimeout))
        CEcWrapperTypes.Conv_Array(gen_pbyData, pbyData)
        return gen_dwRetVal

    def ReleaseProcessDataBits(self, dwClientId, bOutputData, dwBitOffsetPd, wBitLength, dwTimeout): # ret: ECError
        """
        Release previously forced process data.\n
        For a forced output: Value set by application become valid again. Because forced process data bits are writen directly into the process output image,
        the application has to update the process image with the required value, otherwise the forced value is still valid.\n
        For a forced input: Value read from the slaves become valid again.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            bOutputData: EC_TRUE: write output data, EC_FALSE: write input data
            dwBitOffsetPd: Bit offset in Process data image
            wBitLength: Number of bits that shall be written to the process image.
            dwTimeout: Timeout [ms] The timeout value must not be set to EC_NOWAIT.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_bOutputData = CEcWrapperTypes.Conv(bOutputData, "bool")
        gen_dwBitOffsetPd = CEcWrapperTypes.Conv(dwBitOffsetPd, "uint")
        gen_wBitLength = CEcWrapperTypes.Conv(wBitLength, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReleaseProcessDataBits(self.m_dwMasterInstanceId, gen_dwClientId, gen_bOutputData, gen_dwBitOffsetPd, gen_wBitLength, gen_dwTimeout))
        return gen_dwRetVal

    def ReleaseAllProcessDataBits(self, dwClientId, dwTimeout): # ret: ECError
        """
        Release all previously forced process data for a dedicated client. \n
        For a forced output: Value set by application become valid again. Because forced process data bits are writen directly into the process output image,
        the application has to update the process image with the required value, otherwise the forced value is still valid.\n
        For a forced input: Value read from the slaves become valid again.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTimeout: Timeout [ms] The timeout value must not be set to EC_NOWAIT.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReleaseAllProcessDataBits(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTimeout))
        return gen_dwRetVal

    def GetNumConnectedSlaves(self): # ret: uint
        """
        Get amount of currently connected slaves.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecGetNumConnectedSlaves(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def GetNumConnectedSlavesMain(self): # ret: ECError
        """
        Get the amount of currently connected Slaves to main interface.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetNumConnectedSlavesMain(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def GetNumConnectedSlavesRed(self): # ret: ECError
        """
        Get the amount of currently connected Slaves to redundancy interface.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetNumConnectedSlavesRed(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def ReadSlaveEEPRomReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, wEEPRomStartOffset, pwReadData, dwReadLen, pdwNumOutData, dwTimeout): # ret: ECError
        """
        Requests a EEPROM data read operation from slave and returns immediately.
        
        \note This function may be called from within the JobTask's context.
        A 4.6.42 ecatNotify - EC_NOTIFY_EEPROM_OPERATION is given on completion or timeout, see below.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_EEPROM_OPERATION_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wEEPRomStartOffset: Word address to start EEPROM read from
            pwReadData: Pointer to EC_T_WORD array to carry the read data, must be valid until the operation complete
            dwReadLen: Size of the EC_T_WORD array provided at pwReadData (in EC_T_WORDs)
            pdwNumOutData: Pointer to EC_T_DWORD carrying actually read data (in EC_T_WORDs) after completion
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wEEPRomStartOffset = CEcWrapperTypes.Conv(wEEPRomStartOffset, "ushort")
        gen_pwReadData = CEcWrapperTypes.Conv(pwReadData, "ushort")
        gen_dwReadLen = CEcWrapperTypes.Conv(dwReadLen, "uint")
        gen_pdwNumOutData = CEcWrapperTypes.Conv(pdwNumOutData, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReadSlaveEEPRomReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wEEPRomStartOffset, ctypes.pointer(gen_pwReadData), gen_dwReadLen, ctypes.pointer(gen_pdwNumOutData), gen_dwTimeout))
        return gen_dwRetVal

    def WriteSlaveEEPRomReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, wEEPRomStartOffset, pwWriteData, dwWriteLen, dwTimeout): # ret: ECError
        """
        Requests a EEPROM data write operation from slave and returns immediately.
        
        \note The EEPROM's CRC is updated automatically. A reset of the slave controller is needed to reload the alias address in register 0x12.
        A EC_NOTIFY_EEPROM_OPERATION is given on completion or timeout. This function may be called from within the JobTask's context.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_EEPROM_OPERATION_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wEEPRomStartOffset: Word address to start EEPROM Write from.
            pwWriteData: Pointer to WORD array carrying the write data, must be valid until operation complete
            dwWriteLen: Sizeof Write Data WORD array (in WORDS)
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wEEPRomStartOffset = CEcWrapperTypes.Conv(wEEPRomStartOffset, "ushort")
        gen_pwWriteData = CEcWrapperTypes.Conv(pwWriteData, "ushort")
        gen_dwWriteLen = CEcWrapperTypes.Conv(dwWriteLen, "uint")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecWriteSlaveEEPRomReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wEEPRomStartOffset, ctypes.pointer(gen_pwWriteData), gen_dwWriteLen, gen_dwTimeout))
        return gen_dwRetVal

    def ReloadSlaveEEPRom(self, bFixedAddressing, wSlaveAddress, dwTimeout): # ret: ECError
        """
        Causes a slave to reload its EEPROM values to ESC registers.
        
        \note Alias address at 0x12 is not reloaded through this command, this is prevented by the slave hardware. The slave controller must be reset to reload the alias address.
        This function may not be called from within the JobTask's context.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            dwTimeout: Timeout [ms] The function will block at most for this time. The timeout value must not be set to EC_NOWAIT

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReloadSlaveEEPRom(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_dwTimeout))
        return gen_dwRetVal

    def ReloadSlaveEEPRomReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, dwTimeout): # ret: ECError
        """
        Request a slave to reload its EEPROM values to ESC registers, and returns immediately.
        
        \note Alias address at 0x12 is not reloaded through this command, this is prevented by the slave hardware. The slave controller must be reset to reload the alias address.
        A EC_NOTIFY_EEPROM_OPERATION is given on completion or timeout. This function may be called from within the JobTask's context.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_EEPROM_OPERATION_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReloadSlaveEEPRomReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, gen_dwTimeout))
        return gen_dwRetVal

    def ResetSlaveController(self, bFixedAddressing, wSlaveAddress, dwTimeout): # ret: ECError
        """
        Reset ESC if it is capable of issuing a hardware reset.
        A special sequence of three independent and consecutive frames/commands has to be sent do the slave (Reset register ECAT 0x0040 or PDI 0x0041). Afterwards, the slave is reset.
        
        \note Check that the ESC supports resetting. The slave state should be in INIT when calling this function. The number of acylic frames per cycle must be at least 3, otherwise an error is returned.
        This function may not be called from within the JobTask's context.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            dwTimeout: Timeout [ms] The function will block at most for this time. The timeout value must not be set to EC_NOWAIT

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecResetSlaveController(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_dwTimeout))
        return gen_dwRetVal

    def AssignSlaveEEPRom(self, bFixedAddressing, wSlaveAddress, bSlavePDIAccessEnable, bForceAssign, dwTimeout): # ret: ECError
        """
        Set EEPROM Assignment to PDI or EtherCAT Master.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            bSlavePDIAccessEnable: EC_TRUE: EEPROM assigned to slave PDI application,
            bForceAssign: Force Assignment of EEPROM (only for ECat Master Assignment)
            dwTimeout: Timeout [ms] The function will block at most for this time. The timeout value must not be set to EC_NOWAIT.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_bSlavePDIAccessEnable = CEcWrapperTypes.Conv(bSlavePDIAccessEnable, "bool")
        gen_bForceAssign = CEcWrapperTypes.Conv(bForceAssign, "bool")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecAssignSlaveEEPRom(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_bSlavePDIAccessEnable, gen_bForceAssign, gen_dwTimeout))
        return gen_dwRetVal

    def AssignSlaveEEPRomReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, bSlavePDIAccessEnable, bForceAssign, dwTimeout): # ret: ECError
        """
        Requests EEPROM Assignment to PDI or EtherCAT Master operation and return immediately
        
        \note EC_NOTIFY_EEPROM_OPERATION is given on completion or timeout. This function may be called from within the JobTask's context.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_EEPROM_OPERATION_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            bSlavePDIAccessEnable: EC_TRUE: EEPROM assigned to slave PDI application, EC_FALSE: EEPROM assigned to Ecat
            bForceAssign: Force Assignment of EEPROM (only for ECat Master Assignment)
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_bSlavePDIAccessEnable = CEcWrapperTypes.Conv(bSlavePDIAccessEnable, "bool")
        gen_bForceAssign = CEcWrapperTypes.Conv(bForceAssign, "bool")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecAssignSlaveEEPRomReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, gen_bSlavePDIAccessEnable, gen_bForceAssign, gen_dwTimeout))
        return gen_dwRetVal

    def ActiveSlaveEEPRom(self, bFixedAddressing, wSlaveAddress, pbSlavePDIAccessActive, dwTimeout): # ret: ECError
        """
        Check whether EEPROM is marked access active by Slave PDI application.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            pbSlavePDIAccessActive: Pointer to Boolean value: EC_TRUE: EEPROM active by PDI application, EC_FALSE: EEPROM not active
            dwTimeout: Timeout [ms] The function will block at most for this time. The timeout value must not be set to EC_NOWAIT

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_pbSlavePDIAccessActive = CEcWrapperTypes.Conv(pbSlavePDIAccessActive, "bool")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecActiveSlaveEEPRom(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, ctypes.pointer(gen_pbSlavePDIAccessActive), gen_dwTimeout))
        return gen_dwRetVal

    def ActiveSlaveEEPRomReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, pbSlavePDIAccessActive, dwTimeout): # ret: ECError
        """
        Requests EEPROM is marked access active by Slave PDI application check and returns immediately.
        
        \note A EC_NOTIFY_EEPROM_OPERATION is given on completion or timeout. This function may be called from within the JobTask's context.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_EEPROM_OPERATION_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            pbSlavePDIAccessActive: Pointer to Boolean value: EC_TRUE: EEPROM active by PDI application, EC_FALSE: EEPROM not active. Must be valid until operation complete
            dwTimeout: Timeout [ms] The function will block at most for this time. The timeout value must not be set to EC_NOWAIT.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_pbSlavePDIAccessActive = CEcWrapperTypes.Conv(pbSlavePDIAccessActive, "bool")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecActiveSlaveEEPRomReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, ctypes.pointer(gen_pbSlavePDIAccessActive), gen_dwTimeout))
        return gen_dwRetVal

    def HCAcceptTopoChange(self): # ret: ECError
        """
        Accept last detected topology change manually after Hot Connect was configured in manual mode calling EC_IOCTL_HC_SETMODE
        
        \note If Hot connect is configured in manual mode, the master will generate the notifications EC_NOTIFY_HC_PROBEALLGROUPS or EC_NOTIFY_HC_DETECTADDGROUPS after a topology change was detected.
        The application can call ecatHCAcceptTopoChange() to accept this change. This will set all new detected slaves to the current master state.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecHCAcceptTopoChange(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def HCGetNumGroupMembers(self, dwGroupIndex): # ret: ECError
        """
        Get number of slaves belonging to a specific HotConnect group.

        Args:
            dwGroupIndex: Index of HotConnect group, 0 is the mandatory group

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwGroupIndex = CEcWrapperTypes.Conv(dwGroupIndex, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecHCGetNumGroupMembers(self.m_dwMasterInstanceId, gen_dwGroupIndex))
        return gen_dwRetVal

    def HCGetSlaveIdsOfGroup(self, dwGroupIndex, adwSlaveId, dwMaxNumSlaveIds): # ret: ECError
        """
        Return the list of ID referencing slaves belonging to a specific HotConnect group.

        Args:
            dwGroupIndex: Index of HotConnect group, 0 is the mandatory group
            adwSlaveId: DWORD array to carry slave ids of specified HotConncet group
            dwMaxNumSlaveIds: size of adwSlaveId array

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwGroupIndex = CEcWrapperTypes.Conv(dwGroupIndex, "uint")
        gen_adwSlaveId = CEcWrapperTypes.Conv(adwSlaveId, "uint")
        gen_dwMaxNumSlaveIds = CEcWrapperTypes.Conv(dwMaxNumSlaveIds, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecHCGetSlaveIdsOfGroup(self.m_dwMasterInstanceId, gen_dwGroupIndex, ctypes.pointer(gen_adwSlaveId), gen_dwMaxNumSlaveIds))
        return gen_dwRetVal

    def SetSlavePortState(self, dwSlaveId, wPort, bClose, bForce, dwTimeout): # ret: ECError
        """
        Open or close slave port
        
        \note This function can be called to re-open ports closed by a rescue scan.

        Args:
            dwSlaveId: Slave ID
            wPort: Port to open or close. Can be ESC_PORT_A, ESC_PORT_B, ESC_PORT_C, ESC_PORT_D
            bClose: EC_TRUE: close port, EC_FALSE: open port
            bForce: EC_TRUE: port will be closed or open, EC_FALSE: port will be set in AutoClose mode
            dwTimeout: Timeout [ms]

        Returns:
            - EC_E_NOERROR on success
            - EC_E_SLAVE_NOT_PRESENT if slave not present
            - EC_E_NOTFOUND if the slave with ID dwSlaveId does not exist
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_wPort = CEcWrapperTypes.Conv(wPort, "ushort")
        gen_bClose = CEcWrapperTypes.Conv(bClose, "bool")
        gen_bForce = CEcWrapperTypes.Conv(bForce, "bool")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetSlavePortState(self.m_dwMasterInstanceId, gen_dwSlaveId, gen_wPort, gen_bClose, gen_bForce, gen_dwTimeout))
        return gen_dwRetVal

    def SetSlavePortStateReq(self, dwClientId, dwTferId, dwSlaveId, wPort, bClose, bForce, dwTimeout): # ret: ECError
        """
        Requests Open or close slave port operation and returns immediately.
        
        \note A EC_T_PORT_OPERATION_NTFY_DESC is given on completion. This function can be called to re-open ports closed by a rescue scan.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_PORT_OPERATION_NTFY_DESC
            dwSlaveId: Slave ID
            wPort: Port to open or close. Can be ESC_PORT_A, ESC_PORT_B, ESC_PORT_C, ESC_PORT_D
            bClose: EC_TRUE: close port, EC_FALSE: open port
            bForce: EC_TRUE: port will be closed or open, EC_FALSE: port will be set in AutoClose mode
            dwTimeout: Timeout [ms]

        Returns:
            - EC_E_NOERROR on success
            - EC_E_SLAVE_NOT_PRESENT if slave not present
            - EC_E_NOTFOUND if the slave with ID dwSlaveId does not exist
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_wPort = CEcWrapperTypes.Conv(wPort, "ushort")
        gen_bClose = CEcWrapperTypes.Conv(bClose, "bool")
        gen_bForce = CEcWrapperTypes.Conv(bForce, "bool")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetSlavePortStateReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_dwSlaveId, gen_wPort, gen_bClose, gen_bForce, gen_dwTimeout))
        return gen_dwRetVal

    def SlaveSerializeMbxTfers(self, dwSlaveId): # ret: ECError
        """
        All mailbox transfers to the specified slave are serialized. The parallel (overlapped) usage of more than one protocol (CoE, EoE, FoE, etc.) will be disabled.
        
        \note By default parallel mailbox transfers are enabled.

        Args:
            dwSlaveId: Slave ID

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_INVALIDPARM if master is not initialized
            - EC_E_NOTFOUND if the slave with given ID does not exist
            - EC_E_NO_MBX_SUPPORT if slave does not support mailbox transfers
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSlaveSerializeMbxTfers(self.m_dwMasterInstanceId, gen_dwSlaveId))
        return gen_dwRetVal

    def SlaveParallelMbxTfers(self, dwSlaveId): # ret: ECError
        """
        Reenable the parallel (overlapped) usage of more than one protocol (CoE, EoE, FoE, etc.).
        
        \note By default parallel mailbox transfers are enabled.

        Args:
            dwSlaveId: Slave ID

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_INVALIDPARM if master is not initialized
            - EC_E_NOTFOUND if the slave with given ID does not exist
            - EC_E_NO_MBX_SUPPORT if slave does not support mailbox transfers
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSlaveParallelMbxTfers(self.m_dwMasterInstanceId, gen_dwSlaveId))
        return gen_dwRetVal

    def DcEnable(self): # ret: ECError
        """
        Enable DC Support

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcEnable(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def DcDisable(self): # ret: ECError
        """
        Disable DC Support

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcDisable(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def DcIsEnabled(self, pbDcIsEnabled): # ret: ECError
        """
        This function checks if DC is enabled and used.
        
        \note This function can be called at any time after applying the configuration.

        Args:
            pbDcIsEnabled: EC_TRUE if DC is enabled

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pbDcIsEnabled = CEcWrapperTypes.Conv(pbDcIsEnabled, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcIsEnabled(self.m_dwMasterInstanceId, ctypes.pointer(gen_pbDcIsEnabled)))
        return gen_dwRetVal

    def DcConfigure(self, pDcConfigure): # ret: ECError
        """
        Configure the distributed clocks.
        - Set the DC synchronization settling time ([ms]).
        - Set the DC slave limit for the wire or'ed clock deviation value. This value determines whether the slave clocks are synchronized or not.
        - Configure the ARMW burst frames to compensate the static deviations of the clock speeds.
        
        \note This function can be called at any time after applying the configuration.

        Args:
            pDcConfigure: Configuration parameter a pointer to a structure of type EC_T_DC_CONFIGURE.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pDcConfigure = CEcWrapperTypes.Conv(pDcConfigure, "EC_T_DC_CONFIGURE")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcConfigure(self.m_dwMasterInstanceId, gen_pDcConfigure))
        return gen_dwRetVal

    def DcContDelayCompEnable(self): # ret: ECError
        """
        Enable the continuous propagation delay compensation.
        Calling this function generate a propagation delay measurement every 30s. The result of the measurement is used to correct the propagation delay values on the bus.
        
        \note This function can be called at any time after applying the configuration.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcContDelayCompEnable(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def DcContDelayCompDisable(self): # ret: ECError
        """
        Disable the continuous propagation delay compensation.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcContDelayCompDisable(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def DcmConfigure(self, pDcmConfig, dwInSyncTimeout): # ret: ECError
        """
        Configure DC master synchonization

        Args:
            pDcmConfig: Configuration information, a pointer to a structure of type EC_T_DCM_CONFIG.
            dwInSyncTimeout: Currently not implemented.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pDcmConfig = CEcWrapperTypes.Conv(pDcmConfig, "EC_T_DCM_CONFIG")
        gen_dwInSyncTimeout = CEcWrapperTypes.Conv(dwInSyncTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcmConfigure(self.m_dwMasterInstanceId, ctypes.pointer(gen_pDcmConfig), gen_dwInSyncTimeout))
        return gen_dwRetVal

    def DcmGetStatus(self, pdwErrorCode, pnDiffCur, pnDiffAvg, pnDiffMax): # ret: ECError
        """
        Get DC master synchonization controller status.

        Args:
            pdwErrorCode: Pointer to current error code of the DCM controller (see below).
            pnDiffCur: Pointer to current difference between set value and actual value of controller in nanosec.
            pnDiffAvg: Pointer to average difference between set value and actual value of controller in nanosec
            pnDiffMax: Pointer to maximum difference between set value and actual value of controller in nanosec

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_NOTREADY DCM control loop is not running
            - EC_E_BUSY DCM control loop is running and try to get InSync
            - DCM_E_MAX_CTL_ERROR_EXCEED Set if the controller error exceeds the InSyncLimit
            - DCM_E_DRIFT_TO_HIGH DCM control loop not able to compensate drift. Drift above 600ppm.
        """
        gen_pdwErrorCode = CEcWrapperTypes.Conv(pdwErrorCode, "uint")
        gen_pnDiffCur = CEcWrapperTypes.Conv(pnDiffCur, "int")
        gen_pnDiffAvg = CEcWrapperTypes.Conv(pnDiffAvg, "int")
        gen_pnDiffMax = CEcWrapperTypes.Conv(pnDiffMax, "int")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcmGetStatus(self.m_dwMasterInstanceId, ctypes.pointer(gen_pdwErrorCode), ctypes.pointer(gen_pnDiffCur), ctypes.pointer(gen_pnDiffAvg), ctypes.pointer(gen_pnDiffMax)))
        return gen_dwRetVal

    def DcxGetStatus(self, pdwErrorCode, pnDiffCur, pnDiffAvg, pnDiffMax, pnTimeStampDiff): # ret: ECError
        """
        Get DC master external synchonization controller status.

        Args:
            pdwErrorCode: DCX controller error code
            pnDiffCur: Current difference between set value and actual value of controller in nanosec.
            pnDiffAvg: Average difference between set value and actual value of controller in nanosec.
            pnDiffMax: Maximum difference between set value and actual value of controller in nanosec.
            pnTimeStampDiff: Difference between external and internal timestamp

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pdwErrorCode = CEcWrapperTypes.Conv(pdwErrorCode, "uint")
        gen_pnDiffCur = CEcWrapperTypes.Conv(pnDiffCur, "int")
        gen_pnDiffAvg = CEcWrapperTypes.Conv(pnDiffAvg, "int")
        gen_pnDiffMax = CEcWrapperTypes.Conv(pnDiffMax, "int")
        gen_pnTimeStampDiff = CEcWrapperTypes.Conv(pnTimeStampDiff, "Int64")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcxGetStatus(self.m_dwMasterInstanceId, ctypes.pointer(gen_pdwErrorCode), ctypes.pointer(gen_pnDiffCur), ctypes.pointer(gen_pnDiffAvg), ctypes.pointer(gen_pnDiffMax), ctypes.pointer(gen_pnTimeStampDiff)))
        return gen_dwRetVal

    def DcmResetStatus(self): # ret: ECError
        """
        Reset DC master synchonization controller status, average and maximum difference between set value and actual value

        Args:

        Returns:
            EEC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcmResetStatus(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def DcmGetBusShiftConfigured(self, pbBusShiftConfigured): # ret: ECError
        """
        Check if DCM Bus Shift is configured/possible in configuration (ENI file)

        Args:
            pbBusShiftConfigured: EC_TRUE if DCM bus shift mode is supported by the current configuration

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pbBusShiftConfigured = CEcWrapperTypes.Conv(pbBusShiftConfigured, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcmGetBusShiftConfigured(self.m_dwMasterInstanceId, ctypes.pointer(gen_pbBusShiftConfigured)))
        return gen_dwRetVal

    def DcmShowStatus(self): # ret: ECError
        """
        Show DC master synchronization status as DbgMsg (for development purposes only).

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcmShowStatus(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def DcmGetAdjust(self, pnAdjustPermil): # ret: ECError
        """
        Returns the current adjustment value for the timer. bCtlOff must be set to EC_TRUE to enable external adjustment.

        Args:
            pnAdjustPermil: Current adjustment value of the timer.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pnAdjustPermil = CEcWrapperTypes.Conv(pnAdjustPermil, "int")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecDcmGetAdjust(self.m_dwMasterInstanceId, ctypes.pointer(gen_pnAdjustPermil)))
        return gen_dwRetVal

    def GetSlaveInfo(self, bFixedAddressing, wSlaveAddress, out_pGetSlaveInfo): # ret: ECError
        """
        Get Slave Info
        
        \deprecated Use emGetCfgSlaveInfo or emGetBusSlaveInfo instead

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            pGetSlaveInfo: Slave information

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        pGetSlaveInfo = DN_EC_T_GET_SLAVE_INFO()
        gen_pGetSlaveInfo = CEcWrapperTypes.Conv(pGetSlaveInfo, "EC_T_GET_SLAVE_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveInfo(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, ctypes.pointer(gen_pGetSlaveInfo)))
        out_pGetSlaveInfo.value = CEcWrapperTypes.Conv(gen_pGetSlaveInfo, "DN_EC_T_GET_SLAVE_INFO")
        return gen_dwRetVal

    def GetCfgSlaveInfo(self, bStationAddress, wSlaveAddress, out_pSlaveInfo): # ret: ECError
        """
        Return information about a configured slave from the ENI file

        Args:
            bStationAddress: 
            wSlaveAddress: Slave address according bFixedAddressing
            pSlaveInfo: Information about the slave.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bStationAddress = CEcWrapperTypes.Conv(bStationAddress, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        pSlaveInfo = DN_EC_T_CFG_SLAVE_INFO()
        gen_pSlaveInfo = CEcWrapperTypes.Conv(pSlaveInfo, "EC_T_CFG_SLAVE_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetCfgSlaveInfo(self.m_dwMasterInstanceId, gen_bStationAddress, gen_wSlaveAddress, ctypes.pointer(gen_pSlaveInfo)))
        out_pSlaveInfo.value = CEcWrapperTypes.Conv(gen_pSlaveInfo, "DN_EC_T_CFG_SLAVE_INFO")
        return gen_dwRetVal

    def GetCfgSlaveEoeInfo(self, bStationAddress, wSlaveAddress, pSlaveEoeInfo): # ret: ECError
        """
        Return EoE information about a configured slave from the ENI file

        Args:
            bStationAddress: 
            wSlaveAddress: Slave address according bFixedAddressing
            pSlaveEoeInfo: Information about the slave

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_NOTFOUND if the slave with the given address does not exist
            - EC_E_NO_MBX_SUPPORT if the slave does not support mailbox communication
            - EC_E_NO_EOE_SUPPORT if the slave supports mailbox communication, but not EoE
        """
        gen_bStationAddress = CEcWrapperTypes.Conv(bStationAddress, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_pSlaveEoeInfo = CEcWrapperTypes.Conv(pSlaveEoeInfo, "EC_T_CFG_SLAVE_EOE_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetCfgSlaveEoeInfo(self.m_dwMasterInstanceId, gen_bStationAddress, gen_wSlaveAddress, gen_pSlaveEoeInfo))
        return gen_dwRetVal

    def GetBusSlaveInfo(self, bStationAddress, wSlaveAddress, out_pSlaveInfo): # ret: ECError
        """
        Return information about a slave connected to the EtherCAT bus

        Args:
            bStationAddress: 
            wSlaveAddress: Slave address according bFixedAddressing
            pSlaveInfo: Information from the slave.

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_NOTFOUND if the slave with the given address does not exist
        """
        gen_bStationAddress = CEcWrapperTypes.Conv(bStationAddress, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        pSlaveInfo = DN_EC_T_BUS_SLAVE_INFO()
        gen_pSlaveInfo = CEcWrapperTypes.Conv(pSlaveInfo, "EC_T_BUS_SLAVE_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetBusSlaveInfo(self.m_dwMasterInstanceId, gen_bStationAddress, gen_wSlaveAddress, ctypes.pointer(gen_pSlaveInfo)))
        out_pSlaveInfo.value = CEcWrapperTypes.Conv(gen_pSlaveInfo, "DN_EC_T_BUS_SLAVE_INFO")
        return gen_dwRetVal

    def GetSlaveInpVarInfoNumOf(self, bFixedAddressing, wSlaveAddress, out_pwSlaveInpVarInfoNumOf): # ret: ECError
        """
        Gets the number of input variables of a specific slave.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            pwSlaveInpVarInfoNumOf: Number of found process variable entries

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        pwSlaveInpVarInfoNumOf = 0
        gen_pwSlaveInpVarInfoNumOf = CEcWrapperTypes.Conv(pwSlaveInpVarInfoNumOf, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveInpVarInfoNumOf(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, ctypes.pointer(gen_pwSlaveInpVarInfoNumOf)))
        out_pwSlaveInpVarInfoNumOf.value = CEcWrapperTypes.Conv(gen_pwSlaveInpVarInfoNumOf, "ushort")
        return gen_dwRetVal

    def GetSlaveOutpVarInfoNumOf(self, bFixedAddressing, wSlaveAddress, out_pwSlaveOutpVarInfoNumOf): # ret: ECError
        """
        Gets the number of output variables of a specific slave.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            pwSlaveOutpVarInfoNumOf: Number of found process variables

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        pwSlaveOutpVarInfoNumOf = 0
        gen_pwSlaveOutpVarInfoNumOf = CEcWrapperTypes.Conv(pwSlaveOutpVarInfoNumOf, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveOutpVarInfoNumOf(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, ctypes.pointer(gen_pwSlaveOutpVarInfoNumOf)))
        out_pwSlaveOutpVarInfoNumOf.value = CEcWrapperTypes.Conv(gen_pwSlaveOutpVarInfoNumOf, "ushort")
        return gen_dwRetVal

    def GetSlaveOutpVarByObjectEx(self, bFixedAddressing, wSlaveAddress, wIndex, wSubIndex, pProcessVarInfoEntry): # ret: ECError
        """
        Gets the input process variable extended information entry by object index, subindex of a specific slave.
        
        \note See EC_T_PROCESS_VAR_INFO_EX.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wIndex: Object index
            wSubIndex: Object sub index
            pProcessVarInfoEntry: Process variable extended information entry

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wIndex = CEcWrapperTypes.Conv(wIndex, "ushort")
        gen_wSubIndex = CEcWrapperTypes.Conv(wSubIndex, "ushort")
        gen_pProcessVarInfoEntry = CEcWrapperTypes.Conv(pProcessVarInfoEntry, "EC_T_PROCESS_VAR_INFO_EX")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveOutpVarByObjectEx(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wIndex, gen_wSubIndex, gen_pProcessVarInfoEntry))
        return gen_dwRetVal

    def GetSlaveInpVarByObjectEx(self, bFixedAddressing, wSlaveAddress, wIndex, wSubIndex, pProcessVarInfoEntry): # ret: ECError
        """
        Gets the input process variable extended information entry by object index, subindex of a specific slave.
        
        \note See EC_T_PROCESS_VAR_INFO_EX.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wIndex: Object index
            wSubIndex: Object sub index
            pProcessVarInfoEntry: Process variable extended information entry

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wIndex = CEcWrapperTypes.Conv(wIndex, "ushort")
        gen_wSubIndex = CEcWrapperTypes.Conv(wSubIndex, "ushort")
        gen_pProcessVarInfoEntry = CEcWrapperTypes.Conv(pProcessVarInfoEntry, "EC_T_PROCESS_VAR_INFO_EX")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveInpVarByObjectEx(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wIndex, gen_wSubIndex, gen_pProcessVarInfoEntry))
        return gen_dwRetVal

    def FindOutpVarByName(self, szVariableName, out_pSlaveOutpVarInfo): # ret: ECError
        """
        Finds an output process variable information entry by the variable name.
        
        \note See EC_T_PROCESS_VAR_INFO.

        Args:
            szVariableName: Variable name
            pSlaveOutpVarInfo: 

        Returns:
            EC_E_NOERROR or error code
        """
        gen_szVariableName = CEcWrapperTypes.Conv(szVariableName, "string")
        pSlaveOutpVarInfo = DN_EC_T_PROCESS_VAR_INFO()
        gen_pSlaveOutpVarInfo = CEcWrapperTypes.Conv(pSlaveOutpVarInfo, "EC_T_PROCESS_VAR_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecFindOutpVarByName(self.m_dwMasterInstanceId, gen_szVariableName, ctypes.pointer(gen_pSlaveOutpVarInfo)))
        out_pSlaveOutpVarInfo.value = CEcWrapperTypes.Conv(gen_pSlaveOutpVarInfo, "DN_EC_T_PROCESS_VAR_INFO")
        return gen_dwRetVal

    def FindOutpVarByNameEx(self, szVariableName, pProcessVarInfoEntry): # ret: ECError
        """
        Finds an output process variable extended information entry by the variable name.
        
        \note See EC_T_PROCESS_VAR_INFO_EX.

        Args:
            szVariableName: Variable name
            pProcessVarInfoEntry: Process variable extended information entry

        Returns:
            EC_E_NOERROR or error code
        """
        gen_szVariableName = CEcWrapperTypes.Conv(szVariableName, "string")
        gen_pProcessVarInfoEntry = CEcWrapperTypes.Conv(pProcessVarInfoEntry, "EC_T_PROCESS_VAR_INFO_EX")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecFindOutpVarByNameEx(self.m_dwMasterInstanceId, gen_szVariableName, gen_pProcessVarInfoEntry))
        return gen_dwRetVal

    def FindInpVarByName(self, szVariableName, pProcessVarInfoEntry): # ret: ECError
        """
        Finds an input process variable information entry by the variable name.
        
        \note See EC_T_PROCESS_VAR_INFO.

        Args:
            szVariableName: Variable name
            pProcessVarInfoEntry: Process variable information entry

        Returns:
            EC_E_NOERROR or error code
        """
        gen_szVariableName = CEcWrapperTypes.Conv(szVariableName, "string")
        gen_pProcessVarInfoEntry = CEcWrapperTypes.Conv(pProcessVarInfoEntry, "EC_T_PROCESS_VAR_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecFindInpVarByName(self.m_dwMasterInstanceId, gen_szVariableName, gen_pProcessVarInfoEntry))
        return gen_dwRetVal

    def FindInpVarByNameEx(self, szVariableName, pProcessVarInfoEntry): # ret: ECError
        """
        Finds an input process variable extended information entry by the variable name.
        
        \note See EC_T_PROCESS_VAR_INFO_EX.

        Args:
            szVariableName: Variable name
            pProcessVarInfoEntry: Process variable extended information entry

        Returns:
            EC_E_NOERROR or error code
        """
        gen_szVariableName = CEcWrapperTypes.Conv(szVariableName, "string")
        gen_pProcessVarInfoEntry = CEcWrapperTypes.Conv(pProcessVarInfoEntry, "EC_T_PROCESS_VAR_INFO_EX")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecFindInpVarByNameEx(self.m_dwMasterInstanceId, gen_szVariableName, gen_pProcessVarInfoEntry))
        return gen_dwRetVal

    def EthDbgMsg(self, byEthTypeByte0, byEthTypeByte1, szMsg): # ret: ECError
        """
        Send a debug message to the EtherCAT Link Layer. This feature can be used for debugging purposes.

        Args:
            byEthTypeByte0: Ethernet type byte 0
            byEthTypeByte1: Ethernet type byte 1
            szMsg: Message to send to link layer

        Returns:
            EC_E_NOERROR or error code
        """
        gen_byEthTypeByte0 = CEcWrapperTypes.Conv(byEthTypeByte0, "byte")
        gen_byEthTypeByte1 = CEcWrapperTypes.Conv(byEthTypeByte1, "byte")
        gen_szMsg = CEcWrapperTypes.Conv(szMsg, "string")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecEthDbgMsg(self.m_dwMasterInstanceId, gen_byEthTypeByte0, gen_byEthTypeByte1, gen_szMsg))
        return gen_dwRetVal

    def BlockNode(self, pMisMatch, dwTimeout): # ret: ECError
        """
        If an invalid slave node is connected, which happens bus topology scan to fail, the previous port, where this node is connected to can be shut down with this call. This allows a HotConnect system to be not disturbed, if unknown nodes are connected.
        If this function will be executed on a HotConnect member (a slave which is part of a hot connect group) the complete hot connect group will be excluded from the bus.
        
        \note This function may only be called from within the JobTask's context with parameter dwTimeout set to EC_NOWAIT.

        Args:
            pMisMatch: Pointer to EC_T_SB_MISMATCH_DESC carrying mismatch descriptor.H
            dwTimeout: Timeout [ms]. The function will block at most for this time.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pMisMatch = CEcWrapperTypes.Conv(pMisMatch, "EC_T_SB_MISMATCH_DESC")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecBlockNode(self.m_dwMasterInstanceId, gen_pMisMatch, gen_dwTimeout))
        return gen_dwRetVal

    def OpenBlockedPorts(self, dwTimeout): # ret: ECError
        """
        If an invalid node is blocked out by call to ecatBlockNode this call allows re-opening all blocked ports to check whether mismatch cause is removed from bus.
        
        \note This function may only be called from within the JobTask's context with parameter dwTimeout set to EC_NOWAIT.

        Args:
            dwTimeout: Timeout [ms]. The function will block at most for this time.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecOpenBlockedPorts(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def ForceTopologyChange(self): # ret: ECError
        """
        Force changed topology (trigger HC State Machine).

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecForceTopologyChange(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def IsTopologyChangeDetected(self, pbTopologyChangeDetected): # ret: ECError
        """
        Returns whether topology change detected.

        Args:
            pbTopologyChangeDetected: Pointer to Bool value: EC_TRUE if Topology Change Detected, EC_FALSE if not.

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_INVALIDSTATE if the master is not initialized
        """
        gen_pbTopologyChangeDetected = CEcWrapperTypes.Conv(pbTopologyChangeDetected, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecIsTopologyChangeDetected(self.m_dwMasterInstanceId, ctypes.pointer(gen_pbTopologyChangeDetected)))
        return gen_dwRetVal

    def IsTopologyKnown(self, out_pbTopologyKnown): # ret: ECError
        """
        Returns whether topology known

        Args:
            pbTopologyKnown: Topology known

        Returns:
            EC_E_NOERROR or error code
        """
        pbTopologyKnown = False
        gen_pbTopologyKnown = CEcWrapperTypes.Conv(pbTopologyKnown, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecIsTopologyKnown(self.m_dwMasterInstanceId, ctypes.pointer(gen_pbTopologyKnown)))
        out_pbTopologyKnown.value = CEcWrapperTypes.Conv(gen_pbTopologyKnown, "bool")
        return gen_dwRetVal

    def GetBusTime(self, out_pqwBusTime): # ret: ECError
        """
        This function returns the actual bus time in nano seconds.

        Args:
            pqwBusTime: Bus time [ns]

        Returns:
            EC_E_NOERROR or error code
        """
        pqwBusTime = 0
        gen_pqwBusTime = CEcWrapperTypes.Conv(pqwBusTime, "UInt64")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetBusTime(self.m_dwMasterInstanceId, ctypes.pointer(gen_pqwBusTime)))
        out_pqwBusTime.value = CEcWrapperTypes.Conv(gen_pqwBusTime, "uint64")
        return gen_dwRetVal

    def IsSlavePresent(self, dwSlaveId, out_pbPresence): # ret: ECError
        """
        Returns whether a specific slave is currently connected to the Bus. This function may be called from within the JobTask. Since Slave Id is a parameter, valid response only can be retrieved after calling ecatConfigureMaster.

        Args:
            dwSlaveId: Slave ID
            pbPresence: EC_TRUE if slave is currently connected to the bus, EC_FALSE if not.

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_INVALIDSTATE if the master is not initialized
            - EC_E_NOTFOUND if the slave with ID dwSlaveId does not exist or no ENI File was loaded
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        pbPresence = False
        gen_pbPresence = CEcWrapperTypes.Conv(pbPresence, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecIsSlavePresent(self.m_dwMasterInstanceId, gen_dwSlaveId, ctypes.pointer(gen_pbPresence)))
        out_pbPresence.value = CEcWrapperTypes.Conv(gen_pbPresence, "bool")
        return gen_dwRetVal

    def PassThroughSrvGetStatus(self): # ret: DN_EC_PTS_STATE
        """
        Gets the status of the Pass-through server.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = DN_EC_PTS_STATE(CEcWrapperTypes.ConvRes(CEcWrapper.Get().ecPassThroughSrvGetStatus(self.m_dwMasterInstanceId)))
        return gen_dwRetVal

    def PassThroughSrvStart(self, poPtsStartParams, dwTimeout): # ret: ECError
        """
        Starts the Pass Through Server

        Args:
            poPtsStartParams: Pass through server start parameter
            dwTimeout: Timeout

        Returns:
            EC_E_NOERROR or error code
        """
        gen_poPtsStartParams = CEcWrapperTypes.Conv(poPtsStartParams, "EC_T_PTS_SRV_START_PARMS")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecPassThroughSrvStart(self.m_dwMasterInstanceId, gen_poPtsStartParams, gen_dwTimeout))
        return gen_dwRetVal

    def PassThroughSrvStop(self, dwTimeout): # ret: ECError
        """
        Stops the Pass Through Server

        Args:
            dwTimeout: Timeout

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecPassThroughSrvStop(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def PassThroughSrvEnable(self, dwTimeout): # ret: ECError
        """
        Enables the Pass-through server.

        Args:
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecPassThroughSrvEnable(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def PassThroughSrvDisable(self, dwTimeout): # ret: ECError
        """
        Disables the Pass-through server.

        Args:
            dwTimeout: Timeout [ms]

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecPassThroughSrvDisable(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def AdsAdapterStart(self, poStartParams, dwTimeout): # ret: ECError
        """
        Starts the Ads Pass Through Server

        Args:
            poStartParams: Pass through server start parameter
            dwTimeout: Timeout

        Returns:
            EC_E_NOERROR or error code
        """
        gen_poStartParams = CEcWrapperTypes.Conv(poStartParams, "EC_T_ADS_ADAPTER_START_PARMS")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecAdsAdapterStart(self.m_dwMasterInstanceId, gen_poStartParams, gen_dwTimeout))
        return gen_dwRetVal

    def AdsAdapterStop(self, dwTimeout): # ret: ECError
        """
        Stops the Ads Pass Through Server

        Args:
            dwTimeout: Timeout

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecAdsAdapterStop(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    def GetSrcMacAddress(self, out_pMacSrc): # ret: ECError
        """
        Gets the source MAC address

        Args:
            pMacSrc: 6-byte buffer to write source MAC address to.

        Returns:
            EC_E_NOERROR or error code
        """
        pMacSrc = DN_ETHERNET_ADDRESS()
        gen_pMacSrc = CEcWrapperTypes.Conv(pMacSrc, "ETHERNET_ADDRESS")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSrcMacAddress(self.m_dwMasterInstanceId, ctypes.pointer(gen_pMacSrc)))
        out_pMacSrc.value = CEcWrapperTypes.Conv(gen_pMacSrc, "DN_ETHERNET_ADDRESS")
        return gen_dwRetVal

    def SetLicenseKey(self, pszLicenseKey): # ret: ECError
        """
        Sets the license key for the protected version of EC-Master.
        
        \note Must be called after initialization and before configuration. This function may not be called if a non protected version is used.

        Args:
            pszLicenseKey: License key as zero terminated string with 26 characters.

        Returns:
            - EC_E_NOERROR or error code
            - EC_E_INVALIDSIZE the format of the license key is wrong. The correct length is 26 characters
            - EC_E_LICENSE_MISSING the license key doesn't match to the MAC Address
        """
        gen_pszLicenseKey = CEcWrapperTypes.Conv(pszLicenseKey, "string")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetLicenseKey(self.m_dwMasterInstanceId, gen_pszLicenseKey))
        return gen_dwRetVal

    def GetVersion(self, out_pdwVersion): # ret: ECError
        """
        Gets the version number as a 32-bit value

        Args:
            pdwVersion: Pointer to EC_T_DWORD to carry out version number

        Returns:
            - EC_E_NOERROR
            - EC_E_INVALIDPARM
        """
        pdwVersion = 0
        gen_pdwVersion = CEcWrapperTypes.Conv(pdwVersion, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetVersion(self.m_dwMasterInstanceId, ctypes.pointer(gen_pdwVersion)))
        out_pdwVersion.value = CEcWrapperTypes.Conv(gen_pdwVersion, "uint")
        return gen_dwRetVal

    def TraceDataConfig(self, wTraceDataSize): # ret: ECError
        """
        

        Args:
            wTraceDataSize: 

        Returns:
            
        """
        gen_wTraceDataSize = CEcWrapperTypes.Conv(wTraceDataSize, "ushort")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecTraceDataConfig(self.m_dwMasterInstanceId, gen_wTraceDataSize))
        return gen_dwRetVal

    def TraceDataGetInfo(self, pTraceDataInfo): # ret: ECError
        """
        

        Args:
            pTraceDataInfo: 

        Returns:
            
        """
        gen_pTraceDataInfo = CEcWrapperTypes.Conv(pTraceDataInfo, "EC_T_TRACE_DATA_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecTraceDataGetInfo(self.m_dwMasterInstanceId, gen_pTraceDataInfo))
        return gen_dwRetVal

    def FastModeInit(self): # ret: ECError
        """
        

        Args:

        Returns:
            
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecFastModeInit(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def FastSendAllCycFrames(self): # ret: ECError
        """
        

        Args:

        Returns:
            
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecFastSendAllCycFrames(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def FastProcessAllRxFrames(self, pbAreAllCycFramesProcessed): # ret: ECError
        """
        

        Args:
            pbAreAllCycFramesProcessed: 

        Returns:
            
        """
        gen_pbAreAllCycFramesProcessed = CEcWrapperTypes.Conv(pbAreAllCycFramesProcessed, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecFastProcessAllRxFrames(self.m_dwMasterInstanceId, ctypes.pointer(gen_pbAreAllCycFramesProcessed)))
        return gen_dwRetVal

    def ReadSlaveIdentification(self, bFixedAddressing, wSlaveAddress, wAdo, pwValue, dwTimeout): # ret: ECError
        """
        Read identification value from slave.
        
        \note This function may not be called from within the JobTask's context.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wAdo: ADO used for identification command
            pwValue: Pointer to Word value containing the Identification value
            dwTimeout: Timeout [ms]

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_SLAVE_NOT_PRESENT if slave not present
            - EC_E_BUSY another transfer request is already pending
            - EC_E_NOTFOUND if the slave with the given address does not exist
            - EC_E_NOTREADY if the working counter was not set when sending the command (slave may not be connected or did not respond)
            - EC_E_TIMEOUT if the slave did not respond to the command
            - EC_E_BUSY if the master or the corresponding slave is currently changing its operational state
            - EC_E_INVALIDPARM if the command is not supported or the timeout value is set to EC_NOWAIT
            - EC_E_ADO_NOT_SUPPORTED if the slave does not support requesting ID mechanism
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wAdo = CEcWrapperTypes.Conv(wAdo, "ushort")
        gen_pwValue = CEcWrapperTypes.Conv(pwValue, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReadSlaveIdentification(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wAdo, ctypes.pointer(gen_pwValue), gen_dwTimeout))
        return gen_dwRetVal

    def ReadSlaveIdentificationReq(self, dwClientId, dwTferId, bFixedAddressing, wSlaveAddress, wAdo, pwValue, dwTimeout): # ret: ECError
        """
        Request the identification value from a slave and returns immediately.
        
        \note This function may be called from within the JobTask's context.
        A notification EC_NOTIFY_SLAVE_IDENTIFICATION is given on completion or timeout.

        Args:
            dwClientId: Client ID returned by RegisterClient (0 if all registered clients shall be notified).
            dwTferId: Transfer ID. The application can set this ID to identify the transfer. It will be passed back to the application within EC_T_SLAVE_IDENTIFICATION_NTFY_DESC
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            wAdo: ADO used for identification command
            pwValue: Pointer to Word value containing the Identification value, must be valid until the request complete.
            dwTimeout: Timeout [ms]

        Returns:
            - EC_E_NOERROR if successful
            - EC_E_SLAVE_NOT_PRESENT if slave not present
            - EC_E_NOTFOUND if the slave with the given address does not exist
            - EC_E_INVALIDPARM if the command is not supported or the timeout value is set to EC_NOWAIT
            - EC_E_ADO_NOT_SUPPORTED if the slave does not support requesting ID mechanism
        """
        gen_dwClientId = CEcWrapperTypes.Conv(dwClientId, "uint")
        gen_dwTferId = CEcWrapperTypes.Conv(dwTferId, "uint")
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_wAdo = CEcWrapperTypes.Conv(wAdo, "ushort")
        gen_pwValue = CEcWrapperTypes.Conv(pwValue, "ushort")
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecReadSlaveIdentificationReq(self.m_dwMasterInstanceId, gen_dwClientId, gen_dwTferId, gen_bFixedAddressing, gen_wSlaveAddress, gen_wAdo, ctypes.pointer(gen_pwValue), gen_dwTimeout))
        return gen_dwRetVal

    def SetSlaveDisabled(self, bFixedAddressing, wSlaveAddress, bDisabled): # ret: ECError
        """
        Enable or disable a specific slave
        
        \note The EtherCAT state of disabled slaves can not be set higher than PREOP. If the state is higher than PREOP at the time this function is called. The state will be automatically change to PREOP. The information about the last requested state is lost and is set to PREOP too.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            bDisabled: EC_TRUE: Disable slave, EC_FALSE: Enable slave

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_bDisabled = CEcWrapperTypes.Conv(bDisabled, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetSlaveDisabled(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_bDisabled))
        return gen_dwRetVal

    def SetSlavesDisabled(self, bFixedAddressing, wSlaveAddress, eSlaveSelection, bDisabled): # ret: ECError
        """
        Enable or disable a specific group of slaves
        
        \note The EtherCAT state of disabled slaves can not be set higher than PREOP. If the state is higher than PREOP at the time this function is called. The state will be automatically change to PREOP. The information about the last requested state is lost and is set to PREOP too.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            eSlaveSelection: Slave selection criteria for following slaves
            bDisabled: EC_TRUE: Disable slaves, EC_FALSE: Enable slaves.

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_eSlaveSelection = CEcWrapperTypes.Conv(eSlaveSelection, "EC_T_SLAVE_SELECTION")
        gen_bDisabled = CEcWrapperTypes.Conv(bDisabled, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetSlavesDisabled(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_eSlaveSelection, gen_bDisabled))
        return gen_dwRetVal

    def SetSlaveDisconnected(self, bFixedAddressing, wSlaveAddress, bDisconnected): # ret: ECError
        """
        Mark specific slave for connection or disconnection
        
        \note The EtherCAT state of disconnected slaves can not be set higher than INIT. If the state is higher than INIT at the time this function is called. The state will be automatically change to INIT. The information about the last requested state is lost and is set to INIT too.

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            bDisconnected: EC_TRUE: Mark slave for disconnection, EC_FALSE: Mark slave for (re-)connection

        Returns:
            EC_E_NOERROR or error code
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_bDisconnected = CEcWrapperTypes.Conv(bDisconnected, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetSlaveDisconnected(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_bDisconnected))
        return gen_dwRetVal

    def SetSlavesDisconnected(self, bFixedAddressing, wSlaveAddress, eSlaveSelection, bDisconnected): # ret: ECError
        """
        Mark a specific group of slaves  for connection or disconnection

        Args:
            bFixedAddressing: EC_TRUE: use station address, EC_FALSE: use AutoInc address
            wSlaveAddress: Slave address according bFixedAddressing
            eSlaveSelection: Slave selection criteria
            bDisconnected: EC_TRUE: mark slaves for disconnection, EC_FALSE: mark slaves for connection

        Returns:
            - EC_E_NOERROR or error code
            - EC_E_NOTFOUND if the slave does not exist
        """
        gen_bFixedAddressing = CEcWrapperTypes.Conv(bFixedAddressing, "bool")
        gen_wSlaveAddress = CEcWrapperTypes.Conv(wSlaveAddress, "ushort")
        gen_eSlaveSelection = CEcWrapperTypes.Conv(eSlaveSelection, "EC_T_SLAVE_SELECTION")
        gen_bDisconnected = CEcWrapperTypes.Conv(bDisconnected, "bool")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecSetSlavesDisconnected(self.m_dwMasterInstanceId, gen_bFixedAddressing, gen_wSlaveAddress, gen_eSlaveSelection, gen_bDisconnected))
        return gen_dwRetVal

    def GetMemoryUsage(self, pdwCurrentUsage, pdwMaxUsage): # ret: ECError
        """
        Returns information about memory usage. All calls to malloc/free and new/delete are monitored.

        Args:
            pdwCurrentUsage: Current memory usage in Bytes at the time where this function is called
            pdwMaxUsage: Maximum memory usage in Bytes since initialization at the time where this function is called

        Returns:
            EC_E_NOERROR or error code
        """
        gen_pdwCurrentUsage = CEcWrapperTypes.Conv(pdwCurrentUsage, "uint")
        gen_pdwMaxUsage = CEcWrapperTypes.Conv(pdwMaxUsage, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetMemoryUsage(self.m_dwMasterInstanceId, ctypes.pointer(gen_pdwCurrentUsage), ctypes.pointer(gen_pdwMaxUsage)))
        return gen_dwRetVal

    def GetSlaveStatistics(self, dwSlaveId, pSlaveStatisticsDesc): # ret: ECError
        """
        Get Slave's statistics counter.

        Args:
            dwSlaveId: Slave id
            pSlaveStatisticsDesc: Pointer to struct EC_T_SLVSTATISTICS_DESC

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_pSlaveStatisticsDesc = CEcWrapperTypes.Conv(pSlaveStatisticsDesc, "EC_T_SLVSTATISTICS_DESC")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetSlaveStatistics(self.m_dwMasterInstanceId, gen_dwSlaveId, gen_pSlaveStatisticsDesc))
        return gen_dwRetVal

    def ClearSlaveStatistics(self, dwSlaveId): # ret: ECError
        """
        Clears all error registers of a slave.

        Args:
            dwSlaveId: Slave Id, INVALID_SLAVE_ID clears all slaves

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwSlaveId = CEcWrapperTypes.Conv(dwSlaveId, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecClearSlaveStatistics(self.m_dwMasterInstanceId, gen_dwSlaveId))
        return gen_dwRetVal

    def GetMasterSyncUnitInfoNumOf(self): # ret: ECError
        """
        Get number of Master Sync Units info entries.

        Args:

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetMasterSyncUnitInfoNumOf(self.m_dwMasterInstanceId))
        return gen_dwRetVal

    def GetMasterSyncUnitInfo(self, wMsuId, pMsuInfo): # ret: ECError
        """
        Get number of Master Sync Units info entries.

        Args:
            wMsuId: 
            pMsuInfo: 

        Returns:
            EC_E_NOERROR or error code
        """
        gen_wMsuId = CEcWrapperTypes.Conv(wMsuId, "ushort")
        gen_pMsuInfo = CEcWrapperTypes.Conv(pMsuInfo, "EC_T_MSU_INFO")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetMasterSyncUnitInfo(self.m_dwMasterInstanceId, gen_wMsuId, gen_pMsuInfo))
        return gen_dwRetVal

    def GetMasterDump(self, pbyBuffer, dwBufferSize, pdwDumpSize): # ret: ECError
        """
        The dump contains relevant information about the master and slave status. The dump is only intended for internal troubleshooting at acontis Amongst others it contains the following descriptors:
        EC_T_INIT_MASTER_PARMS, EC_T_BUS_DIAGNOSIS_INFO, EC_T_MAILBOX_STATISTICS, EC_T_CFG_SLAVE_INFO, EC_T_BUS_SLAVE_INFO, EC_T_SLVSTATISTICS_DESC
        
        \note The buffer is written until all relevant data have been dumped or buffer size has been exceeded.

        Args:
            pbyBuffer: Preallocated buffer to dump log data
            dwBufferSize: Size of preallocated buffer
            pdwDumpSize: Size of master dump

        Returns:
            - EC_E_NOERROR
            - EC_E_NOMEMORY if buffer too small
        """
        gen_pbyBuffer = CEcWrapperTypes.Conv(pbyBuffer, "byte[]")
        gen_dwBufferSize = CEcWrapperTypes.Conv(dwBufferSize, "uint")
        gen_pdwDumpSize = CEcWrapperTypes.Conv(pdwDumpSize, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecGetMasterDump(self.m_dwMasterInstanceId, gen_pbyBuffer, gen_dwBufferSize, ctypes.pointer(gen_pdwDumpSize)))
        CEcWrapperTypes.Conv_Array(gen_pbyBuffer, pbyBuffer)
        return gen_dwRetVal

    def BadConnectionsDetect(self, dwTimeout): # ret: ECError
        """
        Analyzes the slave ESC error counters, Invalid Frame Counter (0x0300), RX Error Counter (0x0301),
        Lost Link Counter (0x0310), whether there is a problem in the area PHY - connector - cable - connector - PHY.
        If one of the above error counters shows a value not equal to zero, an EC_NOTIFY_BAD_CONNECTION is generated, which contains the exact position of the faulty connection.
        
        \note Reads the error counters of all slaves before detection.
        It is recommended to call emBadConnectionsReset() on startup of EC-Master to ensure that all error counters of all slaves are in a defined state.

        Args:
            dwTimeout: Timeout [ms] May not be EC_NOWAIT!

        Returns:
            EC_E_NOERROR or error code
        """
        gen_dwTimeout = CEcWrapperTypes.Conv(dwTimeout, "uint")
        gen_dwRetVal = self.ConvResAsError(CEcWrapper.Get().ecBadConnectionsDetect(self.m_dwMasterInstanceId, gen_dwTimeout))
        return gen_dwRetVal

    #// @CODEGENERATOR_IMPL_END@


class CEcWrapperPythonRefParam:
    """
    'ref' Parameter 
    """
    def __init__(self, value):
        self.value = value


class CEcWrapperPythonOutParam:
    """
    'out' Parameter 
    """
    def __init__(self):
        self.value =  None


class CEcWrapperPythonException(Exception):
    """
    EcWrapper Python Exception

    EnableExceptionHandling = true, functions to throw an exception instead of returning an error code
    """
    def __init__(self, code, text, message = None):
        message = message if message else "{} (0x{:08X})".format(text, code)
        super(CEcWrapperPythonException, self).__init__(message)
        self.code = code
        self.text = text
        self.message = message
        return

    def __str__(self):
        return self.message


class CEcWrapperPythonEx(CEcWrapperPython):
    """
    Extended EcWrapper for Python (combines EcWrapper with RAS server and Mailbox gateway server)
    """
    def __init__(self):
        super().__init__()
        self._rasServer = None
        self._mbxGatewayServer = None


    def InitWrapper(self, dwMasterInstanceId, oInitMaster, oRasParms, oMbxGatewayParms, bUseAuxClock, bSimulator = False, oSimulatorParms = None):
        """
        Initializes the EtherCAT wrapper

        Args:
            dwMasterInstanceId: Master instance
            oInitMaster: Pointer to parameter definitions
            oRasParms: Pointer to ras parameter definitions (null = Ras server will not be started)
            oMbxGatewayParms: Pointer to mailbox gateway parameter definitions
            bUseAuxClock: True, to use the soft real-time timer
            bSimulator: True, to activate simulator mode
            oSimulatorParms: Pointer to simulator HiL parameter definitions

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        if bSimulator and oMbxGatewayParms is not None:
            return ECError.EC_INVALIDPARM
  
        if oInitMaster is not None:
            eRetVal = ECError.EC_ERROR
    
            if oRasParms is not None:
                oParamsMasterRas = DN_EC_T_INIT_PARMS_MASTER_RAS_SERVER()
                oParamsMasterRas.oRas = oRasParms
                self._rasServer = CEcWrapperPython()
                eRetVal = self._rasServer.InitInstance(oParamsMasterRas)
                if eRetVal != ECError.EC_NOERROR:
                    return eRetVal
    
            oParams = DN_EC_T_INIT_PARMS_MASTER()
            oParams.dwMasterInstanceId = dwMasterInstanceId
            oParams.oMaster = oInitMaster
            oParams.bUseAuxClock = bUseAuxClock
            eRetVal = self.InitInstance(oParams)
            if eRetVal != ECError.EC_NOERROR:
                if self._rasServer is not None:
                    self._rasServer.DeinitInstance()
                    self._rasServer = None
      
                return eRetVal
    
            if oMbxGatewayParms is not None:
                oParamsMbxGateway = DN_EC_T_INIT_PARMS_MBXGATEWAY_SERVER()
                oParamsMbxGateway.dwMasterInstanceId = dwMasterInstanceId
                oParamsMbxGateway.oMbxGateway = oMbxGatewayParms
                self._mbxGatewayServer = CEcWrapperPython()
                eRetVal = self._mbxGatewayServer.InitInstance(oParamsMbxGateway)
                if eRetVal != ECError.EC_NOERROR:
                    if self._rasServer is not None:
                        self._rasServer.DeinitInstance()
                        self._rasServer = None
        
                    self.DeinitInstance()
                    return eRetVal
    
            return ECError.EC_NOERROR
  
        if bSimulator:
            eRetVal = ECError.EC_ERROR
    
            if oRasParms is not None:
                oParamsSimulatorRas = DN_EC_T_INIT_PARMS_SIMULATOR_RAS_SERVER()
                oParamsSimulatorRas.oRas = oRasParms
                self._rasServer = CEcWrapperPython()
                eRetVal = self._rasServer.InitInstance(oParamsSimulatorRas)
                if eRetVal != ECError.EC_NOERROR:
                    return eRetVal
    
            oParams = DN_EC_T_INIT_PARMS_SIMULATOR()
            oParams.dwSimulatorInstanceId = dwMasterInstanceId
            oParams.oSimulator = oSimulatorParms
            eRetVal = self.InitInstance(oParams)
            if eRetVal != ECError.EC_NOERROR:
                if self._rasServer is not None:
                    self._rasServer.DeinitInstance()
                    self._rasServer = None
      
                return eRetVal
    
            return ECError.EC_NOERROR
  
        if oRasParms is not None:
            oParams = DN_EC_T_INIT_PARMS_RAS_CLIENT()
            oParams.dwMasterInstanceId = dwMasterInstanceId
            oParams.oRas = oRasParms
            return self.InitInstance(oParams)
  
        if oMbxGatewayParms is not None:
            oParams = DN_EC_T_INIT_PARMS_MBXGATEWAY_CLIENT()
            oParams.oMbxGateway = oMbxGatewayParms
            return self.InitInstance(oParams)
  
        return ECError.EC_NOTSUPPORTED


    def DeinitWrapper(self):
        """
        Terminates the EtherCAT wrapper and releases all resources

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        eRetVal = self.DeinitInstance()
        if eRetVal != ECError.EC_NOERROR:
            return eRetVal
  
        if self._rasServer is not None:
            eRetVal = self._rasServer.DeinitInstance()
            if eRetVal != ECError.EC_NOERROR:
                return eRetVal
    
            self._rasServer = None
  
        if self._mbxGatewayServer is not None:
            eRetVal = self._mbxGatewayServer.DeinitInstance()
            if eRetVal != ECError.EC_NOERROR:
                return eRetVal
    
            self._mbxGatewayServer = None
  
        return eRetVal


class CEcMasterPython(CEcWrapperPython):
    """
    CEcMaster for Python
    """

    @staticmethod
    def Open(oParms):
        """
        Initialize EcMaster and return instance

        Args:
            oParms: Parameter definitions

        Returns:
            Instance on success, otherwise Null.
        """
        oObj = CEcMasterPython()
        eRes = oObj.DoOpen(oParms)
        if eRes != ECError.EC_NOERROR:
            return None
        return oObj


    def DoOpen(self, oParms):
        """
        Initialize EcMaster

        Args:
            oParms: Parameter definitions

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        return self.InitInstance(oParms)


    def Close(self):
        """
        Deinitialize EcMaster

        Returns:
            ECError: EC_E_NOERROR on success, otherwise an error code.
        """
        return self.DeinitInstance()
