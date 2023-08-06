#/*-----------------------------------------------------------------------------
# * EcWrapperPythonTypes.py
# * Copyright                acontis technologies GmbH, Ravensburg, Germany
# * Description              EC-Wrapper Python Types
# *---------------------------------------------------------------------------*/
from enum import Enum, unique

class uint32Enum(int, Enum):
    """
    Base class for creating enumerated constants of unsigned 32 bit integers
    """
    def __new__(cls, value):
        if value < 0:
            raise ValueError("values < 0x0 are not supported")
        if value > 0xFFFFFFFF:
            raise ValueError("values > 0xFFFFFFFF are not supported")
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj


class CEcWrapperPythonTypes:
    @staticmethod
    def Create_ArrayByType(type_, size):
        defval = 0
        if type_ == "bool":
            defval = False
        elif type_.startswith("DN_"):
            defval = None
        return [defval] * size

@unique
class ELinkMode(uint32Enum):
    """Link Layer Modi"""
    #///<summary>Undefined </summary>
    UNDEFINED = 0 # // = EcLinkMode_UNDEFINED,
    #///<summary>INTERRUPT </summary>
    INTERRUPT = 1 # // = EcLinkMode_INTERRUPT,
    #///<summary>POLLING </summary>
    POLLING = 2 # // = EcLinkMode_POLLING,

@unique
class EMailBoxFlags(uint32Enum):
    """MailBoxFlags"""
    #///<summary>No Flags</summary>
    NONE_ = 0
    #///<summary>Complete Access</summary>
    SDO_COMPLETE = 1

@unique
class EEscPort(uint32Enum):
    """ESC Ports (see defines ESC_PORT_A..D)"""
    #///<summary>ESC_PORT_A</summary>
    PORT_A = 0
    #///<summary>ESC_PORT_B</summary>
    PORT_B = 1
    #///<summary>ESC_PORT_C</summary>
    PORT_C = 2
    #///<summary>ESC_PORT_D</summary>
    PORT_D = 3
    #///<summary>ESC_PORT_INVALID</summary>
    PORT_INVALID = 0xFF

@unique
class ELinkType(uint32Enum):
    """Link Layer Type"""
    #///<summary>Undefined</summary>
    UNDEFINED = 0 #// = EcLinkType_UNDEFINED,
    #///<summary>WINPCAP</summary>
    WINPCAP = 1 #// = EcLinkType_WINPCAP,
    #///<summary>SOCKRAW</summary>
    SOCKRAW = 2 #// = EcLinkType_SOCKRAW,
    #///<summary>I8254X</summary>
    I8254X = 3 #// = EcLinkType_I8254X,
    #///<summary>I8255X</summary>
    I8255X = 4 #// = EcLinkType_I8255X,
    #///<summary>UDP</summary>
    UDP = 5 #// = EcLinkType_Udp,
    #///<summary>RTL8139</summary>
    RTL8139 = 6 #// = EcLinkType_RTL8139,
    #///<summary>RTL8169</summary>
    RTL8169 = 7 #// = EcLinkType_RTL8169,
    #///<summary>CCAT</summary>
    CCAT = 8 #// = EcLinkType_CCAT,
    #///<summary>NDIS</summary>
    NDIS = 9 #// = EcLinkType_NDIS,
    #///<summary>Simulator</summary>
    Simulator = 10 #// = EcLinkType_Simulator,

class DN_EC_T_LINK_PARMS_DEFAULT:
    def __init__(self):
        return

class DN_EC_T_LINK_PARMS_WINPCAP:
    def __init__(self):
        self.abyIpAddress = [ 0, 0, 0, 0 ]
        self.szAdapterId = "" #/* {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX} */

class DN_EC_T_LINK_PARMS_SOCKRAW:
    def __init__(self):
        self.szAdapterName = ""

class DN_EC_T_LINK_PARMS_I8254X:
    def __init__(self):
        self.wRxBufferCnt = 0           #/* RX buffer count, 0: default to 96 */
        self.wRxBufferSize = 0          #/* RX buffer size (single Ethernet frame).
												#		       \sa EC_T_LINK_I8254X_BUFFERSIZE.
											#			       0: buffer optimized for standard Ethernet frame. */
        self.wTxBufferCnt = 0           #/* TX buffer count, 0: default to 96 */
        self.wTxBufferSize = 0          #/* TX buffer size (single Ethernet frame).
												#		       \sa EC_T_LINK_I8254X_BUFFERSIZE.
												#		       0: buffer optimized for standard Ethernet frame. */
        self.bDisableLocks = False          #/* Locks in LL Disabled */

class DN_EC_T_LINK_PARMS_UDP:
    def __init__(self):
        self.szAdapterName = ""
        self.abyIpAddress = [ 0, 0, 0, 0 ]
        self.wPort = 0

class DN_EC_T_LINK_PARMS_NDIS:
    def __init__(self):
        self.szAdapterName = ""
        self.abyIpAddress = [ 0, 0, 0, 0 ]

class DN_EC_T_SIMULATOR_DEVICE_CONNECTION_DESC:
    def __init__(self):
        self.dwType = 0                #/* EC_SIMULATOR_DEVICE_CONNECTION_TYPE_... */
        self.dwInstanceID = 0          #/* EC-Simulator Instance ID */
        self.wCfgFixedAddress = 0    #  /* EC-Simulator Configuration (ENI/EXI) */
        self.byPort = 0                #/* 0...3: Port A-D */

class DN_EC_T_LINK_PARMS_SIMULATOR:
    def __init__(self):
        self.szEniFilename = ""
        self.oDeviceConnection = DN_EC_T_SIMULATOR_DEVICE_CONNECTION_DESC()  #/* [in] see EC_SIMULATOR_DEVICE_CONNECTION_TYPE_... */

        #/* EC-Simulator core parameters */
        self.dwBusCycleTimeUsec = 0                            #/* [in] cycle time of simulator job task */
        self.bDisableProcessDataImage = False                      #/* [in] don't allocate Process Data Image at simulator (legacy support, CiA402 simulation) */
        self.qwOemKey = 0                                     #/* [in] 64 bit OEM key (optional) */

        #/* adapter parameters */
        self.abyMac = [ 0, 0, 0, 0 ]                                      #/* [in] MAC station address */
        self.dwRxBufferCnt = 0                                 #/* [in] Frame buffer count for IST */

        #/* application specific */
        self.bJobsExecutedByApp = False                            #/* [in] EC_FALSE: esExecJob explicitely called by application, EC_TRUE: implicitely by emllSimulator */

        #/* license key */
        self.szLicenseKey = ""

        #/* RAS server port */
        self.wRasServerPort = 0                              #/* [in] RAS server port */
        self.dwRasPriority = 0                                 #/* [in] RAS server thread priority */

class DN_EC_T_LINK_PARMS:
    def __init__(self):
        self.eLinkType = ELinkType.UNDEFINED
        self.eLinkMode = ELinkType.UNDEFINED
        self.dwInstance = 0
        self.oDefault = DN_EC_T_LINK_PARMS_DEFAULT()
        self.oWinPcap = DN_EC_T_LINK_PARMS_WINPCAP()
        self.oSockRaw = DN_EC_T_LINK_PARMS_SOCKRAW()
        self.oI8254x = DN_EC_T_LINK_PARMS_I8254X()
        self.oUdp = DN_EC_T_LINK_PARMS_UDP()
        self.oNdis = DN_EC_T_LINK_PARMS_NDIS()
        self.oSimulator = DN_EC_T_LINK_PARMS_SIMULATOR()

class DN_EC_T_INIT_MASTER_PARMS:
    def __init__(self):
        self.dwSignature = 0                        #/*< [in] set to ATECAT_SIGNATURE */
        self.dwSize = 0                             #/*< [in] set to sizeof(EC_T_INIT_MASTER_PARMS) */

        #//struct _EC_T_OS_PARMS*      pOsParms;         #/*< [in] OS layer parameters */
        self.oLinkParms = None    #/*< [in] Link layer parameters */
        self.oLinkParmsRed = None #/*< [in] Link layer parameters for red device */

        self.dwBusCycleTimeUsec = 0                 #/*< [in] [usec] bus cycle time in microseconds */

        #/* memory */
        self.dwMaxBusSlaves = 0                     #/*< [in] maximum pre-allocated bus slave objects */
        self.dwMaxAcycFramesQueued = 0              #/*< [in] maximum queued Ethernet frames */
        self.dwAdditionalEoEEndpoints = 0           #/*< [in] additional EoE endpoints */

        #/* bus load */
        self.dwMaxAcycBytesPerCycle = 0             #/*< [in] maximum bytes sent during eUsrJob_SendAcycFrames per cycle */

        #/* CPU load */
        self.dwMaxAcycFramesPerCycle = 0            #/*< [in] maximum frames amount sent during eUsrJob_SendAcycFrames per cycle */
        self.dwMaxAcycCmdsPerCycle = 0              #/*< [in] maximum cmds amount sent during eUsrJob_SendAcycFrames per cycle */
        self.dwMaxSlavesProcessedPerCycle = 0       #/*< [in] maximum slave-related state machine calls per cycle */

        #/* retry and timeouts */
        self.dwEcatCmdMaxRetries = 0                #/*< [in] maximum retries to send pending ethercat command frames */
        self.dwEcatCmdTimeout = 0                   #/*< [in] timeout to send pending ethercat command frames */
        self.dwEoETimeout = 0                       #/*< [in] timeout sending EoE frames */
        self.dwFoEBusyTimeout = 0                   #/*< [in] obsolete */

        #/* VLAN */
        self.bVLANEnable = False                         #/*< [in] E=enable (1/0) */
        self.wVLANId = 0                           #/*< [in] I=VLAN Id (12Bit)*/
        self.byVLANPrio = 0                          #/*< [in] P=Prio (3Bit) */

        #/* Slave to slave mailbox communication */
        self.dwMaxS2SMbxSize = 0                    #/*< [in] Size of the queued S2S mailbox in bytes */
        self.dwMaxQueuedS2SMbxTfe = 0              #/*< [in] S2S Fifo number of entries */

        #/* logging */
        self.dwLogLevel = DN_EC_LOG_LEVEL.UNDEFINED               #/*< [in] log level. See EC_LOG_LEVEL_... */

class DN_EC_T_INIT_PARMS:
    """Abstract initalization parameters"""
    pass

class DN_EC_T_INIT_PARMS_MASTER(DN_EC_T_INIT_PARMS):
    """EcMaster initalization parameters"""
    def __init__(self):
        self.dwMasterInstanceId = 0
        self.oMaster = DN_EC_T_INIT_MASTER_PARMS()
        self.bUseAuxClock = False

class DN_EC_T_INIT_PARMS_RAS_CLIENT(DN_EC_T_INIT_PARMS):
    """RAS client initalization parameters"""
    def __init__(self):
        self.dwMasterInstanceId = 0
        self.oRas = DN_EC_T_INITRASPARAMS()

class DN_EC_T_INIT_PARMS_MASTER_RAS_SERVER(DN_EC_T_INIT_PARMS):
    """RAS server of EcMaster initalization parameters"""
    def __init__(self):
        self.oRas = DN_EC_T_INITRASPARAMS()

class DN_EC_T_INIT_PARMS_MBXGATEWAY_CLIENT(DN_EC_T_INIT_PARMS):
    """Mailbox gateway client of EcMaster initalization parameters"""
    def __init__(self):
        self.oMbxGateway = DN_EC_T_INIT_MBXGATEWAY_PARMS()

class DN_EC_T_INIT_PARMS_MBXGATEWAY_SERVER(DN_EC_T_INIT_PARMS):
    """Mailbox gateway server of EcMaster initalization parameters"""
    def __init__(self):
        self.dwMasterInstanceId = 0
        self.oMbxGateway = DN_EC_T_INIT_MBXGATEWAY_PARMS()

class DN_EC_T_INIT_PARMS_SIMULATOR(DN_EC_T_INIT_PARMS):
    """EcSimulator initalization parameters"""
    def __init__(self):
        self.dwSimulatorInstanceId = 0
        self.oSimulator = DN_EC_T_SIMULATOR_INIT_PARMS()

class DN_EC_T_INIT_PARMS_SIMULATOR_RAS_SERVER(DN_EC_T_INIT_PARMS):
    """RAS server of EcSimulator initalization parameters"""
    def __init__(self):
        self.oRas = DN_EC_T_INITRASPARAMS()

@unique
class EC_T_DEFALT_VALUE(uint32Enum):
    EC_T_DEFALT_VALUE_ATECAT_VERSION = 0
    EC_T_DEFALT_VALUE_ATECAT_SIGNATURE = 1
    EC_T_DEFALT_VALUE_INVALID_SLAVE_ID = 2
    EC_T_DEFALT_VALUE_MASTER_SLAVE_ID = 3
    EC_T_DEFALT_VALUE_MAX_NUMOF_MASTER_INSTANCES = 4
    EC_T_DEFALT_VALUE_MASTER_RED_SLAVE_ID = 5
    EC_T_DEFALT_VALUE_EL9010_SLAVE_ID = 6
    EC_T_DEFALT_VALUE_FRAMELOSS_SLAVE_ID = 7
    EC_T_DEFALT_VALUE_JUNCTION_RED_FLAG = 8
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_SB_SLAVEINFO_DESC:
    def __init__(self):
        self.dwScanBusStatus = 0 # uint                    #/* Status during last Bus Scan */
        self.dwVendorId = 0 # uint                         #/* Vendor Identification */
        self.dwProductCode = 0 # uint                      #/* Product Code */
        self.dwRevisionNumber = 0 # uint                   #/* Revision Number */
        self.dwSerialNumber = 0 # uint                     #/* Serial Number */

class DN_EC_T_COE_OBDESC:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_COE_ENTRYDESC:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

@unique
class ECoEObjCode(uint32Enum):
    """OB Desc Object Code"""
    #///<summary>Variable</summary>
    VARIABLE = 0x07 # //OBJCODE_VAR,

    #///<summary>Array</summary>
    ARRAY = 0x08 # //OBJCODE_ARR,

    #///<summary>Record</summary>
    RECORD = 0x09 # //OBJCODE_REC,

class DN_ATEMRAS_T_CONNOTIFYDESC:
    def __init__(self):
        self.dwCause = 0 # uint   /**< [in]   Connection change type */
        self.dwCookie = 0 # uint  /**< [in]   Cookie of connection */

class DN_ATEMRAS_T_REGNOTIFYDESC:
    def __init__(self):
        self.dwCookie = 0 # uint       #/**< [in]   Cookie of connection */
        self.dwResult = 0 # uint       #/**< [in]   Result of call */
        self.dwInstanceId = 0 # uint   #/**< [in]   ID master instance */
        self.dwClientId = 0 # uint     #/**< [in]   ID of un- / registered client */

class DN_ATEMRAS_T_MARSHALERRORDESC:
    def __init__(self):
        self.dwCookie = 0 # uint       #/**< [in]   Cookie of faulting connection */
        self.dwCause = 0 # uint        #/**< [in]   Cause of fault */
        self.dwLenStatCmd = 0 # uint   #/**< [in]   Faulty Protocol Header */
        self.dwCommandCode = 0 # uint  #/**< [in]   Faulting command code */

class DN_ATEMRAS_T_NONOTIFYMEMORYDESC:
    def __init__(self):
        self.dwCookie = 0 # uint       #/**< [in]   Cookie of faulting connection */
        self.dwCode = 0  # uint        #/**< [in]   Fault causing notification code */        

@unique
class DN_NotifyType(uint32Enum):
    EUnknown = 0
    EError = 1
    EInfo = 2
    EMailBox = 3
    EBusScan = 4
    EHotConnect = 5
    EApp = 6

@unique
class DN_RasNotifyCode(uint32Enum):
    """Specifies EtherCAT errors codes"""
    CONNECTION = 0x00100001 # // data = DN_ATEMRAS_T_CONNOTIFYDESC
    REGISTER = 0x00100002 # // data = DN_ATEMRAS_T_REGNOTIFYDESC
    UNREGISTER = 0x00100003 # // data = DN_ATEMRAS_T_REGNOTIFYDESC
    MARSHALERROR = 0x00110001 # // data = DN_ATEMRAS_T_MARSHALERRORDESC
    ACKERROR = 0x00110002 # // data = none
    NONOTIFYMEMORY = 0x00110003 # // data = DN_ATEMRAS_T_NONOTIFYMEMORYDESC
    STDNOTIFYMEMORYSMALL = 0x00110004 # // data = DN_ATEMRAS_T_NONOTIFYMEMORYDESC
    MBXNOTIFYMEMORYSMALL = 0x00110005 # // data = DN_ATEMRAS_T_NONOTIFYMEMORYDESC

@unique
class EcDeviceState(uint32Enum):
    """Specifies all possible Device states"""
    #/// <summary>Init</summary>
    INIT = 0x0001

    #/// <summary>Pre-operational </summary>
    PREOP = 0x0002

    #/// <summary>Bootstrap</summary>
    BOOTSTRAP = 0x0003

    #/// <summary>Safe operational</summary>
    SAFEOP = 0x0004

    #/// <summary>Operational</summary>
    OP = 0x0008

    #/// <summary>Unknown</summary>
    Unknown = 0xFFFF & (~0x0010)

@unique
class EcRunMode(uint32Enum):
    """Run modes"""
    #/// <summary>None</summary>
    None_ = 0
    #/// <summary>Master</summary>
    Master = 1
    #/// <summary>RasServer</summary>
    RasServer = 2
    #/// <summary>RasClient</summary>
    RasClient = 3
    #/// <summary>MbxGateway</summary>
    MbxGateway = 4
    #/// <summary>MbxGatewaySrv</summary>
    MbxGatewaySrv = 5
    #/// <summary>SimulatorSil</summary>
    SimulatorSil = 6
    #/// <summary>SimulatorHil</summary>
    SimulatorHil = 7
    #/// <summary>SimulatorRasServer</summary>
    SimulatorRasServer = 8

class DN_EC_T_INITRASPARAMS:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_INIT_MBXGATEWAY_PARMS:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

@unique
class ECoeObEntryDescInfo(uint32Enum):
    """OB Entry Description Information"""
    #///<summary>Object Access</summary>
    OBJACCESS = 0x01

    #///<summary>Object Category</summary>
    OBJCATEGORY = 0x02

    #///<summary>PDO Mapping</summary>
    PDOMAPPING = 0x04

    #///<summary>Unit Type</summary>
    UNITTYPE = 0x08

    #///<summary>Default Value</summary>
    DEFAULTVALUE = 0x10

    #///<summary>Min Value</summary>
    MINVALUE = 0x20

    #///<summary>Max Value</summary>
    MAXVALUE = 0x40

@unique
class ECoeObEntryAccess(uint32Enum):
    """OB Entry Access"""
    #///<summary>Read Preop</summary>
    R_PREOP = 0x01

    #///<summary>Read Safeop</summary>
    R_SAFEOP = 0x02

    #///<summary>Read OP</summary>
    R_OP = 0x04

    #///<summary>Write Preop</summary>
    W_PREOP = 0x08

    #///<summary>Write Safeop</summary>
    W_SAFEOP = 0x10

    #///<summary>Write OP</summary>
    W_OP = 0x20

@unique
class EMbxProtocol(uint32Enum):
    """Supported mailbox protocols"""
    #///<summary>Object Access</summary>
    AOE = 0x01

    #///<summary>Object Category</summary>
    EOE = 0x02

    #///<summary>PDO Mapping</summary>
    COE = 0x04

    #///<summary>Unit Type</summary>
    FOE = 0x08

    #///<summary>Default Value</summary>
    SOE = 0x10

    #///<summary>Min Value</summary>
    VOE = 0x20

class DN_EC_T_CYC_CONFIG_DESC:
    def __init__(self):
        self.dwTaskId = 0 # uint
        self.dwPriority = 0 # uint
        self.dwCycleTime = 0 # uint

class DN_EC_T_PTS_SRV_START_PARMS:
    def __init__(self):
        self.oIpAddr = [] # byte[]
        self.dwPtsThreadPriority = 0 # uint
        self.wPort = 0 # ushort

class DN_EC_T_SIMULATOR_INIT_PARMS:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

@unique
class DN_NotifyCode(uint32Enum):
    """Specifies EtherCAT errors codes"""
    UNDEFINED = 0 #// data = None
    #// @CODEGENERATOR_IMPL_NOTIFYCODE_BEGIN@
    STATECHANGED = (0x00000000 | 1) #// data = DN_EC_T_STATECHANGE
    ETH_LINK_CONNECTED = (0x00000000 | 2) #// data = DN_EC_T_DWORD
    SB_STATUS = (0x00000000 | 3) #// data = DN_EC_T_SB_STATUS_NTFY_DESC
    DC_STATUS = (0x00000000 | 4) #// data = DN_EC_T_DWORD
    DC_SLV_SYNC = (0x00000000 | 5) #// data = DN_EC_T_DC_SYNC_NTFY_DESC
    DCL_STATUS = (0x00000000 | 8) #// data = DN_EC_T_DWORD
    DCM_SYNC = (0x00000000 | 9) #// data = DN_EC_T_DCM_SYNC_NTFY_DESC
    DCX_SYNC = (0x00000000 | 10) #// data = DN_EC_T_DCX_SYNC_NTFY_DESC
    SLAVE_STATECHANGED = (0x00000000 | 21) #// data = DN_EC_T_SLAVE_STATECHANGED_NTFY_DESC
    SLAVES_STATECHANGED = (0x00000000 | 22) #// data = DN_EC_T_SLAVES_STATECHANGED_NTFY_DESC
    RAWCMD_DONE = (0x00000000 | 100) #// data = DN_EC_T_RAWCMDRESPONSE_NTFY_DESC
    COE_TX_PDO = (0x00020000 | 1) #// data = DN_EC_T_TX_PDO_NTFY_DESC
    SLAVE_PRESENCE = (0x00000000 | 101) #// data = DN_EC_T_SLAVE_PRESENCE_NTFY_DESC
    SLAVES_PRESENCE = (0x00000000 | 102) #// data = DN_EC_T_SLAVES_PRESENCE_NTFY_DESC
    REFCLOCK_PRESENCE = (0x00000000 | 103) #// data = DN_EC_T_REFCLOCK_PRESENCE_NTFY_DESC
    MASTER_RED_STATECHANGED = (0x00000000 | 104) #// data = DN_EC_T_DWORD
    MASTER_RED_FOREIGN_SRC_MAC = (0x00000000 | 105) #// data = DN_EC_T_DWORD
    SLAVE_REGISTER_TRANSFER = (0x00000000 | 106) #// data = DN_EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC
    PORT_OPERATION = (0x00000000 | 108) #// data = DN_EC_T_PORT_OPERATION_NTFY_DESC
    SLAVE_IDENTIFICATION = (0x00000000 | 109) #// data = DN_EC_T_SLAVE_IDENTIFICATION_NTFY_DESC
    CYCCMD_WKC_ERROR = (0x00010000 | 1) #// data = DN_EC_T_WKCERR_DESC
    MASTER_INITCMD_WKC_ERROR = (0x00010000 | 2) #// data = DN_EC_T_WKCERR_DESC
    SLAVE_INITCMD_WKC_ERROR = (0x00010000 | 3) #// data = DN_EC_T_WKCERR_DESC
    EOE_MBXSND_WKC_ERROR = (0x00010000 | 7) #// data = DN_EC_T_WKCERR_DESC
    COE_MBXSND_WKC_ERROR = (0x00010000 | 8) #// data = DN_EC_T_WKCERR_DESC
    FOE_MBXSND_WKC_ERROR = (0x00010000 | 9) #// data = DN_EC_T_WKCERR_DESC
    FRAME_RESPONSE_ERROR = (0x00010000 | 10) #// data = DN_EC_T_FRAME_RSPERR_DESC
    SLAVE_INITCMD_RESPONSE_ERROR = (0x00010000 | 11) #// data = DN_EC_T_INITCMD_ERR_DESC
    MASTER_INITCMD_RESPONSE_ERROR = (0x00010000 | 12) #// data = DN_EC_T_INITCMD_ERR_DESC
    MBSLAVE_INITCMD_TIMEOUT = (0x00010000 | 14) #// data = DN_EC_T_INITCMD_ERR_DESC
    NOT_ALL_DEVICES_OPERATIONAL = (0x00010000 | 15) #// data = DN_EC_T_DWORD
    ETH_LINK_NOT_CONNECTED = (0x00010000 | 16) #// data = DN_EC_T_DWORD
    RED_LINEBRK = (0x00010000 | 18) #// data = DN_EC_T_DWORD
    STATUS_SLAVE_ERROR = (0x00010000 | 19) #// data = DN_EC_T_DWORD
    SLAVE_ERROR_STATUS_INFO = (0x00010000 | 20) #// data = DN_EC_T_SLAVE_ERROR_INFO_DESC
    SLAVE_NOT_ADDRESSABLE = (0x00010000 | 21) #// data = DN_EC_T_WKCERR_DESC
    SOE_MBXSND_WKC_ERROR = (0x00010000 | 23) #// data = DN_EC_T_WKCERR_DESC
    SOE_WRITE_ERROR = (0x00010000 | 24) #// data = DN_EC_T_INITCMD_ERR_DESC
    MBSLAVE_COE_SDO_ABORT = (0x00010000 | 25) #// data = DN_EC_T_MBOX_SDO_ABORT_DESC
    CLIENTREGISTRATION_DROPPED = (0x00010000 | 26) #// data = DN_EC_T_DWORD
    RED_LINEFIXED = (0x00010000 | 27) #// data = DN_EC_T_DWORD
    FOE_MBSLAVE_ERROR = (0x00010000 | 28) #// data = DN_EC_T_MBOX_FOE_ABORT_DESC
    MBXRCV_INVALID_DATA = (0x00010000 | 29) #// data = DN_EC_T_MBXRCV_INVALID_DATA_DESC
    PDIWATCHDOG = (0x00010000 | 30) #// data = DN_EC_T_PDIWATCHDOG_DESC
    SLAVE_NOTSUPPORTED = (0x00010000 | 31) #// data = DN_EC_T_SLAVE_NOTSUPPORTED_DESC
    SLAVE_UNEXPECTED_STATE = (0x00010000 | 32) #// data = DN_EC_T_SLAVE_UNEXPECTED_STATE_DESC
    ALL_DEVICES_OPERATIONAL = (0x00010000 | 33) #// data = DN_EC_T_DWORD
    VOE_MBXSND_WKC_ERROR = (0x00010000 | 34) #// data = DN_EC_T_WKCERR_DESC
    EEPROM_CHECKSUM_ERROR = (0x00010000 | 35) #// data = DN_EC_T_EEPROM_CHECKSUM_ERROR_DESC
    JUNCTION_RED_CHANGE = (0x00010000 | 37) #// data = DN_EC_T_JUNCTION_RED_CHANGE_DESC
    SLAVES_UNEXPECTED_STATE = (0x00010000 | 38) #// data = DN_EC_T_SLAVES_UNEXPECTED_STATE_DESC
    LINE_CROSSED = (0x00010000 | 36) #// data = DN_EC_T_LINE_CROSSED_DESC
    SLAVES_ERROR_STATUS = (0x00010000 | 39) #// data = DN_EC_T_SLAVES_ERROR_DESC
    FRAMELOSS_AFTER_SLAVE = (0x00010000 | 40) #// data = DN_EC_T_FRAMELOSS_AFTER_SLAVE_NTFY_DESC
    S2SMBX_ERROR = (0x00010000 | 41) #// data = DN_EC_T_S2SMBX_ERROR_DESC
    MBOXRCV = 0x00020000 #// data = DN_COE_SDO_DOWNLOAD
    SB_MISMATCH = (0x00030000 | 2) #// data = DN_EC_T_SB_MISMATCH_DESC
    SB_DUPLICATE_HC_NODE = (0x00030000 | 3) #// data = DN_EC_T_SB_MISMATCH_DESC
    HC_DETECTADDGROUPS = (0x00040000 | 2) #// data = DN_EC_T_HC_DETECTALLGROUP_NTFY_DESC
    HC_PROBEALLGROUPS = (0x00040000 | 3) #// data = DN_EC_T_HC_DETECTALLGROUP_NTFY_DESC
    HC_TOPOCHGDONE = (0x00040000 | 4) #// data = DN_EC_T_DWORD
    #// @CODEGENERATOR_IMPL_NOTIFYCODE_END@

@unique
class DN_EC_T_IOCTL(uint32Enum):
    """Specifies IOCTL codes"""
    #// @CODEGENERATOR_IMPL_IOCTL_BEGIN@
    REGISTERCLIENT = (0x00000000 | 2)
    UNREGISTERCLIENT = (0x00000000 | 3)
    ISLINK_CONNECTED = (0x00000000 | 6)
    SET_FRAME_RESPONSE_ERROR_NOTIFY_MASK = (0x00000000 | 8)
    LINKLAYER_DBG_MSG = (0x00000000 | 10)
    RESET_SLAVE = (0x00000000 | 13)
    SLAVE_LINKMESSAGES = (0x00000000 | 14)
    GET_CYCLIC_CONFIG_INFO = (0x00000000 | 15)
    GET_LINKLAYER_MODE = (0x00000000 | 16)
    IS_SLAVETOSLAVE_COMM_CONFIGURED = (0x00000000 | 17)
    INITIATE_UPDATE_ALL_SLAVE_STATE = (0x00000000 | 19)
    ADD_BRD_SYNC_WINDOW_MONITORING = (0x00000000 | 20)
    ONLY_PROCESS_DATA_IN_IMAGE = (0x00000000 | 21)
    REGISTER_CYCFRAME_RX_CB = (0x00000000 | 22)
    SET_PD_OFFSET_COMPAT_MODE = (0x00000000 | 23)
    IS_MAIN_LINK_CONNECTED = (0x00000000 | 24)
    IS_RED_LINK_CONNECTED = (0x00000000 | 25)
    ADD_COE_INITCMD = (0x00000000 | 26)
    GET_PDMEMORYSIZE = (0x00000000 | 40)
    REGISTER_PDMEMORYPROVIDER = (0x00000000 | 41)
    FORCE_BROADCAST_DESTINATION = (0x00000000 | 42)
    SET_SLVSTAT_PERIOD = (0x00000000 | 43)
    FORCE_SLVSTAT_COLLECTION = (0x00000000 | 44)
    GET_SLVSTATISTICS = (0x00000000 | 45)
    CLR_SLVSTATISTICS = (0x00000000 | 46)
    SET_MBX_RETRYACCESS_COUNT = (0x00000000 | 47)
    SET_MBX_RETRYACCESS_PERIOD = (0x00000000 | 48)
    ALL_SLAVES_MUST_REACH_MASTER_STATE = (0x00000000 | 49)
    SET_NOTIFICATION_CTL = (0x00000000 | 50)
    MASTEROD_SET_VALUE = (0x00000000 | 51)
    SET_CYCFRAME_LAYOUT = (0x00000000 | 52)
    SET_NOTIFICATION_ENABLED = (0x00000000 | 53)
    GET_NOTIFICATION_ENABLED = (0x00000000 | 54)
    SET_MASTER_DEFAULT_TIMEOUTS = (0x00000000 | 55)
    SET_COPYINFO_IN_SENDCYCFRAMES = (0x00000000 | 56)
    SET_BUS_CYCLE_TIME = (0x00000000 | 57)
    ADDITIONAL_VARIABLES_FOR_SPECIFIC_DATA_TYPES = (0x00000000 | 58)
    SET_IGNORE_INPUTS_ON_WKC_ERROR = (0x00000000 | 59)
    SET_GENENI_ASSIGN_EEPROM_BACK_TO_ECAT = (0x00000000 | 60)
    SET_AUTO_ACK_AL_STATUS_ERROR_ENABLED = (0x00000000 | 61)
    SET_AUTO_ADJUST_CYCCMD_WKC_ENABLED = (0x00000000 | 62)
    CLEAR_MASTER_INFO_COUNTERS = (0x00000000 | 63)
    SET_SPLITTED_FRAME_PROCESSING_ENABLED = (0x00000000 | 64)
    SET_ADJUST_CYCFRAMES_AFTER_SLAVES_STATE_CHANGE = (0x00000000 | 65)
    GET_SLVSTAT_PERIOD = (0x00000000 | 66)
    SET_EOE_DEFFERED_SWITCHING_ENABLED = (0x00000000 | 67)
    SET_NEW_BUSSLAVES_TO_INIT = (0x00000000 | 68)
    SET_ZERO_INPUTS_ON_WKC_ZERO = (0x00000000 | 69)
    SET_ZERO_INPUTS_ON_WKC_ERROR = (0x00000000 | 70)
    SET_MAILBOX_POLLING_CYCLES = (0x00000000 | 71)
    SET_IGNORE_SWAPDATA = (0x00000000 | 72)
    SET_MASTER_MAX_STATE = (0x00000000 | 73)
    REG_DC_SLV_SYNC_NTFY = (0x00030000 | 3)
    UNREG_DC_SLV_SYNC_NTFY = (0x00030000 | 4)
    DC_SLV_SYNC_STATUS_GET = (0x00030000 | 5)
    DC_SLV_SYNC_DEVLIMIT_SET = (0x00030000 | 6)
    DC_SLV_SYNC_DEVLIMIT_GET = (0x00030000 | 7)
    DC_SHIFT_SYSTIME = (0x00030000 | 16)
    DC_SETSYNCSTARTOFFSET = (0x00030000 | 17)
    DC_FIRST_DC_SLV_AS_REF_CLOCK = (0x00030000 | 18)
    DC_SLAVE_CONTROLLED_BY_PDI = (0x00030000 | 19)
    DC_ENABLE_ALL_DC_SLV = (0x00030000 | 20)
    DCM_REGISTER_TIMESTAMP = (0x00070000 | 1)
    DCM_UNREGISTER_TIMESTAMP = (0x00070000 | 2)
    DCM_REGISTER_STARTSO_CALLBACK = (0x00070000 | 3)
    DCM_GET_LOG = (0x00070000 | 4)
    SB_RESTART = (0x00050000 | 1)
    SB_STATUS_GET = (0x00050000 | 2)
    SB_SET_BUSCNF_VERIFY = (0x00050000 | 3)
    SB_SET_BUSCNF_VERIFY_PROP = (0x00050000 | 4)
    SB_BUSCNF_GETSLAVE_INFO = (0x00050000 | 5)
    SB_BUSCNF_GETSLAVE_INFO_EEP = (0x00050000 | 6)
    SB_ENABLE = (0x00050000 | 7)
    SB_BUSCNF_GETSLAVE_INFO_EX = (0x00050000 | 9)
    SLV_ALIAS_ENABLE = (0x00050000 | 10)
    SB_SET_BUSCNF_READ_PROP = (0x00050000 | 12)
    SB_SET_TOPOLOGY_CHANGED_DELAY = (0x00050000 | 13)
    SB_SET_ERROR_ON_CROSSED_LINES = (0x00050000 | 14)
    SB_SET_TOPOLOGY_CHANGE_AUTO_MODE = (0x00050000 | 15)
    SB_ACCEPT_TOPOLOGY_CHANGE = (0x00050000 | 16)
    SB_NOTIFY_UNEXPECTED_BUS_SLAVES = (0x00050000 | 17)
    SB_SET_NOTIFY_NOT_CONNECTED_PORT_A = (0x00050000 | 19)
    SB_SET_JUNCTION_REDUNDANCY_MODE = (0x00050000 | 21)
    SB_GET_BUS_SLAVE_PORTS_INFO = (0x00050000 | 22)
    SB_SET_ERROR_ON_LINE_BREAK = (0x00050000 | 23)
    SB_SET_NO_DC_SLAVES_AFTER_JUNCTION = (0x00050000 | 25)
    SB_SET_TOPOLOGY_CHANGED_DELAYS = (0x00050000 | 26)
    HC_SETMODE = (0x00060000 | 1)
    HC_GETMODE = (0x00060000 | 2)
    HC_CONFIGURETIMEOUTS = (0x00060000 | 3)
    SET_FRAME_LOSS_SIMULATION = (0x00FF0000 | 1)
    SET_RXFRAME_LOSS_SIMULATION = (0x00FF0000 | 2)
    SET_TXFRAME_LOSS_SIMULATION = (0x00FF0000 | 3)
    GET_FAST_CONTEXT = (0x00FF0000 | 4)
    SET_OEM_KEY = (0x00FF0000 | 5)
    CHECK_OEM_KEY = (0x00FF0000 | 6)
    #// @CODEGENERATOR_IMPL_IOCTL_END@

class ECError(uint32Enum):
    """Specifies EtherCAT errors codes"""
    #// @CODEGENERATOR_IMPL_ERRCODE_BEGIN@
    EC_NOERROR = 0x00000000
    EC_ERROR = 0x98110000
    EMRAS_ERROR = 0x98110180
    EC_NOTSUPPORTED = 0x98110001
    EC_INVALIDINDEX = 0x98110002
    EC_INVALIDOFFSET = 0x98110003
    EC_CANCEL = 0x98110004
    EC_INVALIDSIZE = 0x98110005
    EC_INVALIDDATA = 0x98110006
    EC_NOTREADY = 0x98110007
    EC_BUSY = 0x98110008
    EC_ACYC_FRM_FREEQ_EMPTY = 0x98110009
    EC_NOMEMORY = 0x9811000A
    EC_INVALIDPARM = 0x9811000B
    EC_NOTFOUND = 0x9811000C
    EC_DUPLICATE = 0x9811000D
    EC_INVALIDSTATE = 0x9811000E
    EC_TIMER_LIST_FULL = 0x9811000F
    EC_TIMEOUT = 0x98110010
    EC_OPENFAILED = 0x98110011
    EC_SENDFAILED = 0x98110012
    EC_INSERTMAILBOX = 0x98110013
    EC_INVALIDCMD = 0x98110014
    EC_UNKNOWN_MBX_PROTOCOL = 0x98110015
    EC_ACCESSDENIED = 0x98110016
    EC_IDENTIFICATIONFAILED = 0x98110017
    EC_LOCK_CREATE_FAILED = 0x98110018
    EC_PRODKEY_INVALID = 0x9811001A
    EC_WRONG_FORMAT = 0x9811001B
    EC_FEATURE_DISABLED = 0x9811001C
    EC_SHADOW_MEMORY = 0x9811001D
    EC_BUSCONFIG_MISMATCH = 0x9811001E
    EC_CONFIGDATAREAD = 0x9811001F
    EC_ENI_NO_SAFEOP_OP_SUPPORT = 0x98110020
    EC_XML_CYCCMDS_MISSING = 0x98110021
    EC_XML_ALSTATUS_READ_MISSING = 0x98110022
    EC_MCSM_FATAL_ERROR = 0x98110023
    EC_SLAVE_ERROR = 0x98110024
    EC_FRAME_LOST = 0x98110025
    EC_CMD_MISSING = 0x98110026
    EC_CYCCMD_WKC_ERROR = 0x98110027
    EC_INVALID_DCL_MODE = 0x98110028
    EC_AI_ADDRESS = 0x98110029
    EC_INVALID_SLAVE_STATE = 0x9811002A
    EC_SLAVE_NOT_ADDRESSABLE = 0x9811002B
    EC_CYC_CMDS_OVERFLOW = 0x9811002C
    EC_LINK_DISCONNECTED = 0x9811002D
    EC_MASTERCORE_INACCESSIBLE = 0x9811002E
    EC_COE_MBXSND_WKC_ERROR = 0x9811002F
    EC_COE_MBXRCV_WKC_ERROR = 0x98110030
    EC_NO_MBX_SUPPORT = 0x98110031
    EC_NO_COE_SUPPORT = 0x98110032
    EC_NO_EOE_SUPPORT = 0x98110033
    EC_NO_FOE_SUPPORT = 0x98110034
    EC_NO_SOE_SUPPORT = 0x98110035
    EC_NO_VOE_SUPPORT = 0x98110036
    EC_EVAL_VIOLATION = 0x98110037
    EC_EVAL_EXPIRED = 0x98110038
    EC_LICENSE_MISSING = 0x98110039
    EC_SDO_ABORTCODE_TOGGLE = 0x98110040
    EC_SDO_ABORTCODE_TIMEOUT = 0x98110041
    EC_SDO_ABORTCODE_CCS_SCS = 0x98110042
    EC_SDO_ABORTCODE_BLK_SIZE = 0x98110043
    EC_SDO_ABORTCODE_SEQNO = 0x98110044
    EC_SDO_ABORTCODE_CRC = 0x98110045
    EC_SDO_ABORTCODE_MEMORY = 0x98110046
    EC_SDO_ABORTCODE_ACCESS = 0x98110047
    EC_SDO_ABORTCODE_WRITEONLY = 0x98110048
    EC_SDO_ABORTCODE_READONLY = 0x98110049
    EC_SDO_ABORTCODE_INDEX = 0x9811004A
    EC_SDO_ABORTCODE_PDO_MAP = 0x9811004B
    EC_SDO_ABORTCODE_PDO_LEN = 0x9811004C
    EC_SDO_ABORTCODE_P_INCOMP = 0x9811004D
    EC_SDO_ABORTCODE_I_INCOMP = 0x9811004E
    EC_SDO_ABORTCODE_HARDWARE = 0x9811004F
    EC_SDO_ABORTCODE_DATA_LENGTH_NOT_MATCH = 0x98110050
    EC_SDO_ABORTCODE_DATA_LENGTH_TOO_HIGH = 0x98110051
    EC_SDO_ABORTCODE_DATA_LENGTH_TOO_LOW = 0x98110052
    EC_SDO_ABORTCODE_OFFSET = 0x98110053
    EC_SDO_ABORTCODE_VALUE_RANGE = 0x98110054
    EC_SDO_ABORTCODE_VALUE_TOO_HIGH = 0x98110055
    EC_SDO_ABORTCODE_VALUE_TOO_LOW = 0x98110056
    EC_SDO_ABORTCODE_MINMAX = 0x98110057
    EC_SDO_ABORTCODE_GENERAL = 0x98110058
    EC_SDO_ABORTCODE_TRANSFER = 0x98110059
    EC_SDO_ABORTCODE_TRANSFER_LOCAL_CONTROL = 0x9811005A
    EC_SDO_ABORTCODE_TRANSFER_DEVICE_STATE = 0x9811005B
    EC_SDO_ABORTCODE_DICTIONARY = 0x9811005C
    EC_SDO_ABORTCODE_UNKNOWN = 0x9811005D
    EC_SDO_ABORTCODE_MODULE_ID_LIST_NOT_MATCH = 0x9811005E
    EC_FOE_ERRCODE_NOTDEFINED = 0x98110060
    EC_FOE_ERRCODE_NOTFOUND = 0x98110061
    EC_FOE_ERRCODE_ACCESS = 0x98110062
    EC_FOE_ERRCODE_DISKFULL = 0x98110063
    EC_FOE_ERRCODE_ILLEGAL = 0x98110064
    EC_FOE_ERRCODE_PACKENO = 0x98110065
    EC_FOE_ERRCODE_EXISTS = 0x98110066
    EC_FOE_ERRCODE_NOUSER = 0x98110067
    EC_FOE_ERRCODE_BOOTSTRAPONLY = 0x98110068
    EC_FOE_ERRCODE_NOTINBOOTSTRAP = 0x98110069
    EC_FOE_ERRCODE_INVALIDPASSWORD = 0x9811006A
    EC_FOE_ERRCODE_PROGERROR = 0x9811006B
    EC_FOE_ERRCODE_INVALID_CHECKSUM = 0x9811006C
    EC_FOE_ERRCODE_INVALID_FIRMWARE = 0x9811006D
    EC_FOE_ERRCODE_NO_FILE = 0x9811006F
    EC_CFGFILENOTFOUND = 0x98110070
    EC_EEPROMREADERROR = 0x98110071
    EC_EEPROMWRITEERROR = 0x98110072
    EC_XML_CYCCMDS_SIZEMISMATCH = 0x98110073
    EC_XML_INVALID_INP_OFF = 0x98110074
    EC_XML_INVALID_OUT_OFF = 0x98110075
    EC_PORTCLOSE = 0x98110076
    EC_PORTOPEN = 0x98110077
    EC_SOE_ERRORCODE_INVALID_ACCESS = 0x98110078
    EC_SOE_ERRORCODE_NOT_EXIST = 0x98110079
    EC_SOE_ERRORCODE_INVL_ACC_ELEM1 = 0x9811007A
    EC_SOE_ERRORCODE_NAME_NOT_EXIST = 0x9811007B
    EC_SOE_ERRORCODE_NAME_UNDERSIZE = 0x9811007C
    EC_SOE_ERRORCODE_NAME_OVERSIZE = 0x9811007D
    EC_SOE_ERRORCODE_NAME_UNCHANGE = 0x9811007E
    EC_SOE_ERRORCODE_NAME_WR_PROT = 0x9811007F
    EC_SOE_ERRORCODE_UNDERS_TRANS = 0x98110080
    EC_SOE_ERRORCODE_OVERS_TRANS = 0x98110081
    EC_SOE_ERRORCODE_ATTR_UNCHANGE = 0x98110082
    EC_SOE_ERRORCODE_ATTR_WR_PROT = 0x98110083
    EC_SOE_ERRORCODE_UNIT_NOT_EXIST = 0x98110084
    EC_SOE_ERRORCODE_UNIT_UNDERSIZE = 0x98110085
    EC_SOE_ERRORCODE_UNIT_OVERSIZE = 0x98110086
    EC_SOE_ERRORCODE_UNIT_UNCHANGE = 0x98110087
    EC_SOE_ERRORCODE_UNIT_WR_PROT = 0x98110088
    EC_SOE_ERRORCODE_MIN_NOT_EXIST = 0x98110089
    EC_SOE_ERRORCODE_MIN_UNDERSIZE = 0x9811008A
    EC_SOE_ERRORCODE_MIN_OVERSIZE = 0x9811008B
    EC_SOE_ERRORCODE_MIN_UNCHANGE = 0x9811008C
    EC_SOE_ERRORCODE_MIN_WR_PROT = 0x9811008D
    EC_SOE_ERRORCODE_MAX_NOT_EXIST = 0x9811008E
    EC_SOE_ERRORCODE_MAX_UNDERSIZE = 0x9811008F
    EC_SOE_ERRORCODE_MAX_OVERSIZE = 0x98110090
    EC_SOE_ERRORCODE_MAX_UNCHANGE = 0x98110091
    EC_SOE_ERRORCODE_MAX_WR_PROT = 0x98110092
    EC_SOE_ERRORCODE_DATA_NOT_EXIST = 0x98110093
    EC_SOE_ERRORCODE_DATA_UNDERSIZE = 0x98110094
    EC_SOE_ERRORCODE_DATA_OVERSIZE = 0x98110095
    EC_SOE_ERRORCODE_DATA_UNCHANGE = 0x98110096
    EC_SOE_ERRORCODE_DATA_WR_PROT = 0x98110097
    EC_SOE_ERRORCODE_DATA_MIN_LIMIT = 0x98110098
    EC_SOE_ERRORCODE_DATA_MAX_LIMIT = 0x98110099
    EC_SOE_ERRORCODE_DATA_INCOR = 0x9811009A
    EC_SOE_ERRORCODE_PASWD_PROT = 0x9811009B
    EC_SOE_ERRORCODE_TEMP_UNCHANGE = 0x9811009C
    EC_SOE_ERRORCODE_INVL_INDIRECT = 0x9811009D
    EC_SOE_ERRORCODE_TEMP_UNCHANGE1 = 0x9811009E
    EC_SOE_ERRORCODE_ALREADY_ACTIVE = 0x9811009F
    EC_SOE_ERRORCODE_NOT_INTERRUPT = 0x98110100
    EC_SOE_ERRORCODE_CMD_NOT_AVAIL = 0x98110101
    EC_SOE_ERRORCODE_CMD_NOT_AVAIL1 = 0x98110102
    EC_SOE_ERRORCODE_DRIVE_NO = 0x98110103
    EC_SOE_ERRORCODE_IDN = 0x98110104
    EC_SOE_ERRORCODE_FRAGMENT_LOST = 0x98110105
    EC_SOE_ERRORCODE_BUFFER_FULL = 0x98110106
    EC_SOE_ERRORCODE_NO_DATA = 0x98110107
    EC_SOE_ERRORCODE_NO_DEFAULT_VALUE = 0x98110108
    EC_SOE_ERRORCODE_DEFAULT_LONG = 0x98110109
    EC_SOE_ERRORCODE_DEFAULT_WP = 0x9811010A
    EC_SOE_ERRORCODE_INVL_DRIVE_NO = 0x9811010B
    EC_SOE_ERRORCODE_GENERAL_ERROR = 0x9811010C
    EC_SOE_ERRCODE_NO_ELEM_ADR = 0x9811010D
    EC_SLAVE_NOT_PRESENT = 0x9811010E
    EC_NO_FOE_SUPPORT_BS = 0x9811010F
    EC_EEPROMRELOADERROR = 0x98110110
    EC_SLAVECTRLRESETERROR = 0x98110111
    EC_SYSDRIVERMISSING = 0x98110112
    EC_BUSCONFIG_TOPOCHANGE = 0x9811011E
    EC_EOE_MBX_WKC_ERROR = 0x9811011F
    EC_FOE_MBX_WKC_ERROR = 0x98110120
    EC_SOE_MBX_WKC_ERROR = 0x98110121
    EC_AOE_MBX_WKC_ERROR = 0x98110122
    EC_VOE_MBX_WKC_ERROR = 0x98110123
    EC_EEPROMASSIGNERROR = 0x98110124
    EC_MBX_ERROR_TYPE = 0x98110125
    EC_REDLINEBREAK = 0x98110126
    EC_XML_INVALID_CMD_WITH_RED = 0x98110127
    EC_XML_PREV_PORT_MISSING = 0x98110128
    EC_XML_DC_CYCCMDS_MISSING = 0x98110129
    EC_DLSTATUS_IRQ_TOPOCHANGED = 0x98110130
    EC_PTS_IS_NOT_RUNNING = 0x98110131
    EC_ADS_IS_RUNNING = 0x98110132
    EC_PTS_THREAD_CREATE_FAILED = 0x98110133
    EC_PTS_SOCK_BIND_FAILED = 0x98110134
    EC_PTS_NOT_ENABLED = 0x98110135
    EC_PTS_LL_MODE_NOT_SUPPORTED = 0x98110136
    EC_VOE_NO_MBX_RECEIVED = 0x98110137
    EC_DC_REF_CLOCK_SYNC_OUT_UNIT_DISABLED = 0x98110138
    EC_DC_REF_CLOCK_NOT_FOUND = 0x98110139
    EC_MBX_CMD_WKC_ERROR = 0x9811013B
    EC_NO_AOE_SUPPORT = 0x9811013C
    EC_AOE_INV_RESPONSE_SIZE = 0x9811013D
    EC_AOE_ERROR = 0x9811013E
    EC_AOE_SRVNOTSUPP = 0x9811013F
    EC_AOE_INVALIDGRP = 0x98110140
    EC_AOE_INVALIDOFFSET = 0x98110141
    EC_AOE_INVALIDACCESS = 0x98110142
    EC_AOE_INVALIDSIZE = 0x98110143
    EC_AOE_INVALIDDATA = 0x98110144
    EC_AOE_NOTREADY = 0x98110145
    EC_AOE_BUSY = 0x98110146
    EC_AOE_INVALIDCONTEXT = 0x98110147
    EC_AOE_NOMEMORY = 0x98110148
    EC_AOE_INVALIDPARM = 0x98110149
    EC_AOE_NOTFOUND = 0x9811014A
    EC_AOE_SYNTAX = 0x9811014B
    EC_AOE_INCOMPATIBLE = 0x9811014C
    EC_AOE_EXISTS = 0x9811014D
    EC_AOE_SYMBOLNOTFOUND = 0x9811014E
    EC_AOE_SYMBOLVERSIONINVALID = 0x9811014F
    EC_AOE_INVALIDSTATE = 0x98110150
    EC_AOE_TRANSMODENOTSUPP = 0x98110151
    EC_AOE_NOTIFYHNDINVALID = 0x98110152
    EC_AOE_CLIENTUNKNOWN = 0x98110153
    EC_AOE_NOMOREHDLS = 0x98110154
    EC_AOE_INVALIDWATCHSIZE = 0x98110155
    EC_AOE_NOTINIT = 0x98110156
    EC_AOE_TIMEOUT = 0x98110157
    EC_AOE_NOINTERFACE = 0x98110158
    EC_AOE_INVALIDINTERFACE = 0x98110159
    EC_AOE_INVALIDCLSID = 0x9811015A
    EC_AOE_INVALIDOBJID = 0x9811015B
    EC_AOE_PENDING = 0x9811015C
    EC_AOE_ABORTED = 0x9811015D
    EC_AOE_WARNING = 0x9811015E
    EC_AOE_INVALIDARRAYIDX = 0x9811015F
    EC_AOE_SYMBOLNOTACTIVE = 0x98110160
    EC_AOE_ACCESSDENIED = 0x98110161
    EC_AOE_INTERNAL = 0x98110162
    EC_AOE_TARGET_PORT_NOT_FOUND = 0x98110163
    EC_AOE_TARGET_MACHINE_NOT_FOUND = 0x98110164
    EC_AOE_UNKNOWN_CMD_ID = 0x98110165
    EC_AOE_PORT_NOT_CONNECTED = 0x98110166
    EC_AOE_INVALID_AMS_LENGTH = 0x98110167
    EC_AOE_INVALID_AMS_ID = 0x98110168
    EC_AOE_PORT_DISABLED = 0x98110169
    EC_AOE_PORT_CONNECTED = 0x9811016A
    EC_AOE_INVALID_AMS_PORT = 0x9811016B
    EC_AOE_NO_MEMORY = 0x9811016C
    EC_AOE_VENDOR_SPECIFIC = 0x9811016D
    EC_XML_AOE_NETID_INVALID = 0x9811016E
    EC_MAX_BUS_SLAVES_EXCEEDED = 0x9811016F
    EC_MBXERR_SYNTAX = 0x98110170
    EC_MBXERR_UNSUPPORTEDPROTOCOL = 0x98110171
    EC_MBXERR_INVALIDCHANNEL = 0x98110172
    EC_MBXERR_SERVICENOTSUPPORTED = 0x98110173
    EC_MBXERR_INVALIDHEADER = 0x98110174
    EC_MBXERR_SIZETOOSHORT = 0x98110175
    EC_MBXERR_NOMOREMEMORY = 0x98110176
    EC_MBXERR_INVALIDSIZE = 0x98110177
    EC_DC_SLAVES_BEFORE_REF_CLOCK = 0x98110178
    EC_DATA_TYPE_CONVERSION_FAILED = 0x98110179
    EC_FOE_ERRCODE_MAX_FILE_SIZE = 0x9811017A
    EC_LINE_CROSSED = 0x9811017B
    EC_LINE_CROSSED_SLAVE_INFO = 0x9811017C
    EC_SOCKET_DISCONNECTED = 0x9811017D
    EC_ADO_NOT_SUPPORTED = 0x9811017E
    EC_FRAMELOSS_AFTER_SLAVE = 0x9811017F
    EC_ERROR_LAST = 0x9811017F
    EC_ERROR2 = 0x98130000
    EC_FOE_ERRCODE_FILE_HEAD_MISSING = 0x98130001
    EC_FOE_ERRCODE_FLASH_PROBLEM = 0x98130002
    EC_FOE_ERRCODE_FILE_INCOMPATIBLE = 0x98130003
    EC_SDO_ABORTCODE_SI_NOT_WRITTEN = 0x98130004
    EC_SDO_ABORTCODE_CA_TYPE_MISM = 0x98130005
    EC_SDO_ABORTCODE_OBJ_TOO_BIG = 0x98130006
    EC_SDO_ABORTCODE_PDO_MAPPED = 0x98130007
    EC_OEM_SIGNATURE_MISMATCH = 0x98130008
    EC_ENI_ENCRYPTION_WRONG_VERSION = 0x98130009
    EC_ENI_ENCRYPTED = 0x9813000A
    EC_OEM_KEY_MISMATCH = 0x9813000B
    EC_OEM_KEY_MISSING = 0x9813000C
    EC_AOE_NO_RTIME = 0x9813000D
    EC_AOE_LOCKED_MEMORY = 0x9813000E
    EC_AOE_MAILBOX = 0x9813000F
    EC_AOE_WRONG_HMSG = 0x98130010
    EC_AOE_BAD_TASK_ID = 0x98130011
    EC_AOE_NO_IO = 0x98130012
    EC_AOE_UNKNOWN_AMS_COMMAND = 0x98130013
    EC_AOE_WIN32 = 0x98130014
    EC_AOE_LOW_INSTALL_LEVEL = 0x98130015
    EC_AOE_NO_DEBUG = 0x98130016
    EC_AOE_AMS_SYNC_WIN32 = 0x98130017
    EC_AOE_AMS_SYNC_TIMEOUT = 0x98130018
    EC_AOE_AMS_SYNC_AMS = 0x98130019
    EC_AOE_AMS_SYNC_NO_INDEX_MAP = 0x9813001A
    EC_AOE_TCP_SEND = 0x9813001B
    EC_AOE_HOST_UNREACHABLE = 0x9813001C
    EC_AOE_INVALIDAMSFRAGMENT = 0x9813001D
    EC_AOE_NO_LOCKED_MEMORY = 0x9813001E
    EC_AOE_MAILBOX_FULL = 0x9813001F
    EC_S2SMBX_NOT_CONFIGURED = 0x98130020
    EC_S2SMBX_NO_MEMORY = 0x98130021
    EC_S2SMBX_NO_DESCRIPTOR = 0x98130022
    EC_S2SMBX_DEST_SLAVE_NOT_FOUND = 0x98130023
    EC_MASTER_RED_STATE_INACTIVE = 0x98130024
    EC_MASTER_RED_STATE_ACTIVE = 0x98130025
    EC_JUNCTION_RED_LINE_BREAK = 0x98130026
    EC_VALIDATION_ERROR = 0x98130027
    EC_TIMEOUT_WAITING_FOR_DC = 0x98130028
    EC_TIMEOUT_WAITING_FOR_DCM = 0x98130029
    EC_SIGNATURE_MISMATCH = 0x98130030
    EC_PDIWATCHDOG = 0x98130031
    EC_BAD_CONNECTION = 0x98130032
    EC_ERROR_LAST2 = 0x9813FFFF
    EMRAS_INVALIDCOOKIE = 0x98110181
    EMRAS_MULSRVDISMULCON = 0x98110183
    EMRAS_LOGONCANCELLED = 0x98110184
    EMRAS_INVALIDVERSION = 0x98110186
    EMRAS_INVALIDACCESSCONFIG = 0x98110187
    EMRAS_ACCESSLESS = 0x98110188
    EMRAS_INVALIDDATARECEIVED = 0x98110189
    EMRAS_SERVERSTOPPED = 0x98110191
    EMRAS_WDEXPIRED = 0x98110192
    EMRAS_RECONEXPIRED = 0x98110193
    EMRAS_CLIENTLOGON = 0x98110194
    EMRAS_RECONNECT = 0x98110195
    EMRAS_SOCKCHANGE = 0x98110196
    EMRAS_CLNTDISC = 0x98110197
    EMRAS_ACCESS_NOT_FOUND = 0x98110198
    EMRAS_ERROR_LAST = 0x981101BF
    #// @CODEGENERATOR_IMPL_ERRCODE_END@

class DN_EC_T_COE_OBJ1018:
    def __init__(self):
        self.wSubIndex0 = 0 # ushort
        self.dwVendorID = 0 # uint
        self.dwProductcode = 0 # uint
        self.dwRevision = 0 # uint
        self.dwSerialnumber = 0 # uint

class DN_EC_T_COE_OBJ2001:
    def __init__(self):
        self.dwMasterStateSummary = 0 # uint

class DN_EC_T_COE_OBJ2001_DESC:
    def __init__(self):
        self.bMasterOk = False # bool
        self.masterState = DN_EC_T_STATE.UNKNOWN # DN_EC_T_STATE
        self.bSlaveInReqState = False # bool
        self.bMasterInReqState = False # bool
        self.bBusScanMatch = False # bool
        self.bDCEnabled = False # bool
        self.bDCInSync = False # bool
        self.bDCBusy = False # bool
        self.bLinkUp = False # bool

    @staticmethod
    def Create(obj2001):
        s_MASK_MasterOk = (1 << 0)
        s_MASK_MasterStateINIT = (1 << 4)
        s_MASK_MasterStatePreOP = (1 << 5)
        s_MASK_MasterStateSaveOP = (1 << 6)
        s_MASK_MasterStateOP = (1 << 7)
        s_MASK_SlaveInReqState = (1 << 8)
        s_MASK_MasterInReqState = (1 << 9)
        s_MASK_BusScanMatch = (1 << 10)
        s_MASK_DCEnabled = (1 << 12)
        s_MASK_DCinSync = (1 << 13)
        s_MASK_DCBusy = (1 << 14)
        s_MASK_LinkUp = (1 << 16)

        dwMasterStateSumObj = obj2001.dwMasterStateSummary

        obj = DN_EC_T_COE_OBJ2001_DESC()
        obj.bMasterOk = (dwMasterStateSumObj & s_MASK_MasterOk) == s_MASK_MasterOk
        obj.bBusScanMatch = (dwMasterStateSumObj & s_MASK_BusScanMatch) == s_MASK_BusScanMatch
        obj.bDCBusy = (dwMasterStateSumObj & s_MASK_DCBusy) == s_MASK_DCBusy
        obj.bDCEnabled = (dwMasterStateSumObj & s_MASK_DCEnabled) == s_MASK_DCEnabled
        obj.bDCInSync = (dwMasterStateSumObj & s_MASK_DCinSync) == s_MASK_DCinSync
        obj.bLinkUp = (dwMasterStateSumObj & s_MASK_LinkUp) == s_MASK_LinkUp
        obj.bSlaveInReqState = (dwMasterStateSumObj & s_MASK_SlaveInReqState) == s_MASK_SlaveInReqState
        obj.bMasterInReqState = (dwMasterStateSumObj & s_MASK_MasterInReqState) == s_MASK_MasterInReqState

        if ((dwMasterStateSumObj & s_MASK_MasterStateINIT) == s_MASK_MasterStateINIT):
            obj.masterState = DN_EC_T_STATE.INIT
        elif ((dwMasterStateSumObj & s_MASK_MasterStatePreOP) == s_MASK_MasterStatePreOP):
            obj.masterState = DN_EC_T_STATE.PREOP
        elif ((dwMasterStateSumObj & s_MASK_MasterStateSaveOP) == s_MASK_MasterStateSaveOP):
            obj.masterState = DN_EC_T_STATE.SAFEOP
        elif ((dwMasterStateSumObj & s_MASK_MasterStateOP) == s_MASK_MasterStateOP):
            obj.masterState = DN_EC_T_STATE.OP
        else:
            obj.masterState = DN_EC_T_STATE.UNKNOWN

        return obj

class DN_EC_T_MBOXRCV:
    def __init__(self):
        self.eMbxTferType = DN_EC_T_MBXTFER_TYPE.BCppDummy # DN_EC_T_MBXTFER_TYPE
        self.eTferStatus = DN_EC_T_MBXTFER_STATUS.BCppDummy # DN_EC_T_MBXTFER_STATUS
        self.dwErrorCode = 0 # UInt32
        self.dwTferId = 0 # UInt32
        self.MbxData = None # object
        self.MbxTferData = None # byte[]

@unique
class DN_EC_LOG_TYPE(uint32Enum):
    MASTER = 0
    RASCLIENT = 1
    RASSERVER = 2
    MBXGATEWAY = 3
    SIMULATORRASSERVER = 4,

#// @CODEGENERATOR_IMPL_BEGIN@
class DN_EC_T_STATE(uint32Enum):
    UNKNOWN = 0
    INIT = 1
    PREOP = 2
    SAFEOP = 4
    OP = 8
    BOOTSTRAP = 3
    BCppDummy = 0xFFFFFFFF

class DN_EC_CMD_TYPE(uint32Enum):
    NOP = 0x00
    APRD = 0x01
    APWR = 0x02
    APRW = 0x03
    FPRD = 0x04
    FPWR = 0x05
    FPRW = 0x06
    BRD = 0x07
    BWR = 0x08
    BRW = 0x09
    LRD = 0x0A
    LWR = 0x0B
    LRW = 0x0C
    ARMW = 0x0D
    FRMW = 0x0E
    EXT = 0xFF
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_OBJ2002:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJ2003:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJ2005:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJ2020:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJ2200:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJ3XXX:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJ8XXX:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJ9XXX:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJAXXX:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJF000:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJF02X:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_OBJF04X:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_SLAVE_PROP:
    def __init__(self):
        self.wStationAddress = 0 # ushort
        self.wAutoIncAddr = 0 # ushort
        self.achName = "" # string

class DN_EC_T_NOTIFYPARMS:
    def __init__(self):
        self.pCallerData = None # IntPtr
        self.pbyInBuf = None # IntPtr
        self.dwInBufSize = 0 # uint
        self.pbyOutBuf = None # IntPtr
        self.dwOutBufSize = 0 # uint
        self.pdwNumOutData = 0 # uint

class DN_EC_T_WKCERR_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.byCmd = 0 # byte
        self.byRsvd = CEcWrapperPythonTypes.Create_ArrayByType("byte", 3) # byte[]
        self.dwAddr = 0 # uint
        self.wWkcSet = 0 # ushort
        self.wWkcAct = 0 # ushort

class DN_EC_T_FRAME_RSPERR_TYPE(uint32Enum):
    UNDEFINED = 0
    NO_RESPONSE = 1
    WRONG_IDX = 2
    UNEXPECTED = 3
    FRAME_RETRY = 4
    RETRY_FAIL = 5
    FOREIGN_SRC_MAC = 6
    NON_ECAT_FRAME = 7
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_FRAME_RSPERR_DESC:
    def __init__(self):
        self.bIsCyclicFrame = False # bool
        self.EErrorType = 0 # DN_EC_T_FRAME_RSPERR_TYPE
        self.byEcCmdHeaderIdxSet = 0 # byte
        self.byEcCmdHeaderIdxAct = 0 # byte

class DN_EC_T_INITCMD_ERR_TYPE(uint32Enum):
    NO_ERROR = 0
    NO_RESPONSE = 1
    VALIDATION_ERR = 2
    FAILED = 3
    NOT_PRESENT = 4
    ALSTATUS_ERROR = 5
    MBXSLAVE_ERROR = 6
    PDI_WATCHDOG = 7
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_INITCMD_ERR_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.achStateChangeName = "" # string
        self.EErrorType = 0 # DN_EC_T_INITCMD_ERR_TYPE
        self.szComment = "" # string

class DN_EC_T_SLAVE_ERROR_INFO_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.wStatus = 0 # ushort
        self.wStatusCode = 0 # ushort

class DN_EC_T_SLAVES_ERROR_DESC_ENTRY:
    def __init__(self):
        self.wStationAddress = 0 # ushort
        self.wStatus = 0 # ushort
        self.wStatusCode = 0 # ushort
        self.wRes = 0 # ushort

class DN_EC_T_SLAVES_ERROR_DESC:
    def __init__(self):
        self.wCount = 0 # ushort
        self.wRes = 0 # ushort
        self.SlaveError = CEcWrapperPythonTypes.Create_ArrayByType("DN_EC_T_SLAVES_ERROR_DESC_ENTRY", 128) # DN_EC_T_SLAVES_ERROR_DESC_ENTRY[]

class DN_EC_T_MBOX_SDO_ABORT_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.dwErrorCode = 0 # uint
        self.wObjIndex = 0 # ushort
        self.bySubIndex = 0 # byte

class DN_EC_T_MBOX_FOE_ABORT_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.dwErrorCode = 0 # uint
        self.achErrorString = "" # string

class DN_EC_T_MBXRCV_INVALID_DATA_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP

class DN_EC_T_PDIWATCHDOG_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP

class DN_EC_T_SLAVE_NOTSUPPORTED_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP

class DN_EC_T_SLAVE_UNEXPECTED_STATE_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.curState = 0 # DN_EC_T_STATE
        self.expState = 0 # DN_EC_T_STATE

class DN_EC_T_SLAVES_UNEXPECTED_STATE_DESC_ENTRY:
    def __init__(self):
        self.wStationAddress = 0 # ushort
        self.curState = 0 # DN_EC_T_STATE
        self.expState = 0 # DN_EC_T_STATE

class DN_EC_T_SLAVES_UNEXPECTED_STATE_DESC:
    def __init__(self):
        self.wCount = 0 # ushort
        self.wRes = 0 # ushort
        self.SlaveStates = CEcWrapperPythonTypes.Create_ArrayByType("DN_EC_T_SLAVES_UNEXPECTED_STATE_DESC_ENTRY", 128) # DN_EC_T_SLAVES_UNEXPECTED_STATE_DESC_ENTRY[]

class DN_EC_T_EEPROM_CHECKSUM_ERROR_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP

class DN_EC_T_JUNCTION_RED_CHANGE_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.bLineBreak = False # bool
        self.wPort = 0 # ushort

class DN_EC_T_REFCLOCK_PRESENCE_NTFY_DESC:
    def __init__(self):
        self.bPresent = False # bool
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP

class DN_EC_T_DC_SYNC_NTFY_DESC:
    def __init__(self):
        self.IsInSync = 0 # uint
        self.IsNegative = 0 # uint
        self.dwDeviation = 0 # uint
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP

class DN_EC_T_DCM_SYNC_NTFY_DESC:
    def __init__(self):
        self.IsInSync = 0 # uint
        self.nCtlErrorNsecCur = 0 # int
        self.nCtlErrorNsecAvg = 0 # int
        self.nCtlErrorNsecMax = 0 # int

class DN_EC_T_DCX_SYNC_NTFY_DESC:
    def __init__(self):
        self.IsInSync = 0 # uint
        self.nCtlErrorNsecCur = 0 # int
        self.nCtlErrorNsecAvg = 0 # int
        self.nCtlErrorNsecMax = 0 # int
        self.nTimeStampDiff = 0 # int64
        self.dwErrorCode = 0 # uint

class DN_EC_T_SLAVE_STATECHANGED_NTFY_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.newState = 0 # DN_EC_T_STATE

class DN_EC_T_SLAVES_STATECHANGED_NTFY_DESC_ENTRY:
    def __init__(self):
        self.wStationAddress = 0 # ushort
        self.byState = 0 # byte

class DN_EC_T_SLAVES_STATECHANGED_NTFY_DESC:
    def __init__(self):
        self.wCount = 0 # ushort
        self.SlaveStates = CEcWrapperPythonTypes.Create_ArrayByType("DN_EC_T_SLAVES_STATECHANGED_NTFY_DESC_ENTRY", 128) # DN_EC_T_SLAVES_STATECHANGED_NTFY_DESC_ENTRY[]

class DN_EC_T_FRAMELOSS_AFTER_SLAVE_NTFY_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.wPort = 0 # ushort

class DN_EC_T_SB_STATUS_NTFY_DESC:
    def __init__(self):
        self.dwResultCode = 0 # uint
        self.dwSlaveCount = 0 # uint

class DN_EC_T_SB_MISMATCH_DESC:
    def __init__(self):
        self.wPrevFixedAddress = 0 # ushort
        self.wPrevPort = 0 # ushort
        self.wPrevAIncAddress = 0 # ushort
        self.wBusAIncAddress = 0 # ushort
        self.dwBusVendorId = 0 # uint
        self.dwBusProdCode = 0 # uint
        self.dwBusRevisionNo = 0 # uint
        self.dwBusSerialNo = 0 # uint
        self.wBusFixedAddress = 0 # ushort
        self.wIdentificationVal = 0 # ushort
        self.wCfgFixedAddress = 0 # ushort
        self.wCfgAIncAddress = 0 # ushort
        self.dwCfgVendorId = 0 # uint
        self.dwCfgProdCode = 0 # uint
        self.dwCfgRevisionNo = 0 # uint
        self.dwCfgSerialNo = 0 # uint
        self.bIdentValidationError = False # bool
        self.oIdentCmdHdr = CEcWrapperPythonTypes.Create_ArrayByType("ushort", 5) # ushort[]
        self.dwCmdData = 0 # uint
        self.dwCmdVMask = 0 # uint
        self.dwCmdVData = 0 # uint

class DN_EC_T_LINE_CROSSED_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.wInputPort = 0 # ushort

class DN_EC_T_HC_DETECTALLGROUP_NTFY_DESC:
    def __init__(self):
        self.dwResultCode = 0 # uint
        self.dwGroupCount = 0 # uint
        self.dwGroupsPresent = 0 # uint
        self.dwGroupMask = 0 # uint
        self.adwGroupMask = CEcWrapperPythonTypes.Create_ArrayByType("uint", 100) # uint[]

class DN_EC_T_RAWCMDRESPONSE_NTFY_DESC:
    def __init__(self):
        self.dwInvokeId = 0 # uint
        self.dwResult = 0 # uint
        self.dwWkc = 0 # uint
        self.dwCmdIdx = 0 # uint
        self.dwAddr = 0 # uint
        self.dwLength = 0 # uint
        self.pbyData = None # IntPtr

class DN_EC_T_TX_PDO_NTFY_DESC:
    def __init__(self):
        self.wPhysAddr = 0 # uint
        self.dwNumber = 0 # uint
        self.wLen = 0 # uint
        self.pbyData = None # IntPtr

class DN_EC_T_STATECHANGE:
    def __init__(self):
        self.oldState = 0 # DN_EC_T_STATE
        self.newState = 0 # DN_EC_T_STATE

class DN_EC_T_SLAVEREGISTER_TRANSFER_NTFY_DESC:
    def __init__(self):
        self.dwTferId = 0 # uint
        self.dwResult = 0 # uint
        self.bRead = False # bool
        self.wFixedAddr = 0 # ushort
        self.wRegisterOffset = 0 # ushort
        self.wLen = 0 # ushort
        self.pbyData = None # IntPtr

class DN_EC_T_PORT_OPERATION_NTFY_DESC:
    def __init__(self):
        self.dwTferId = 0 # uint
        self.dwResult = 0 # uint
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.wPortStateOld = 0 # ushort
        self.wPortStateNew = 0 # ushort

class DN_EC_T_SLAVE_IDENTIFICATION_NTFY_DESC:
    def __init__(self):
        self.dwTferId = 0 # uint
        self.dwResult = 0 # uint
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.wAdo = 0 # ushort
        self.wValue = 0 # ushort

class DN_EC_T_SLAVE_PRESENCE_NTFY_DESC:
    def __init__(self):
        self.wStationAddress = 0 # ushort
        self.bPresent = 0 # byte

class DN_EC_T_SLAVES_PRESENCE_NTFY_DESC:
    def __init__(self):
        self.wCount = 0 # ushort
        self.SlavePresence = CEcWrapperPythonTypes.Create_ArrayByType("DN_EC_T_SLAVE_PRESENCE_NTFY_DESC", 128) # DN_EC_T_SLAVE_PRESENCE_NTFY_DESC[]

class DN_EC_T_S2SMBX_ERROR_DESC:
    def __init__(self):
        self.SlaveProp = None # DN_EC_T_SLAVE_PROP
        self.wTargetFixedAddress = 0 # ushort
        self.dwErrorCode = 0 # uint

class DN_EC_T_CNF_TYPE(uint32Enum):
    Unknown = 0
    Filename = 1
    Data = 2
    Datadiag = 3
    GenPreopENI = 4
    GenPreopENIWithCRC = 5
    GenOpENI = 6
    None_ = 7
    ConfigData = 8
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_eINFOENTRY(uint32Enum):
    unknown = 0
    pdoffs_in = 1
    pdsize_in = 2
    pdoffs_out = 3
    pdsize_out = 4
    phys_address = 5
    portstate = 6
    dcsupport = 7
    dc64support = 8
    alias_address = 9
    cfgphy_address = 10
    device_name = 11
    ismailbox_slave = 12
    pdoffs_in2 = 21
    pdsize_in2 = 22
    pdoffs_out2 = 23
    pdsize_out2 = 24
    pdoffs_in3 = 31
    pdsize_in3 = 32
    pdoffs_out3 = 33
    pdsize_out3 = 34
    pdoffs_in4 = 41
    pdsize_in4 = 42
    pdoffs_out4 = 43
    pdsize_out4 = 44
    mbx_outsize = 45
    mbx_insize = 46
    mbx_outsize2 = 47
    mbx_insize2 = 48
    isoptional = 49
    ispresent = 50
    esctype = 51
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_SB_SLAVEINFO_REQ_DESC:
    def __init__(self):
        self.eInfoEntry = 0 # DN_EC_T_eINFOENTRY
        self.wAutoIncAddress = 0 # ushort

class DN_EC_T_SB_SLAVEINFO_RES_DESC:
    def __init__(self):
        self.eInfoEntry = 0 # DN_EC_T_eINFOENTRY
        self.dwInfoLength = 0 # uint
        self.pbyInfo = None # IntPtr

class DN_EC_T_SLVSTATISTICS_DESC:
    def __init__(self):
        self.abyInvalidFrameCnt = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]
        self.abyRxErrorCnt = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]
        self.abyFwdRxErrorCnt = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]
        self.byProcessingUnitErrorCnt = 0 # byte
        self.byPdiErrorCnt = 0 # byte
        self.wAlStatusCode = 0 # ushort
        self.abyLostLinkCnt = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]

class DN_EC_T_CFG_SLAVE_INFO:
    def __init__(self):
        self.dwSlaveId = 0 # uint
        self.abyDeviceName = "" # string
        self.dwHCGroupIdx = 0 # uint
        self.bIsPresent = False # bool
        self.bIsHCGroupPresent = False # bool
        self.dwVendorId = 0 # uint
        self.dwProductCode = 0 # uint
        self.dwRevisionNumber = 0 # uint
        self.dwSerialNumber = 0 # uint
        self.wStationAddress = 0 # ushort
        self.wAutoIncAddress = 0 # ushort
        self.dwPdOffsIn = 0 # uint
        self.dwPdSizeIn = 0 # uint
        self.dwPdOffsOut = 0 # uint
        self.dwPdSizeOut = 0 # uint
        self.dwPdOffsIn2 = 0 # uint
        self.dwPdSizeIn2 = 0 # uint
        self.dwPdOffsOut2 = 0 # uint
        self.dwPdSizeOut2 = 0 # uint
        self.dwPdOffsIn3 = 0 # uint
        self.dwPdSizeIn3 = 0 # uint
        self.dwPdOffsOut3 = 0 # uint
        self.dwPdSizeOut3 = 0 # uint
        self.dwPdOffsIn4 = 0 # uint
        self.dwPdSizeIn4 = 0 # uint
        self.dwPdOffsOut4 = 0 # uint
        self.dwPdSizeOut4 = 0 # uint
        self.dwMbxSupportedProtocols = 0 # uint
        self.dwMbxOutSize = 0 # uint
        self.dwMbxInSize = 0 # uint
        self.dwMbxOutSize2 = 0 # uint
        self.dwMbxInSize2 = 0 # uint
        self.bDcSupport = False # bool
        self.wNumProcessVarsInp = 0 # ushort
        self.wNumProcessVarsOutp = 0 # ushort
        self.wPrevStationAddress = 0 # ushort
        self.wPrevPort = 0 # ushort
        self.wIdentifyAdo = 0 # ushort
        self.wIdentifyData = 0 # ushort
        self.byPortDescriptor = 0 # byte
        self.wWkcStateDiagOffsIn = CEcWrapperPythonTypes.Create_ArrayByType("ushort", 4) # ushort[]
        self.wWkcStateDiagOffsOut = CEcWrapperPythonTypes.Create_ArrayByType("ushort", 4) # ushort[]
        self.awMasterSyncUnitIn = CEcWrapperPythonTypes.Create_ArrayByType("ushort", 4) # ushort[]
        self.awMasterSyncUnitOut = CEcWrapperPythonTypes.Create_ArrayByType("ushort", 4) # ushort[]
        self.bDisabled = False # bool
        self.bDisconnected = False # bool
        self.bExtended = False # bool

class DN_EC_T_CFG_SLAVE_EOE_INFO:
    def __init__(self):
        self.dwSlaveId = 0 # uint
        self.bMacAddr = False # bool
        self.abyMacAddr = CEcWrapperPythonTypes.Create_ArrayByType("byte", 6) # byte[]
        self.bIpAddr = False # bool
        self.abyIpAddr = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]
        self.bSubnetMask = False # bool
        self.abySubnetMask = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]
        self.bDefaultGateway = False # bool
        self.abyDefaultGateway = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]
        self.bDnsServer = False # bool
        self.abyDnsServer = CEcWrapperPythonTypes.Create_ArrayByType("byte", 4) # byte[]
        self.bDnsName = False # bool
        self.szDnsName = "" # string

class DN_EC_T_BUS_SLAVE_INFO:
    def __init__(self):
        self.dwSlaveId = 0 # uint
        self.adwPortSlaveIds = CEcWrapperPythonTypes.Create_ArrayByType("uint", 4) # uint[]
        self.wPortState = 0 # ushort
        self.wAutoIncAddress = 0 # ushort
        self.bDcSupport = False # bool
        self.bDc64Support = False # bool
        self.dwVendorId = 0 # uint
        self.dwProductCode = 0 # uint
        self.dwRevisionNumber = 0 # uint
        self.dwSerialNumber = 0 # uint
        self.byESCType = 0 # byte
        self.byESCRevision = 0 # byte
        self.wESCBuild = 0 # ushort
        self.byPortDescriptor = 0 # byte
        self.wFeaturesSupported = 0 # ushort
        self.wStationAddress = 0 # ushort
        self.wAliasAddress = 0 # ushort
        self.wAlStatus = 0 # ushort
        self.wAlStatusCode = 0 # ushort
        self.dwSystemTimeDifference = 0 # uint
        self.wMbxSupportedProtocols = 0 # ushort
        self.wDlStatus = 0 # ushort
        self.wPrevPort = 0 # ushort
        self.wIdentifyData = 0 # ushort
        self.bLineCrossed = False # bool
        self.dwSlaveDelay = 0 # uint
        self.dwPropagDelay = 0 # uint
        self.bIsRefClock = False # bool
        self.bIsDeviceEmulation = False # bool
        self.wLineCrossedFlags = 0 # ushort

class DN_EC_T_TRACE_DATA_INFO:
    def __init__(self):
        self.pbyData = None # IntPtr
        self.dwOffset = 0 # uint
        self.wSize = 0 # ushort

class DN_EC_T_BUS_DIAGNOSIS_INFO:
    def __init__(self):
        self.dwCRC32ConfigCheckSum = 0 # uint
        self.dwNumSlavesFound = 0 # uint
        self.dwNumDCSlavesFound = 0 # uint
        self.dwNumCfgSlaves = 0 # uint
        self.dwNumMbxSlaves = 0 # uint
        self.dwTXFrames = 0 # uint
        self.dwRXFrames = 0 # uint
        self.dwLostFrames = 0 # uint
        self.dwCyclicFrames = 0 # uint
        self.dwCyclicDatagrams = 0 # uint
        self.dwAcyclicFrames = 0 # uint
        self.dwAcyclicDatagrams = 0 # uint
        self.dwClearCounters = 0 # uint
        self.dwRes = CEcWrapperPythonTypes.Create_ArrayByType("uint", 4) # uint[]

class DN_EC_T_STATISTIC:
    def __init__(self):
        self.dwTotal = 0 # uint
        self.dwLast = 0 # uint

class DN_EC_T_STATISTIC_TRANSFER:
    def __init__(self):
        self.Cnt = None # DN_EC_T_STATISTIC
        self.Bytes = None # DN_EC_T_STATISTIC

class DN_EC_T_STATISTIC_TRANSFER_DUPLEX:
    def __init__(self):
        self.Read = None # DN_EC_T_STATISTIC_TRANSFER
        self.Write = None # DN_EC_T_STATISTIC_TRANSFER

class DN_EC_T_MAILBOX_STATISTICS:
    def __init__(self):
        self.Aoe = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX
        self.Coe = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX
        self.Eoe = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX
        self.Foe = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX
        self.Soe = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX
        self.Voe = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX
        self.RawMbx = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX
        self.aRes = None # DN_EC_T_STATISTIC_TRANSFER_DUPLEX

class DN_EC_T_MASTER_INFO:
    def __init__(self):
        self.dwMasterVersion = 0 # uint
        self.BusDiagnosisInfo = None # DN_EC_T_BUS_DIAGNOSIS_INFO
        self.MailboxStatistics = None # DN_EC_T_MAILBOX_STATISTICS

class DN_EC_T_RAS_CONNECTION_INFO:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_MSU_INFO:
    def __init__(self):
        self.wMsuId = 0 # ushort
        self.dwBitOffsIn = 0 # uint
        self.dwBitSizeIn = 0 # uint
        self.dwBitOffsOut = 0 # uint
        self.dwBitSizeOut = 0 # uint
        self.wWkcStateDiagOffsIn = 0 # ushort
        self.wWkcStateDiagOffsOut = 0 # ushort

class DN_EC_T_REGISTERRESULTS:
    def __init__(self):
        self.dwClntId = 0 # uint
        self.pbyPDIn = None # IntPtr
        self.dwPDInSize = 0 # uint
        self.pbyPDOut = None # IntPtr
        self.dwPDOutSize = 0 # uint

class DN_EC_T_MASTER_RED_PARMS:
    def __init__(self):
        self.bEnabled = False # bool
        self.wMasterPdOutSize = 0 # ushort
        self.wMasterPdInSize = 0 # ushort
        self.dwMaxAcycFramesPerCycle = 0 # uint
        self.bUpdateSlavePdOut = False # bool
        self.bUpdateSlavePdIn = False # bool

class DN_EC_T_DC_CONFIGURE:
    def __init__(self):
        self.dwClntId = 0 # uint
        self.dwTimeout = 0 # uint
        self.dwDevLimit = 0 # uint
        self.dwSettleTime = 0 # uint
        self.dwTotalBurstLength = 0 # uint
        self.dwBurstBulk = 0 # uint
        self.bBulkInLinkLayer = False # bool
        self.bAcycDistributionDisabled = False # bool
        self.dwDcStartTimeGrid = 0 # uint
        self.bDcInitBeforeSlaveStateChange = False # bool

class DN_EC_T_DCM_MODE(uint32Enum):
    Off = 0
    BusShift = 1
    MasterShift = 2
    LinkLayerRefClock = 3
    MasterRefClock = 4
    Dcx = 5
    MasterShiftByApp = 6
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_DC_STARTTIME_CB_DESC:
    def __init__(self):
        self.pvContext = None # IntPtr

class DN_EC_T_DCM_CONFIG_BUSSHIFT:
    def __init__(self):
        self.nCtlSetVal = 0 # int
        self.nCtlGain = 0 # int
        self.nCtlDriftErrorGain = 0 # int
        self.nMaxValidVal = 0 # int
        self.bLogEnabled = False # bool
        self.dwInSyncLimit = 0 # uint
        self.dwInSyncSettleTime = 0 # uint
        self.bCtlOff = False # bool
        self.bUseDcLoopCtlStdValues = False # bool
        self.dwInSyncStartDelayCycle = 0 # uint

class DN_EC_T_DCM_CONFIG_MASTERSHIFT:
    def __init__(self):
        self.nCtlSetVal = 0 # int
        self.nCtlGain = 0 # int
        self.nCtlDriftErrorGain = 0 # int
        self.nMaxValidVal = 0 # int
        self.bLogEnabled = False # bool
        self.dwInSyncLimit = 0 # uint
        self.dwInSyncSettleTime = 0 # uint
        self.bCtlOff = False # bool
        self.dwInSyncStartDelayCycle = 0 # uint

class DN_EC_T_DCM_CONFIG_LINKLAYERREFCLOCK:
    def __init__(self):
        self.nCtlSetVal = 0 # int
        self.bLogEnabled = False # bool
        self.DcStartTimeCallbackDesc = None # DN_EC_T_DC_STARTTIME_CB_DESC

class DN_EC_T_DCM_CONFIG_MASTERREFCLOCK:
    def __init__(self):
        self.nCtlSetVal = 0 # int
        self.bLogEnabled = False # bool
        self.dwInSyncLimit = 0 # uint
        self.dwInSyncSettleTime = 0 # uint
        self.dwInSyncStartDelayCycle = 0 # uint

class DN_EC_T_DCM_CONFIG_DCX:
    def __init__(self):
        self.MasterShift = None # DN_EC_T_DCM_CONFIG_MASTERSHIFT
        self.nCtlSetVal = 0 # int
        self.nCtlGain = 0 # int
        self.nCtlDriftErrorGain = 0 # int
        self.nMaxValidVal = 0 # int
        self.bLogEnabled = False # bool
        self.dwInSyncLimit = 0 # uint
        self.dwInSyncSettleTime = 0 # uint
        self.bCtlOff = False # bool
        self.wExtClockFixedAddr = 0 # ushort
        self.dwExtClockTimeout = 0 # uint
        self.dwInSyncStartDelayCycle = 0 # uint
        self.dwMaxErrCompensableOnExtClockReconnect = 0 # uint

class DN_EC_T_DCM_CONFIG:
    def __init__(self):
        self.eMode = 0 # DN_EC_T_DCM_MODE
        self.BusShift = None # DN_EC_T_DCM_CONFIG_BUSSHIFT
        self.MasterShift = None # DN_EC_T_DCM_CONFIG_MASTERSHIFT
        self.LinkLayerRefClock = None # DN_EC_T_DCM_CONFIG_LINKLAYERREFCLOCK
        self.MasterRefClock = None # DN_EC_T_DCM_CONFIG_MASTERREFCLOCK
        self.Dcx = None # DN_EC_T_DCM_CONFIG_DCX

class DN_EC_T_GET_SLAVE_INFO:
    def __init__(self):
        self.dwScanBusStatus = 0 # uint
        self.dwVendorId = 0 # uint
        self.dwProductCode = 0 # uint
        self.dwRevisionNumber = 0 # uint
        self.dwSerialNumber = 0 # uint
        self.wPortState = 0 # ushort
        self.bDcSupport = False # bool
        self.bDc64Support = False # bool
        self.wAliasAddress = 0 # ushort
        self.wPhysAddress = 0 # ushort
        self.dwPdOffsIn = 0 # uint
        self.dwPdSizeIn = 0 # uint
        self.dwPdOffsOut = 0 # uint
        self.dwPdSizeOut = 0 # uint
        self.dwPdOffsIn2 = 0 # uint
        self.dwPdSizeIn2 = 0 # uint
        self.dwPdOffsOut2 = 0 # uint
        self.dwPdSizeOut2 = 0 # uint
        self.dwPdOffsIn3 = 0 # uint
        self.dwPdSizeIn3 = 0 # uint
        self.dwPdOffsOut3 = 0 # uint
        self.dwPdSizeOut3 = 0 # uint
        self.dwPdOffsIn4 = 0 # uint
        self.dwPdSizeIn4 = 0 # uint
        self.dwPdOffsOut4 = 0 # uint
        self.dwPdSizeOut4 = 0 # uint
        self.wCfgPhyAddress = 0 # ushort
        self.abyDeviceName = "" # string
        self.bIsMailboxSlave = False # bool
        self.dwMbxOutSize = 0 # uint
        self.dwMbxInSize = 0 # uint
        self.dwMbxOutSize2 = 0 # uint
        self.dwMbxInSize2 = 0 # uint
        self.dwErrorCode = 0 # uint
        self.dwSBErrorCode = 0 # uint
        self.byPortDescriptor = 0 # byte
        self.byESCType = 0 # byte
        self.wSupportedMbxProtocols = 0 # ushort
        self.wAlStatusValue = 0 # ushort
        self.wAlStatusCode = 0 # ushort
        self.bIsOptional = False # bool
        self.bIsPresent = False # bool
        self.wNumProcessVarsInp = 0 # ushort
        self.wNumProcessVarsOutp = 0 # ushort
        self.dwSlaveId = 0 # uint
        self.bIsHCGroupPresent = False # bool
        self.aPortSlaveIds = CEcWrapperPythonTypes.Create_ArrayByType("uint", 4) # uint[]
        self.dwSystemTimeDifference = 0 # uint

class DN_EC_T_PROCESS_VAR_INFO:
    def __init__(self):
        self.szName = "" # string
        self.wDataType = 0 # ushort
        self.wFixedAddr = 0 # ushort
        self.nBitSize = 0 # int
        self.nBitOffs = 0 # int
        self.bIsInputData = False # bool

class DN_EC_T_PROCESS_VAR_INFO_EX:
    def __init__(self):
        self.szName = "" # string
        self.wDataType = 0 # ushort
        self.wFixedAddr = 0 # ushort
        self.nBitSize = 0 # int
        self.nBitOffs = 0 # int
        self.bIsInputData = False # bool
        self.wIndex = 0 # ushort
        self.wSubIndex = 0 # ushort
        self.wPdoIndex = 0 # ushort
        self.wWkcStateDiagOffs = 0 # ushort
        self.wMasterSyncUnit = 0 # ushort
        self.wRes1 = 0 # ushort
        self.dwRes1 = 0 # uint

class DN_EC_T_COE_ODLIST_TYPE(uint32Enum):
    Lengths = 0
    ALL = 1
    RxPdoMap = 2
    TxPdoMap = 3
    StoredFRepl = 4
    StartupParm = 5
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_COE_EMERGENCY:
    def __init__(self):
        self.wErrorCode = 0 # ushort
        self.byErrorRegister = 0 # byte
        self.abyData = CEcWrapperPythonTypes.Create_ArrayByType("byte", 5) # byte[]
        self.wStationAddress = 0 # ushort

class DN_EC_T_MBX_DATA_COE:
    def __init__(self):
        self.wStationAddress = 0 # ushort
        self.wIndex = 0 # ushort
        self.bySubIndex = 0 # byte
        self.bCompleteAccess = False # bool

class DN_EC_T_MBX_DATA_FOE:
    def __init__(self):
        self.dwTransferredBytes = 0 # uint
        self.dwRequestedBytes = 0 # uint
        self.dwBusyDone = 0 # uint
        self.dwBusyEntire = 0 # uint
        self.szBusyComment = "" # string
        self.dwFileSize = 0 # uint

class DN_EC_T_SOE_NOTIFICATION:
    def __init__(self):
        self.wHeader = 0 # ushort
        self.wIdn = 0 # ushort
        self.abyData = CEcWrapperPythonTypes.Create_ArrayByType("byte", 5) # byte[]
        self.wStationAddress = 0 # ushort

class DN_EC_T_SOE_EMERGENCY:
    def __init__(self):
        self.wHeader = 0 # ushort
        self.abyData = CEcWrapperPythonTypes.Create_ArrayByType("byte", 5) # byte[]
        self.wStationAddress = 0 # ushort

class DN_EC_T_AOE_NETID:
    def __init__(self):
        self.dwNotSupported = 0 # eval limitation

class DN_EC_T_AOE_CMD_RESPONSE:
    def __init__(self):
        self.dwErrorCode = 0 # uint
        self.dwCmdResult = 0 # uint
        self.dwRsvd = 0 # uint

class DN_EC_T_MBXTFER_TYPE(uint32Enum):
    COE_SDO_DOWNLOAD = 0
    COE_SDO_UPLOAD = 1
    COE_GETODLIST = 2
    COE_GETOBDESC = 3
    COE_GETENTRYDESC = 4
    COE_EMERGENCY = 5
    COE_RX_PDO = 6
    FOE_FILE_UPLOAD = 7
    FOE_FILE_DOWNLOAD = 8
    SOE_READREQUEST = 9
    SOE_READRESPONSE = 10
    SOE_WRITEREQUEST = 11
    SOE_WRITERESPONSE = 12
    SOE_NOTIFICATION = 13
    SOE_EMERGENCY = 14
    VOE_MBX_READ = 15
    VOE_MBX_WRITE = 16
    AOE_READ = 17
    AOE_WRITE = 18
    AOE_READWRITE = 19
    AOE_WRITECONTROL = 20
    RAWMBX = 21
    FOE_SEG_DOWNLOAD = 22
    FOE_SEG_UPLOAD = 23
    S2SMBX = 24
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_MBXTFER_STATUS(uint32Enum):
    Idle = 0
    Pend = 1
    TferDone = 2
    TferReqError = 3
    TferWaitingForContinue = 4
    BCppDummy = 0xFFFFFFFF

class DN_EC_T_USER_JOB(uint32Enum):
    Undefined = 0
    ProcessAllRxFrames = 1
    SendAllCycFrames = 2
    RunMcSm = 3
    MasterTimer = 4
    FlushQueuedCmds = 5
    SendAcycFrames = 6
    SendCycFramesByTaskId = 7
    MasterTimerMinimal = 8
    ProcessRxFramesByTaskId = 9
    ProcessAcycRxFrames = 10
    SwitchEoeFrames = 11
    StampSendAllCycFrames = 22
    StampSendCycFramesByTaskId = 27
    SimulatorTimer = 32
    BCppDummy = 0xFFFFFFFF

class DN_EC_PTS_STATE(uint32Enum):
    ePtsStateNone = 0x0000
    ePtsStateNotRunning = 0x0001
    ePtsStateRunningDisabled = 0x0002
    ePtsStateRunningEnabled = 0x0003
    ePtsStateDummy = 0xFFFFFFFF

class DN_EC_T_ADS_ADAPTER_START_PARMS:
    def __init__(self):
        self.dwSignature = 0 # uint
        self.dwSize = 0 # uint
        self.cpuAffinityMask = 0 # ulong
        self.dwThreadPriority = 0 # uint
        self.targetNetID = None # DN_EC_T_AOE_NETID
        self.targetPort = 0 # ushort

class DN_EC_T_SLAVE_SELECTION(uint32Enum):
    eSlaveSelectionDummy = 0xFFFFFFFF

class DN_ETHERNET_ADDRESS:
    def __init__(self):
        self.b = CEcWrapperPythonTypes.Create_ArrayByType("byte", 6) # byte[]

class DN_EC_T_LOG_PARMS:
    def __init__(self):
        self.dwLogLevel = 0 # uint

class DN_EC_T_DEFTYPE(uint32Enum):
    NULL = 0x0000
    BOOLEAN = 0x0001
    INTEGER8 = 0x0002
    INTEGER16 = 0x0003
    INTEGER32 = 0x0004
    UNSIGNED8 = 0x0005
    UNSIGNED16 = 0x0006
    UNSIGNED32 = 0x0007
    REAL32 = 0x0008
    VISIBLESTRING = 0x0009
    OCTETSTRING = 0x000A
    UNICODESTRING = 0x000B
    TIMEOFDAY = 0x000C
    TIMEDIFFERENCE = 0x000D
    DOMAIN = 0x000F
    INTEGER24 = 0x0010
    REAL64 = 0x0011
    INTEGER40 = 0x0012
    INTEGER48 = 0x0013
    INTEGER56 = 0x0014
    INTEGER64 = 0x0015
    UNSIGNED24 = 0x0016
    UNSIGNED40 = 0x0018
    UNSIGNED48 = 0x0019
    UNSIGNED56 = 0x001A
    UNSIGNED64 = 0x001B
    GUID = 0x001D
    BYTE = 0x001E
    WORD = 0x001F
    DWORD = 0x0020
    PDOMAPPING = 0x0021
    IDENTITY = 0x0023
    COMMAND = 0x0025
    PDOCOMPAR = 0x0027
    ENUM = 0x0028
    SMPAR = 0x0029
    RECORD = 0x002A
    BACKUP_PARAMETER = 0x002B
    MODULAR_DEVICE_PROFILE = 0x002C
    BITARR8 = 0x002D
    BITARR16 = 0x002E
    BITARR32 = 0x002F
    BIT1 = 0x0030
    BIT2 = 0x0031
    BIT3 = 0x0032
    BIT4 = 0x0033
    BIT5 = 0x0034
    BIT6 = 0x0035
    BIT7 = 0x0036
    BIT8 = 0x0037
    BIT9 = 0x0038
    BIT10 = 0x0039
    BIT11 = 0x003A
    BIT12 = 0x003B
    BIT13 = 0x003C
    BIT14 = 0x003D
    BIT15 = 0x003E
    BIT16 = 0x003F
    ARRAY_OF_BYTE = 0x000A
    ARRAY_OF_UINT = 0x000B
    ARRAY_OF_INT = 0x0260
    ARRAY_OF_SINT = 0x0261
    ARRAY_OF_DINT = 0x0262
    ARRAY_OF_UDINT = 0x0263
    ERROR_SETTING = 0x0281
    HISTORY = 0x0282
    DIAGNOSIS_OBJECT = 0x0282
    EXTERNAL_SYNC_STATUS = 0x0283
    EXTERNAL_SYNC_SETTINGS = 0x0284
    FSOEFRAME = 0x0285
    FSOECOMMPAR = 0x0286

class Conv_DN_EC_T_DEFTYPE:
    @staticmethod
    def CreateMap():
        map_ = [
            DN_EC_T_DEFTYPE.NULL, "NULL",
            DN_EC_T_DEFTYPE.BOOLEAN, "BOOLEAN",
            DN_EC_T_DEFTYPE.INTEGER8, "INTEGER8",
            DN_EC_T_DEFTYPE.INTEGER16, "INTEGER16",
            DN_EC_T_DEFTYPE.INTEGER32, "INTEGER32",
            DN_EC_T_DEFTYPE.UNSIGNED8, "UNSIGNED8",
            DN_EC_T_DEFTYPE.UNSIGNED16, "UNSIGNED16",
            DN_EC_T_DEFTYPE.UNSIGNED32, "UNSIGNED32",
            DN_EC_T_DEFTYPE.REAL32, "REAL32",
            DN_EC_T_DEFTYPE.VISIBLESTRING, "VISIBLESTRING",
            DN_EC_T_DEFTYPE.OCTETSTRING, "OCTETSTRING",
            DN_EC_T_DEFTYPE.UNICODESTRING, "UNICODESTRING",
            DN_EC_T_DEFTYPE.TIMEOFDAY, "TIMEOFDAY",
            DN_EC_T_DEFTYPE.TIMEDIFFERENCE, "TIMEDIFFERENCE",
            DN_EC_T_DEFTYPE.DOMAIN, "DOMAIN",
            DN_EC_T_DEFTYPE.INTEGER24, "INTEGER24",
            DN_EC_T_DEFTYPE.REAL64, "REAL64",
            DN_EC_T_DEFTYPE.INTEGER40, "INTEGER40",
            DN_EC_T_DEFTYPE.INTEGER48, "INTEGER48",
            DN_EC_T_DEFTYPE.INTEGER56, "INTEGER56",
            DN_EC_T_DEFTYPE.INTEGER64, "INTEGER64",
            DN_EC_T_DEFTYPE.UNSIGNED24, "UNSIGNED24",
            DN_EC_T_DEFTYPE.UNSIGNED40, "UNSIGNED40",
            DN_EC_T_DEFTYPE.UNSIGNED48, "UNSIGNED48",
            DN_EC_T_DEFTYPE.UNSIGNED56, "UNSIGNED56",
            DN_EC_T_DEFTYPE.UNSIGNED64, "UNSIGNED64",
            DN_EC_T_DEFTYPE.GUID, "GUID",
            DN_EC_T_DEFTYPE.BYTE, "BYTE",
            DN_EC_T_DEFTYPE.WORD, "WORD",
            DN_EC_T_DEFTYPE.DWORD, "DWORD",
            DN_EC_T_DEFTYPE.PDOMAPPING, "PDOMAPPING",
            DN_EC_T_DEFTYPE.IDENTITY, "IDENTITY",
            DN_EC_T_DEFTYPE.COMMAND, "COMMAND",
            DN_EC_T_DEFTYPE.PDOCOMPAR, "PDOCOMPAR",
            DN_EC_T_DEFTYPE.ENUM, "ENUM",
            DN_EC_T_DEFTYPE.SMPAR, "SMPAR",
            DN_EC_T_DEFTYPE.RECORD, "RECORD",
            DN_EC_T_DEFTYPE.BACKUP_PARAMETER, "BACKUP_PARAMETER",
            DN_EC_T_DEFTYPE.MODULAR_DEVICE_PROFILE, "MODULAR_DEVICE_PROFILE",
            DN_EC_T_DEFTYPE.BITARR8, "BITARR8",
            DN_EC_T_DEFTYPE.BITARR16, "BITARR16",
            DN_EC_T_DEFTYPE.BITARR32, "BITARR32",
            DN_EC_T_DEFTYPE.BIT1, "BIT1",
            DN_EC_T_DEFTYPE.BIT2, "BIT2",
            DN_EC_T_DEFTYPE.BIT3, "BIT3",
            DN_EC_T_DEFTYPE.BIT4, "BIT4",
            DN_EC_T_DEFTYPE.BIT5, "BIT5",
            DN_EC_T_DEFTYPE.BIT6, "BIT6",
            DN_EC_T_DEFTYPE.BIT7, "BIT7",
            DN_EC_T_DEFTYPE.BIT8, "BIT8",
            DN_EC_T_DEFTYPE.BIT9, "BIT9",
            DN_EC_T_DEFTYPE.BIT10, "BIT10",
            DN_EC_T_DEFTYPE.BIT11, "BIT11",
            DN_EC_T_DEFTYPE.BIT12, "BIT12",
            DN_EC_T_DEFTYPE.BIT13, "BIT13",
            DN_EC_T_DEFTYPE.BIT14, "BIT14",
            DN_EC_T_DEFTYPE.BIT15, "BIT15",
            DN_EC_T_DEFTYPE.BIT16, "BIT16",
            DN_EC_T_DEFTYPE.ARRAY_OF_BYTE, "ARRAY_OF_BYTE",
            DN_EC_T_DEFTYPE.ARRAY_OF_UINT, "ARRAY_OF_UINT",
            DN_EC_T_DEFTYPE.ARRAY_OF_INT, "ARRAY_OF_INT",
            DN_EC_T_DEFTYPE.ARRAY_OF_SINT, "ARRAY_OF_SINT",
            DN_EC_T_DEFTYPE.ARRAY_OF_DINT, "ARRAY_OF_DINT",
            DN_EC_T_DEFTYPE.ARRAY_OF_UDINT, "ARRAY_OF_UDINT",
            DN_EC_T_DEFTYPE.ERROR_SETTING, "ERROR_SETTING",
            DN_EC_T_DEFTYPE.HISTORY, "HISTORY",
            DN_EC_T_DEFTYPE.DIAGNOSIS_OBJECT, "DIAGNOSIS_OBJECT",
            DN_EC_T_DEFTYPE.EXTERNAL_SYNC_STATUS, "EXTERNAL_SYNC_STATUS",
            DN_EC_T_DEFTYPE.EXTERNAL_SYNC_SETTINGS, "EXTERNAL_SYNC_SETTINGS",
            DN_EC_T_DEFTYPE.FSOEFRAME, "FSOEFRAME",
            DN_EC_T_DEFTYPE.FSOECOMMPAR, "FSOECOMMPAR",
        ]
        return map_

    @staticmethod
    def TypeToString(type_):
        map_ = Conv_DN_EC_T_DEFTYPE.CreateMap()
        for i in range(0, len(map_), 2):
            if (map_[i] == type_):
                return map_[i + 1]
        return "NULL"

    @staticmethod
    def TypeFromString(type_):
        map_ = Conv_DN_EC_T_DEFTYPE.CreateMap()
        for i in range(0, len(map_), 2):
            if (map_[i + 1] == type_):
                return map_[i]
        return DN_EC_T_DEFTYPE.NULL

class DN_ESC_SII_REG(uint32Enum):
    PDICONTROL = 0x0000
    PDICONFIG = 0x0001
    SYNCIMPULSELENGTH = 0x0002
    EXTENDEDPDICONFIG = 0x0003
    ALIASADDRESS = 0x0004
    CHECKSUM = 0x0007
    VENDORID = 0x0008
    PRODUCTCODE = 0x000A
    REVISIONNUMBER = 0x000C
    REVISIONNUMBER_LO = 0x000C
    REVISIONNUMBER_HI = 0x000D
    SERIALNUMBER = 0x000E
    BOOT_RECV_MBX = 0x0014
    BOOT_RECV_MBX_OFFSET = 0x0014
    BOOT_RECV_MBX_SIZE = 0x0015
    BOOT_SEND_MBX = 0x0016
    BOOT_SEND_MBX_OFFSET = 0x0016
    BOOT_SEND_MBX_SIZE = 0x0017
    STD_RECV_MBX = 0x0018
    STD_RECV_MBX_OFFSET = 0x0018
    STD_RECV_MBX_SIZE = 0x0019
    STD_SEND_MBX = 0x001A
    STD_SEND_MBX_OFFSET = 0x001A
    STD_SEND_MBX_SIZE = 0x001B
    MBX_PROTOCOL = 0x001C
    FIRSTCATEGORYHDR = 0x0040

class DN_ATEMRAS_ACCESS_LEVEL(uint32Enum):
    ALLOW_ALL = 1
    READWRITE = 2
    READONLY = 3
    BLOCK_ALL = 4

class DN_EC_LOG_LEVEL(uint32Enum):
    SILENT = 0
    ANY = 1
    CRITICAL = 2
    ERROR = 3
    WARNING = 4
    INFO = 5
    INFO_API = 6
    VERBOSE = 7
    VERBOSE_CYC = 8
    UNDEFINED = 0xFFFFFFFF

  #// @CODEGENERATOR_IMPL_END@
