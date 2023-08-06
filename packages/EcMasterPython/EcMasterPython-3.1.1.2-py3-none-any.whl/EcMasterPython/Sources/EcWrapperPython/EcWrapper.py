#/*-----------------------------------------------------------------------------
# * EcWrapper.py
# * Copyright                acontis technologies GmbH, Ravensburg, Germany
# * Description              EC-Wrapper CPython Interface (internal)
# *---------------------------------------------------------------------------*/
# pylint: disable=unused-wildcard-import, wildcard-import
import ctypes
import platform
import collections
from EcWrapperTypes import *

class CEcWrapper:
    _instance = None
    _installDir = ""
    
    @staticmethod
    def GetEcWrapperName():
        name = platform.system()
        if name == "Windows":
            return "EcWrapper.dll"
        return "libEcWrapper.so"
    
    @classmethod
    def Get(cls):
        if cls._instance is None:
            # fix: TapEdInitParams undefined
            RTLD_LAZY = 0x00001 # https://code.woboq.org/userspace/glibc/bits/dlfcn.h.html
            so_file = cls._installDir + cls.GetEcWrapperName()
            #ctypes.set_conversion_mode('utf-8', 'strict')
            cls._instance = ctypes.CDLL(so_file, mode = RTLD_LAZY)
            for function in CEcWrapperInterface:
                try:
                    func = getattr(cls._instance, function.name)
                    if function.args:
                        func.argtypes = function.args
                    func.restype = function.ret
                except AttributeError as error:
                    print("CEcWrapper.Get: ", str(error))
        return cls._instance

# General functions

    @staticmethod
    def ecSetInstallDir(pszInstallDir):
        CEcWrapper._installDir = pszInstallDir 
        CEcWrapper.Get().ecSetInstallDir(pszInstallDir.encode('utf8'))

# Generated functions

CFunction = collections.namedtuple('CFunction', 'name ret args')

# argtypes are not set here, since this only restricts how objects
# can be passed. e.g. ctypes.byref can not be used when a
# ctypes.POINTER(<type>) is expected
CEcWrapperInterface = [
    CFunction(name="ecGetApiVer", ret=ctypes.c_uint, args=None),
    CFunction(name="ecSetInstallDir", ret=None, args=[ctypes.c_char_p]),
    CFunction(name="ecInit", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecInit2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_bool, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecDone", ret=None, args=[ctypes.c_uint]),
    CFunction(name="ecGetMasterByID", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecOsDbgMsg", ret=None, args=[ctypes.c_char_p]),
    CFunction(name="ecOsQueryMsecCount", ret=ctypes.c_uint, args=None),
    CFunction(name="ecGetText2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_STRING_HLP)]),
    CFunction(name="ecOsAuxClkInit", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]),
    CFunction(name="ecOsAuxClkDeinit", ret=ctypes.c_uint, args=None),
    CFunction(name="ecOsCreateEvent", ret=ctypes.c_void_p, args=None),
    CFunction(name="ecOsDeleteEvent", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecOsWaitForEvent", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecOsDeleteThreadHandle", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecEnablePerformanceMeasuring", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecEnableTranslation", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecGetDefaultValue", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecIoControl", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_IOCTLOPARMS)]),
    CFunction(name="ecExecDefaultJob", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecEoeInstallEndpoint", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p]),
    CFunction(name="ecEoeUninstallEndpoint", ret=ctypes.c_uint, args=[ctypes.c_void_p]),
    CFunction(name="ecEoeTriggerTxEvent", ret=ctypes.c_uint, args=[ctypes.c_void_p]),
    CFunction(name="ecESCTypeText", ret=ctypes.c_uint, args=[ctypes.c_ubyte, ctypes.c_bool, ctypes.POINTER(SDN_EC_STRING_HLP)]),
    CFunction(name="ecSlaveVendorText", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_STRING_HLP)]),
    CFunction(name="ecSlaveProdCodeText", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_STRING_HLP)]),
    CFunction(name="ecRestartScanBus", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_bool]),
    CFunction(name="ecSetBusCnfReadProp", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecIoControl2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecGetBusScanSlaveInfoDesc", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_short, ctypes.POINTER(SDN_EC_T_SB_SLAVEINFO_DESC)]),
    CFunction(name="ecGetScanBusStatus", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_SB_STATUS_NTFY_DESC)]),
    CFunction(name="ecCoeGetObjectDescReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort, ctypes.POINTER(SDN_EC_T_COE_OBDESC), ctypes.c_uint]),
    CFunction(name="ecCoeGetEntryDescReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.POINTER(SDN_EC_T_COE_ENTRYDESC), ctypes.c_uint]),
    CFunction(name="ecCoeGetODList2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecMbxTferCreate2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]),
    CFunction(name="ecMbxTferWait", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p]),
    CFunction(name="ecMbxTferCopyTo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecMbxTferCopyFrom", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecNotifyApp2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_ushort, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecGetNotificationData", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecSetNotificationData", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecParseNotificationType", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecParseNotificationErrMsg", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p]),
    CFunction(name="ecParseRasNotificationErrMsg", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p]),
    CFunction(name="ecGetNotificationErrMsg", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(SDN_EC_STRING_HLP)]),
    CFunction(name="ecFreeNotificationErrMsg", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecParseMbxTransferData", ret=None, args=[ctypes.c_void_p, ctypes.POINTER(SDN_EC_T_MBXTFER), ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p]),
    CFunction(name="ecOsWaitForEvent2", ret=ctypes.c_bool, args=[ctypes.c_void_p]),
    CFunction(name="ecForceSlvStatCollection", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecSetAllSlavesMustReachState", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool]),
    CFunction(name="ecSetAdditionalVariablesForSpecificDataTypesEnabled", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool]),
    CFunction(name="ecEnableNotification", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool]),
    CFunction(name="ecGetSlvStatistics", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_SLVSTATISTICS_DESC)]),
    CFunction(name="ecGetCyclicConfigInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_CYC_CONFIG_DESC)]),
    CFunction(name="ecSetScanBusEnable", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecSetScanBusStatus", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecReadIdentifyObj", ret=None, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetSlaveInfoEx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_SB_SLAVEINFO_REQ_DESC), ctypes.POINTER(SDN_EC_T_SB_SLAVEINFO_RES_DESC)]),

#//////////////////////////////////////////////////////////////////////////
#// RasServer functions
    CFunction(name="ecRasSrvStart", ret=ctypes.c_uint, args=[ctypes.POINTER(SDN_ATEMRAS_T_SRVPARMS), ctypes.c_void_p, ctypes.c_bool]),
    CFunction(name="ecRasSrvStop", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.c_uint]),

#//////////////////////////////////////////////////////////////////////////
#// RasClient functions
    CFunction(name="ecRasClntGetVersion", ret=ctypes.c_uint, args=None),
    CFunction(name="ecRasClntInit", ret=ctypes.c_uint, args=[ctypes.POINTER(SDN_ATEMRAS_T_CLNTPARMS), ctypes.c_bool]),
    CFunction(name="ecRasClntClose", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecRasClntAddConnection", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_ATEMRAS_T_CLNTCONDESC), ctypes.c_void_p]),
    CFunction(name="ecRasClntRemoveConnection", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecRasGetConnectionInfo", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.POINTER(SDN_EC_T_RAS_CONNECTION_INFO)]),

#//////////////////////////////////////////////////////////////////////////
#// MbxGateway functions
    CFunction(name="ecMbxGatewayClntGetVersion", ret=ctypes.c_uint, args=None),
    CFunction(name="ecMbxGatewayClntInit", ret=ctypes.c_uint, args=[ctypes.POINTER(SDN_EC_T_MBX_GATEWAY_CLNT_PARMS)]),
    CFunction(name="ecMbxGatewayClntDeinit", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecMbxGatewayClntAddConnection", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_MBX_GATEWAY_CLNT_CONDESC)]),
    CFunction(name="ecMbxGatewayClntRemoveConnection", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecMbxGatewayClntCoeSdoDownload", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecMbxGatewayClntCoeSdoUpload", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.c_uint]),

#//////////////////////////////////////////////////////////////////////////
#// MbxGatewaySrv functions
    CFunction(name="ecMbxGatewaySrvGetVersion", ret=ctypes.c_uint, args=None),
    CFunction(name="ecMbxGatewaySrvStart", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_MBX_GATEWAY_SRV_PARMS), ctypes.c_void_p]),
    CFunction(name="ecMbxGatewaySrvStop", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.c_uint]),

#//////////////////////////////////////////////////////////////////////////
#// Simulator functions
    CFunction(name="ecSimulatorInit", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecSimulatorDeinit", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecInitSimulator", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_SIMULATOR_INIT_PARMS)]),
    CFunction(name="ecDeinitSimulator", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecConnectPorts", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_ushort, ctypes.c_ubyte]),
    CFunction(name="ecDisconnectPort", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte]),
    CFunction(name="ecPowerSlave", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_bool]),
    CFunction(name="ecDeleteSlaveCoeObject", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ushort]),
    CFunction(name="ecClearSlaveCoeObjectDictionary", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecResetSlaveCoeObjectDictionary", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecConfigureNetwork", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecSetErrorAtSlavePort", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_bool]),
    CFunction(name="ecSetErrorGenerationAtSlavePort", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_bool, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecResetErrorGenerationAtSlavePorts", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecSetLinkDownAtSlavePort", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_bool, ctypes.c_uint]),
    CFunction(name="ecSetLinkDownGenerationAtSlavePort", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecResetLinkDownGenerationAtSlavePorts", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),

#//////////////////////////////////////////////////////////////////////////
#// Simulator RasServer functions
    CFunction(name="ecSimulatorRasSrvStart", ret=ctypes.c_uint, args=[ctypes.POINTER(SDN_ATEMRAS_T_SRVPARMS), ctypes.c_void_p, ctypes.c_bool]),
    CFunction(name="ecSimulatorRasSrvStop", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.c_uint]),

#//////////////////////////////////////////////////////////////////////////
#// Performance Measurement functions
    CFunction(name="ecPerfMeasInit", ret=None, args=[ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint]),
    CFunction(name="ecPerfMeasDeinit", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecPerfMeasEnable", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecPerfMeasStart", ret=None, args=[ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecPerfMeasEnd", ret=None, args=[ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecPerfMeasReset", ret=None, args=[ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecPerfMeasDisable", ret=None, args=[ctypes.c_void_p]),
    CFunction(name="ecPerfMeasShow", ret=None, args=[ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p]),
    CFunction(name="ecPerfMeasSetIrqCtlEnabled", ret=None, args=[ctypes.c_bool]),

#//////////////////////////////////////////////////////////////////////////
#// DotNetWrapper functions
#//
    CFunction(name="ecBitCopy", ret=None, args=[ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecIntPtrAdd", ret=ctypes.c_void_p, args=[ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecRegisterClient2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_REGISTERPARMS), ctypes.POINTER(SDN_EC_T_REGISTERRESULTS)]),
    CFunction(name="ecUnregisterClient2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecInitMaster2", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_INIT_MASTER_PARMS)]),
    CFunction(name="ecDeinitMaster", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecGetSlaveInpVarInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecGetSlaveOutpVarInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecGetSlaveInpVarInfoEx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecGetSlaveOutpVarInfoEx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecReadSlaveEEPRom", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecWriteSlaveEEPRom", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetObjectByIdx", ret=ctypes.c_uint, args=[ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]),
    CFunction(name="ecSdoUploadMasterOd", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]),

#//////////////////////////////////////////////////////////////////////////
#// Generated functions

#// @CODEGENERATOR_IMPL_BEGIN@
    CFunction(name="ecSetMasterParms", ret=ctypes.c_uint, args=[ctypes.c_uint, SDN_EC_T_INIT_MASTER_PARMS]),
    CFunction(name="ecSetMasterRedStateReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool]),
    CFunction(name="ecGetMasterRedState", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecGetMasterRedProcessImageInputPtr", ret=ctypes.c_void_p, args=[ctypes.c_uint]),
    CFunction(name="ecGetMasterRedProcessImageOutputPtr", ret=ctypes.c_void_p, args=[ctypes.c_uint]),
    CFunction(name="ecScanBus", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecRescueScan", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetMasterInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, SDN_EC_T_MASTER_INFO]),
    CFunction(name="ecConfigureMaster", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecConfigLoad", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecConfigExcludeSlave", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecConfigIncludeSlave", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecConfigSetPreviousPort", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort]),
    CFunction(name="ecConfigAddJunctionRedundancyConnection", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort]),
    CFunction(name="ecConfigApply", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecConfigExtend", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_uint]),
    CFunction(name="ecIsConfigured", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecSetMasterState", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetMasterState", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecStart", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecStop", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetSlaveId", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecGetSlaveFixedAddr", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecGetSlaveIdAtPosition", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecGetSlaveProp", ret=ctypes.c_bool, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_SLAVE_PROP)]),
    CFunction(name="ecGetSlavePortState", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecGetSlaveState", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecSetSlaveState", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecTferSingleRawCmd", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ubyte, ctypes.c_uint, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecReadSlaveRegister", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecReadSlaveRegisterReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_ushort]),
    CFunction(name="ecWriteSlaveRegister", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecWriteSlaveRegisterReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_ushort]),
    CFunction(name="ecQueueRawCmd", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_uint, ctypes.c_void_p, ctypes.c_ushort]),
    CFunction(name="ecClntQueueRawCmd", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_uint, ctypes.c_void_p, ctypes.c_ushort]),
    CFunction(name="ecGetNumConfiguredSlaves", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecMbxTferAbort", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p]),
    CFunction(name="ecMbxTferDelete", ret=None, args=[ctypes.c_uint, ctypes.c_void_p]),
    CFunction(name="ecClntSendRawMbx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecCoeSdoDownloadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecCoeSdoDownload", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecCoeSdoUploadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecCoeSdoUpload", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecCoeGetODList", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecCoeGetObjectDesc", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecCoeGetEntryDesc", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ushort, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_uint]),
    CFunction(name="ecCoeRxPdoTfer", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecFoeFileUpload", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecFoeFileDownload", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecFoeUploadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecFoeSegmentedUploadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecFoeDownloadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecFoeSegmentedDownloadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecSoeWrite", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecSoeRead", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecSoeAbortProcCmd", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecSoeWriteReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecSoeReadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecAoeGetSlaveNetId", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_AOE_NETID)]),
    CFunction(name="ecAoeRead", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_AOE_NETID), ctypes.c_ushort, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecAoeReadReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, SDN_EC_T_AOE_NETID, ctypes.c_ushort, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecAoeWrite", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_AOE_NETID), ctypes.c_ushort, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecAoeWriteReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, SDN_EC_T_AOE_NETID, ctypes.c_ushort, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecAoeReadWrite", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(SDN_EC_T_AOE_NETID), ctypes.c_ushort, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecAoeWriteControl", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, SDN_EC_T_AOE_NETID, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecVoeRead", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecVoeWrite", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecVoeWriteReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetProcessData", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecSetProcessData", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecSetProcessDataBits", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetProcessDataBits", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecForceProcessDataBits", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_uint, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_uint]),
    CFunction(name="ecReleaseProcessDataBits", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_uint, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecReleaseAllProcessDataBits", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetNumConnectedSlaves", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecGetNumConnectedSlavesMain", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecGetNumConnectedSlavesRed", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecReadSlaveEEPRomReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ushort), ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecWriteSlaveEEPRomReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ushort), ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecReloadSlaveEEPRom", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecReloadSlaveEEPRomReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecResetSlaveController", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_uint]),
    CFunction(name="ecAssignSlaveEEPRom", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_bool, ctypes.c_bool, ctypes.c_uint]),
    CFunction(name="ecAssignSlaveEEPRomReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_bool, ctypes.c_bool, ctypes.c_uint]),
    CFunction(name="ecActiveSlaveEEPRom", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.POINTER(ctypes.c_bool), ctypes.c_uint]),
    CFunction(name="ecActiveSlaveEEPRomReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.POINTER(ctypes.c_bool), ctypes.c_uint]),
    CFunction(name="ecHCAcceptTopoChange", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecHCGetNumGroupMembers", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecHCGetSlaveIdsOfGroup", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]),
    CFunction(name="ecSetSlavePortState", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_ushort, ctypes.c_bool, ctypes.c_bool, ctypes.c_uint]),
    CFunction(name="ecSetSlavePortStateReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ushort, ctypes.c_bool, ctypes.c_bool, ctypes.c_uint]),
    CFunction(name="ecSlaveSerializeMbxTfers", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecSlaveParallelMbxTfers", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecDcEnable", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecDcDisable", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecDcIsEnabled", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecDcConfigure", ret=ctypes.c_uint, args=[ctypes.c_uint, SDN_EC_T_DC_CONFIGURE]),
    CFunction(name="ecDcContDelayCompEnable", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecDcContDelayCompDisable", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecDcmConfigure", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_EC_T_DCM_CONFIG), ctypes.c_uint]),
    CFunction(name="ecDcmGetStatus", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]),
    CFunction(name="ecDcxGetStatus", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int64)]),
    CFunction(name="ecDcmResetStatus", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecDcmGetBusShiftConfigured", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecDcmShowStatus", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecDcmGetAdjust", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]),
    CFunction(name="ecGetSlaveInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.POINTER(SDN_EC_T_GET_SLAVE_INFO)]),
    CFunction(name="ecGetCfgSlaveInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.POINTER(SDN_EC_T_CFG_SLAVE_INFO)]),
    CFunction(name="ecGetCfgSlaveEoeInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, SDN_EC_T_CFG_SLAVE_EOE_INFO]),
    CFunction(name="ecGetBusSlaveInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.POINTER(SDN_EC_T_BUS_SLAVE_INFO)]),
    CFunction(name="ecGetSlaveInpVarInfoNumOf", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecGetSlaveOutpVarInfoNumOf", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ushort)]),
    CFunction(name="ecGetSlaveOutpVarByObjectEx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort, SDN_EC_T_PROCESS_VAR_INFO_EX]),
    CFunction(name="ecGetSlaveInpVarByObjectEx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort, SDN_EC_T_PROCESS_VAR_INFO_EX]),
    CFunction(name="ecFindOutpVarByName", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_char_p, ctypes.POINTER(SDN_EC_T_PROCESS_VAR_INFO)]),
    CFunction(name="ecFindOutpVarByNameEx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_char_p, SDN_EC_T_PROCESS_VAR_INFO_EX]),
    CFunction(name="ecFindInpVarByName", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_char_p, SDN_EC_T_PROCESS_VAR_INFO]),
    CFunction(name="ecFindInpVarByNameEx", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_char_p, SDN_EC_T_PROCESS_VAR_INFO_EX]),
    CFunction(name="ecEthDbgMsg", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_char_p]),
    CFunction(name="ecBlockNode", ret=ctypes.c_uint, args=[ctypes.c_uint, SDN_EC_T_SB_MISMATCH_DESC, ctypes.c_uint]),
    CFunction(name="ecOpenBlockedPorts", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecForceTopologyChange", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecIsTopologyChangeDetected", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecIsTopologyKnown", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecGetBusTime", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_uint64)]),
    CFunction(name="ecIsSlavePresent", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecPassThroughSrvGetStatus", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecPassThroughSrvStart", ret=ctypes.c_uint, args=[ctypes.c_uint, SDN_EC_T_PTS_SRV_START_PARMS, ctypes.c_uint]),
    CFunction(name="ecPassThroughSrvStop", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecPassThroughSrvEnable", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecPassThroughSrvDisable", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecAdsAdapterStart", ret=ctypes.c_uint, args=[ctypes.c_uint, SDN_EC_T_ADS_ADAPTER_START_PARMS, ctypes.c_uint]),
    CFunction(name="ecAdsAdapterStop", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetSrcMacAddress", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(SDN_ETHERNET_ADDRESS)]),
    CFunction(name="ecSetLicenseKey", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_char_p]),
    CFunction(name="ecGetVersion", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecTraceDataConfig", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort]),
    CFunction(name="ecTraceDataGetInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, SDN_EC_T_TRACE_DATA_INFO]),
    CFunction(name="ecFastModeInit", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecFastSendAllCycFrames", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecFastProcessAllRxFrames", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_bool)]),
    CFunction(name="ecReadSlaveIdentification", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ushort), ctypes.c_uint]),
    CFunction(name="ecReadSlaveIdentificationReq", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_ushort, ctypes.POINTER(ctypes.c_ushort), ctypes.c_uint]),
    CFunction(name="ecSetSlaveDisabled", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_bool]),
    CFunction(name="ecSetSlavesDisabled", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_uint, ctypes.c_bool]),
    CFunction(name="ecSetSlaveDisconnected", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_bool]),
    CFunction(name="ecSetSlavesDisconnected", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_bool, ctypes.c_ushort, ctypes.c_uint, ctypes.c_bool]),
    CFunction(name="ecGetMemoryUsage", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecGetSlaveStatistics", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint, SDN_EC_T_SLVSTATISTICS_DESC]),
    CFunction(name="ecClearSlaveStatistics", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
    CFunction(name="ecGetMasterSyncUnitInfoNumOf", ret=ctypes.c_uint, args=[ctypes.c_uint]),
    CFunction(name="ecGetMasterSyncUnitInfo", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_ushort, SDN_EC_T_MSU_INFO]),
    CFunction(name="ecGetMasterDump", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]),
    CFunction(name="ecBadConnectionsDetect", ret=ctypes.c_uint, args=[ctypes.c_uint, ctypes.c_uint]),
#// @CODEGENERATOR_IMPL_END@
]

class CEcWrapperTypes:

    @staticmethod
    def Conv_IntToBytes(val, size):
        return val.to_bytes(size, byteorder='little')

    @staticmethod
    def Conv_IntFromBytes(val):
        return int.from_bytes(val, 'little')

    @staticmethod
    def Conv_IntArrayToBytePtr(val):
        size = len(val)
        buff = (ctypes.c_ubyte * size)(*val)
        return ctypes.cast(buff, ctypes.POINTER(ctypes.c_char * len(buff)))[0]

    @staticmethod
    def Conv_IntArrayFromBytePtr(val):
        # https://www.delftstack.com/de/howto/python/how-to-convert-bytes-to-integers/#int-from-bytes-beispiele
        ar = []
        for a in val:
            ar.append(CEcWrapperTypes.Conv_IntFromBytes(a))
        return ar

    @staticmethod
    def Conv_IntArrayFromBytePtrWithSize(val,size):
        # cast void*
        val = ctypes.cast(val, ctypes.POINTER(ctypes.c_char))
        ar = [0] * size.value
        for i in range(size.value):
            ar[i] = val[i]
        return CEcWrapperTypes.Conv_IntArrayFromBytePtr(ar)

    @staticmethod
    def Create_ArrayByType(type_, size):
        defval = 0
        if type_ == "bool":
            defval = False
        elif type_.startswith("DN_"):
            defval = None
        return [defval] * size

    @staticmethod
    def Conv_IntArrayToCTypesArray(ctype, val):
        return (ctype * len(val))(*val)

    @staticmethod
    def Conv_IntArrayFromCTypesArray(val):
        return [x for x in val]

    @staticmethod
    def Conv_Array(src, dst, size=None):
        if size is None:
            size = len(src)
        
        # workaround for bytes/char_array does not support item assignment
        if isinstance(src, bytes) or isinstance(src, ctypes.Array):
            src = ctypes.cast(src, ctypes.POINTER(ctypes.c_uint8))
        if isinstance(dst, bytes) or isinstance(src, ctypes.Array):
            dst = ctypes.cast(dst, ctypes.POINTER(ctypes.c_uint8))

        for i in range(size):
            dst[i] = src[i]

    @staticmethod
    def Conv_StrToCharPtr(str_):
        return ctypes.c_char_p(str_.encode('utf-8'))

    @staticmethod
    def Conv_StrFromCharPtr(str_):
        return str_.decode()

    @staticmethod
    def Pack(ctype_instance):
        buf = ctypes.string_at(ctypes.byref(ctype_instance), ctypes.sizeof(ctype_instance))
        return buf

    @staticmethod
    def Unpack(ctype, buf):
        cstring = ctypes.create_string_buffer(buf)
        ctype_instance = ctypes.cast(ctypes.pointer(cstring), ctypes.POINTER(ctype)).contents
        return ctype_instance

    @staticmethod
    def Conv(obj1, type_="", pack=False):
        name = obj1.__class__.__name__

        if isinstance(obj1, Enum):
            return obj1.value
        if isinstance(obj1, str):
            return ctypes.c_char_p(obj1.encode('utf-8'))
        if type_ == "byte[]":
            return CEcWrapperTypes.Conv_IntArrayToBytePtr(obj1)

        if name != "" and not name.startswith("DN_") and not name.startswith("SDN_"):
            obj2 = None
            if name.startswith("c_"):
                obj2 = CEcWrapperTypes.ConvSimpleDataTypeFromCTypes(obj1, type_)
            else:
                obj2 = CEcWrapperTypes.ConvSimpleDataTypeToCTypes(obj1, type_)
            if obj2 is not None:
                return obj2

        name2 = name

        if name.startswith("SDN_"):
            name2 = name.replace("SDN_", "DN_")
            t = eval(name2)
            obj2 = t()
            CEcWrapperTypes.CopyFieldsFromStruct(obj1, obj2)
            return obj2

        if name.startswith("DN_"):
            name2 = name.replace("DN_", "SDN_")
            t = eval(name2)
            obj2 = t()
            CEcWrapperTypes.CopyFieldsToStruct(obj1, obj2)
            if pack:
                obj2 = CEcWrapperTypes.Pack(obj2)
            return obj2

        return obj1

    @staticmethod
    def CopyFieldsToStruct(obj1, obj2):
        for attr, value in obj1.__dict__.items():
            if value is None:
                continue
            for attr2 in obj2._fields_:
                if attr == attr2[0]:
                    try:
                        value2 = getattr(obj2, attr)
                        if isinstance(value, Enum):
                            setattr(obj2, attr, value.value)
                        elif isinstance(value, list) and isinstance(value2, ctypes.Array):
                            if len(value) == len(value2):
                                for i, elem in enumerate(value):
                                    value2[i] = elem
                                setattr(obj2, attr, value2)
                        elif value is not None and value.__class__.__name__.startswith("DN_"):
                            value21 = CEcWrapperTypes.Conv(value, False)
                            if value2 is None:
                                value22 = ctypes.py_object(value21)
                                value2 = ctypes.cast(ctypes.pointer(value22), ctypes.c_void_p)
                            else:
                                value2 = value21
                            setattr(obj2, attr, value2)
                        elif isinstance(value, str):
                            if len(value)> 0:
                                value2 = str.encode(value)
                            #for i in range(len(value)):
                            #    value2[i] = value[i]
                            #value2 = ctypes.create_string_buffer(value)
                            #value2 = ctypes.cast(value, ctypes.POINTER(ctypes.c_char * 20))[0]
                            setattr(obj2, attr, value2)
                        else:
                            setattr(obj2, attr, value)
                    except Exception as error:
                        print("CEcWrapperTypes.CopyFieldsToStruct: " + attr + " " + str(error))
                    break

    @staticmethod
    def CopyFieldsFromStruct(obj1, obj2):
        for attr in obj1._fields_:
            for attr2, value2 in obj2.__dict__.items():
                if attr[0] == attr2:
                    v = getattr(obj1, attr2)
                    try:
                        if isinstance(value2, str):
                            setattr(obj2, attr2, str(v.decode('utf-8')))
                        else:
                            setattr(obj2, attr2, v)
                    except Exception as error:
                        print("CEcWrapperTypes.CopyFieldsFromStruct: " + attr2 + " " + str(error))
                    break

    @staticmethod
    def ConvSimpleDataTypeFromCTypes(obj1, _type_):
        return obj1.value

    @staticmethod
    def ConvSimpleDataTypeToCTypes(obj1, type_):
        if type_ == "bool":
            return ctypes.c_uint32(1) if obj1 == True else ctypes.c_uint32(0)
        if type_ == "byte":
            return ctypes.c_uint8(obj1)
        if type_ == "ushort":
            return ctypes.c_uint16(obj1)
        if type_ == "uint":
            return ctypes.c_uint32(obj1)
        if type_ == "ulong":
            return ctypes.c_uint64(obj1)
        if type_ == "sbyte":
            return ctypes.c_int8(obj1)
        if type_ == "short":
            return ctypes.c_int16(obj1)
        if type_ == "int":
            return ctypes.c_int32(obj1)
        if type_ == "long":
            return ctypes.c_int16(obj1)
        if type_ == "IntPtr":
            return ctypes.c_void_p(obj1)
        return None

    @staticmethod
    def ConvRes(obj):
        return obj
    
    @staticmethod
    def GetNotificationDataType(code):
        #// @CODEGENERATOR_IMPL_NOTIFYTYPE_BEGIN@
        if code == DN_NotifyCode.STATECHANGED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.ETH_LINK_CONNECTED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SB_STATUS:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.DC_STATUS:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.DC_SLV_SYNC:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.DCL_STATUS:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.DCM_SYNC:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.DCX_SYNC:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVE_STATECHANGED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVES_STATECHANGED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.RAWCMD_DONE:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.COE_TX_PDO:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVE_PRESENCE:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVES_PRESENCE:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.REFCLOCK_PRESENCE:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.MASTER_RED_STATECHANGED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.MASTER_RED_FOREIGN_SRC_MAC:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVE_REGISTER_TRANSFER:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.PORT_OPERATION:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVE_IDENTIFICATION:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.CYCCMD_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.MASTER_INITCMD_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SLAVE_INITCMD_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.EOE_MBXSND_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.COE_MBXSND_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.FOE_MBXSND_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.FRAME_RESPONSE_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SLAVE_INITCMD_RESPONSE_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.MASTER_INITCMD_RESPONSE_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.MBSLAVE_INITCMD_TIMEOUT:
            return NotificationDataType.Error
        if code == DN_NotifyCode.NOT_ALL_DEVICES_OPERATIONAL:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.ETH_LINK_NOT_CONNECTED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.RED_LINEBRK:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.STATUS_SLAVE_ERROR:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVE_ERROR_STATUS_INFO:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SLAVE_NOT_ADDRESSABLE:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SOE_MBXSND_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SOE_WRITE_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.MBSLAVE_COE_SDO_ABORT:
            return NotificationDataType.Error
        if code == DN_NotifyCode.CLIENTREGISTRATION_DROPPED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.RED_LINEFIXED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.FOE_MBSLAVE_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.MBXRCV_INVALID_DATA:
            return NotificationDataType.Error
        if code == DN_NotifyCode.PDIWATCHDOG:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SLAVE_NOTSUPPORTED:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SLAVE_UNEXPECTED_STATE:
            return NotificationDataType.Error
        if code == DN_NotifyCode.ALL_DEVICES_OPERATIONAL:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.VOE_MBXSND_WKC_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.EEPROM_CHECKSUM_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.JUNCTION_RED_CHANGE:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SLAVES_UNEXPECTED_STATE:
            return NotificationDataType.Error
        if code == DN_NotifyCode.LINE_CROSSED:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SLAVES_ERROR_STATUS:
            return NotificationDataType.Error
        if code == DN_NotifyCode.FRAMELOSS_AFTER_SLAVE:
            return NotificationDataType.Error
        if code == DN_NotifyCode.S2SMBX_ERROR:
            return NotificationDataType.Error
        if code == DN_NotifyCode.SB_MISMATCH:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.SB_DUPLICATE_HC_NODE:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.HC_DETECTADDGROUPS:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.HC_PROBEALLGROUPS:
            return NotificationDataType.Notify
        if code == DN_NotifyCode.HC_TOPOCHGDONE:
            return NotificationDataType.Notify
        #// @CODEGENERATOR_IMPL_NOTIFYTYPE_END@
        return NotificationDataType.Default

    @staticmethod
    def ConvNotificationData(code, pbyInBuf):
        #// @CODEGENERATOR_IMPL_NOTIFY_BEGIN@
        if code == DN_NotifyCode.STATECHANGED:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_STATECHANGE))[0])
        if code == DN_NotifyCode.ETH_LINK_CONNECTED:
            return None
        if code == DN_NotifyCode.SB_STATUS:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SB_STATUS_NTFY_DESC))[0])
        if code == DN_NotifyCode.DC_STATUS:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(ctypes.c_uint))[0])
        if code == DN_NotifyCode.DC_SLV_SYNC:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_DC_SYNC_NTFY_DESC))[0])
        if code == DN_NotifyCode.DCL_STATUS:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(ctypes.c_uint))[0])
        if code == DN_NotifyCode.DCM_SYNC:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_DCM_SYNC_NTFY_DESC))[0])
        if code == DN_NotifyCode.DCX_SYNC:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_DCX_SYNC_NTFY_DESC))[0])
        if code == DN_NotifyCode.SLAVE_STATECHANGED:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVE_STATECHANGED_NTFY_DESC))[0])
        if code == DN_NotifyCode.SLAVES_STATECHANGED:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVES_STATECHANGED_NTFY_DESC))[0])
        if code == DN_NotifyCode.RAWCMD_DONE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_RAWCMDRESPONSE_NTFY_DESC))[0])
        if code == DN_NotifyCode.COE_TX_PDO:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_TX_PDO_NTFY_DESC))[0])
        if code == DN_NotifyCode.SLAVE_PRESENCE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVE_PRESENCE_NTFY_DESC))[0])
        if code == DN_NotifyCode.SLAVES_PRESENCE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVES_PRESENCE_NTFY_DESC))[0])
        if code == DN_NotifyCode.REFCLOCK_PRESENCE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_REFCLOCK_PRESENCE_NTFY_DESC))[0])
        if code == DN_NotifyCode.MASTER_RED_STATECHANGED:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(ctypes.c_uint))[0])
        if code == DN_NotifyCode.MASTER_RED_FOREIGN_SRC_MAC:
            return None
        if code == DN_NotifyCode.SLAVE_REGISTER_TRANSFER:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC))[0])
        if code == DN_NotifyCode.PORT_OPERATION:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_PORT_OPERATION_NTFY_DESC))[0])
        if code == DN_NotifyCode.SLAVE_IDENTIFICATION:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVE_IDENTIFICATION_NTFY_DESC))[0])
        if code == DN_NotifyCode.CYCCMD_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.MASTER_INITCMD_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.SLAVE_INITCMD_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.EOE_MBXSND_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.COE_MBXSND_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.FOE_MBXSND_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.FRAME_RESPONSE_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_FRAME_RSPERR_DESC))[0])
        if code == DN_NotifyCode.SLAVE_INITCMD_RESPONSE_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_INITCMD_ERR_DESC))[0])
        if code == DN_NotifyCode.MASTER_INITCMD_RESPONSE_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_INITCMD_ERR_DESC))[0])
        if code == DN_NotifyCode.MBSLAVE_INITCMD_TIMEOUT:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_INITCMD_ERR_DESC))[0])
        if code == DN_NotifyCode.NOT_ALL_DEVICES_OPERATIONAL:
            return None
        if code == DN_NotifyCode.ETH_LINK_NOT_CONNECTED:
            return None
        if code == DN_NotifyCode.RED_LINEBRK:
            return None
        if code == DN_NotifyCode.STATUS_SLAVE_ERROR:
            return None
        if code == DN_NotifyCode.SLAVE_ERROR_STATUS_INFO:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVE_ERROR_INFO_DESC))[0])
        if code == DN_NotifyCode.SLAVE_NOT_ADDRESSABLE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.SOE_MBXSND_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.SOE_WRITE_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_INITCMD_ERR_DESC))[0])
        if code == DN_NotifyCode.MBSLAVE_COE_SDO_ABORT:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_MBOX_SDO_ABORT_DESC))[0])
        if code == DN_NotifyCode.CLIENTREGISTRATION_DROPPED:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(ctypes.c_uint))[0])
        if code == DN_NotifyCode.RED_LINEFIXED:
            return None
        if code == DN_NotifyCode.FOE_MBSLAVE_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_MBOX_FOE_ABORT_DESC))[0])
        if code == DN_NotifyCode.MBXRCV_INVALID_DATA:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_MBXRCV_INVALID_DATA_DESC))[0])
        if code == DN_NotifyCode.PDIWATCHDOG:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_PDIWATCHDOG_DESC))[0])
        if code == DN_NotifyCode.SLAVE_NOTSUPPORTED:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVE_NOTSUPPORTED_DESC))[0])
        if code == DN_NotifyCode.SLAVE_UNEXPECTED_STATE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVE_UNEXPECTED_STATE_DESC))[0])
        if code == DN_NotifyCode.ALL_DEVICES_OPERATIONAL:
            return None
        if code == DN_NotifyCode.VOE_MBXSND_WKC_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_WKCERR_DESC))[0])
        if code == DN_NotifyCode.EEPROM_CHECKSUM_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_EEPROM_CHECKSUM_ERROR_DESC))[0])
        if code == DN_NotifyCode.JUNCTION_RED_CHANGE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_JUNCTION_RED_CHANGE_DESC))[0])
        if code == DN_NotifyCode.SLAVES_UNEXPECTED_STATE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVES_UNEXPECTED_STATE_DESC))[0])
        if code == DN_NotifyCode.LINE_CROSSED:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_LINE_CROSSED_DESC))[0])
        if code == DN_NotifyCode.SLAVES_ERROR_STATUS:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SLAVES_ERROR_DESC))[0])
        if code == DN_NotifyCode.FRAMELOSS_AFTER_SLAVE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_FRAMELOSS_AFTER_SLAVE_NTFY_DESC))[0])
        if code == DN_NotifyCode.S2SMBX_ERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_S2SMBX_ERROR_DESC))[0])
        if code == DN_NotifyCode.SB_MISMATCH:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SB_MISMATCH_DESC))[0])
        if code == DN_NotifyCode.SB_DUPLICATE_HC_NODE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_SB_MISMATCH_DESC))[0])
        if code == DN_NotifyCode.HC_DETECTADDGROUPS:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_HC_DETECTALLGROUP_NTFY_DESC))[0])
        if code == DN_NotifyCode.HC_PROBEALLGROUPS:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_EC_T_HC_DETECTALLGROUP_NTFY_DESC))[0])
        if code == DN_NotifyCode.HC_TOPOCHGDONE:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(ctypes.c_uint))[0])
        if code == DN_NotifyCode.MBOXRCV:
            pMbxTfer = SDN_EC_T_MBXTFER()
            pMbxTferData = ctypes.c_void_p(None) # IntPtr
            dwMaxDataLen = ctypes.c_uint(0) # uint
            pbyMbxTferDescData = ctypes.c_void_p(None) # IntPtr
            CEcWrapper.Get().ecParseMbxTransferData(pbyInBuf, ctypes.pointer(pMbxTfer), ctypes.byref(pMbxTferData), ctypes.byref(dwMaxDataLen), ctypes.byref(pbyMbxTferDescData))
            eMbxTferType = DN_EC_T_MBXTFER_TYPE(pMbxTfer.eMbxTferType)

            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.COE_SDO_DOWNLOAD:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_MBX_DATA_COE))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.COE_SDO_UPLOAD:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_MBX_DATA_COE))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.COE_GETODLIST:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.COE_GETOBDESC:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.COE_GETENTRYDESC:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.COE_EMERGENCY:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_COE_EMERGENCY))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.FOE_FILE_DOWNLOAD:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_MBX_DATA_FOE))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.FOE_FILE_UPLOAD:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_MBX_DATA_FOE))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.SOE_WRITEREQUEST:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.SOE_READREQUEST:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.SOE_EMERGENCY:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_SOE_EMERGENCY))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.SOE_NOTIFICATION:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_SOE_NOTIFICATION))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.VOE_MBX_WRITE:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.VOE_MBX_READ:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.AOE_WRITE:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_AOE_CMD_RESPONSE))[0])
                return mboxRcv
            if eMbxTferType == DN_EC_T_MBXTFER_TYPE.AOE_READ:
                mboxRcv = CEcWrapperTypes.ConvMbxRcv(pMbxTfer)
                mboxRcv.MbxTferData = CEcWrapperTypes.ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen)
                mboxRcv.MbxData = CEcWrapperTypes.Conv(ctypes.cast(pMbxTferData, ctypes.POINTER(SDN_EC_T_AOE_CMD_RESPONSE))[0])
                return mboxRcv
            return None
        #// @CODEGENERATOR_IMPL_NOTIFY_END@
        return None

    @staticmethod
    def ConvMbxRcv(pMbxTfer):
        mboxRcv = DN_EC_T_MBOXRCV()
        mboxRcv.eMbxTferType = DN_EC_T_MBXTFER_TYPE(pMbxTfer.eMbxTferType)
        mboxRcv.eTferStatus = DN_EC_T_MBXTFER_STATUS(pMbxTfer.eTferStatus)
        mboxRcv.dwErrorCode = pMbxTfer.dwErrorCode
        mboxRcv.dwTferId = pMbxTfer.dwTferId
        return mboxRcv

    @staticmethod
    def ConvMbxTferData(pbyMbxTferDescData, dwMaxDataLen):
        if pbyMbxTferDescData == ctypes.c_void_p(None) or dwMaxDataLen == ctypes.c_uint(0):
            return None
        try:
            return CEcWrapperTypes.Conv_IntArrayFromBytePtrWithSize(pbyMbxTferDescData, dwMaxDataLen)
        except:
            return None

    @staticmethod
    def ConvRasNotificationData(code, pbyInBuf):
        if code == DN_RasNotifyCode.CONNECTION:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_ATEMRAS_T_CONNOTIFYDESC))[0])
        if code == DN_RasNotifyCode.REGISTER:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_ATEMRAS_T_REGNOTIFYDESC))[0])
        if code == DN_RasNotifyCode.UNREGISTER:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_ATEMRAS_T_REGNOTIFYDESC))[0])
        if code == DN_RasNotifyCode.MARSHALERROR:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_ATEMRAS_T_MARSHALERRORDESC))[0])
        if code == DN_RasNotifyCode.NONOTIFYMEMORY:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_ATEMRAS_T_NONOTIFYMEMORYDESC))[0])
        if code == DN_RasNotifyCode.STDNOTIFYMEMORYSMALL:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_ATEMRAS_T_NONOTIFYMEMORYDESC))[0])
        if code == DN_RasNotifyCode.MBXNOTIFYMEMORYSMALL:
            return CEcWrapperTypes.Conv(ctypes.cast(pbyInBuf, ctypes.POINTER(SDN_ATEMRAS_T_NONOTIFYMEMORYDESC))[0])
        return None

    @staticmethod
    def ConvBytesToStructure(bytes_, type2):
        return ctypes.cast(bytes_, ctypes.POINTER(type(type2)))[0]
    
    @staticmethod
    def GetSizeOfStructure(type_):
        return ctypes.sizeof(type_)

    @staticmethod
    def ConvMasterOdData(wObIndex):
        #// @CODEGENERATOR_IMPL_MASTEROD_BEGIN@
        if wObIndex == 0x2002:
            return SDN_EC_T_OBJ2002()
        if wObIndex == 0x2003:
            return SDN_EC_T_OBJ2003()
        if wObIndex == 0x2005:
            return SDN_EC_T_OBJ2005()
        if wObIndex == 0x2020:
            return SDN_EC_T_OBJ2020()
        if wObIndex == 0x2200:
            return SDN_EC_T_OBJ2200()
        if wObIndex >= 0x3000 and wObIndex <= 0x3FFF:
            return SDN_EC_T_OBJ3XXX()
        if wObIndex >= 0x8000 and wObIndex <= 0x8FFF:
            return SDN_EC_T_OBJ8XXX()
        if wObIndex >= 0x9000 and wObIndex <= 0x9FFF:
            return SDN_EC_T_OBJ9XXX()
        if wObIndex >= 0xA000 and wObIndex <= 0xAFFF:
            return SDN_EC_T_OBJAXXX()
        if wObIndex == 0xF000:
            return SDN_EC_T_OBJF000()
        if wObIndex >= 0xF020 and wObIndex <= 0xF02F:
            return SDN_EC_T_OBJF02X()
        if wObIndex >= 0xF040 and wObIndex <= 0xF04F:
            return SDN_EC_T_OBJF04X()
        #// @CODEGENERATOR_IMPL_MASTEROD_END@
        return None

    @staticmethod
    def ReadPdBitsFromAddress(pProcessData, dwBitOffset, dwBitLen, out_pData):
        pData = [0] * dwBitLen
        pDataPin = CEcWrapperTypes.Conv_IntArrayToBytePtr(pData) 
        CEcWrapper.Get().ecBitCopy(pDataPin, 0, pProcessData, dwBitOffset, dwBitLen)
        for i in range(dwBitLen):
            if isinstance(pDataPin[i], bytes):
                pData[i] = CEcWrapperTypes.Conv_IntFromBytes(pDataPin[i])
            else:
                pData[i] = pDataPin[i]
        out_pData.value = pData

    @staticmethod
    def ReadPdBitsFromBytes(pProcessData, dwBitOffset, dwBitLen, out_pData):
        pProcessDataPin = CEcWrapperTypes.Conv_IntArrayToBytePtr(pProcessData) 
        CEcWrapperTypes.ReadPdBitsFromAddress(pProcessDataPin, dwBitOffset, dwBitLen, out_pData)

    @staticmethod
    def ReadPdByteFromAddress(pProcessData, dwOffset, dwLength, out_pData):
        src = CEcWrapper.Get().ecIntPtrAdd(pProcessData, dwOffset)
        out_pData.value = CEcWrapperTypes.Conv_IntArrayFromBytePtrWithSize(src, dwLength)

    @staticmethod
    def ReadPdByteFromBytes(pProcessData, dwOffset, dwLength, out_pData):
        pData = [0] * dwLength
        for i in range(dwLength):
            if isinstance(pProcessData[dwOffset + i], bytes):
                pData[i] = CEcWrapperTypes.Conv_IntFromBytes(pProcessData[dwOffset + i])
            else:
                pData[i] = pProcessData[dwOffset + i]
        out_pData.value = pData
 

    @staticmethod
    def WritePdBitsToAddress(pProcessData, dwBitOffset, pData, dwBitLen):
        pDataPin = CEcWrapperTypes.Conv_IntArrayToBytePtr(pData) 
        CEcWrapper.Get().ecBitCopy(pProcessData, dwBitOffset, pDataPin, 0, dwBitLen)

    @staticmethod
    def WritePdBitsToBytes(pProcessData, dwBitOffset, pData, dwBitLen):
        pProcessDataPin = CEcWrapperTypes.Conv_IntArrayToBytePtr(pProcessData) 
        CEcWrapperTypes.WritePdBitsToAddress(pProcessDataPin, dwBitOffset, pData, dwBitLen)

    @staticmethod
    def WritePdByteToAddress(pProcessData, dwOffset, pData):
        pDataPin = CEcWrapperTypes.Conv_IntArrayToBytePtr(pData) 
        CEcWrapper.Get().ecBitCopy(pProcessData, dwOffset * 8, pDataPin, 0, len(pData) * 8)

    @staticmethod
    def WritePdByteToBytes(pProcessData, dwOffset, pData):
        for i, elem in enumerate(pData):
            pProcessData[dwOffset + i] = elem
