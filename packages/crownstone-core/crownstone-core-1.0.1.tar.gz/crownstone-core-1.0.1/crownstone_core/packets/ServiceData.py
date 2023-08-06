from crownstone_core.packets.CrownstoneErrors import CrownstoneErrors
from crownstone_core.packets.serviceDataParsers.parsers import parseOpCode5, parseOpCode6, parseOpCode4, parseOpCode3
from crownstone_core.protocol.BluenetTypes import DeviceType
from crownstone_core.protocol.SwitchState import SwitchState
from crownstone_core.util.EncryptionHandler import EncryptionHandler


class ServiceData:
    
    def __init__(self, data, unencrypted = False):
        self.opCode = 0
        self.dataType = 0
        self.crownstoneId = 0
        self.switchState = SwitchState(0)
        self.flagsBitmask = 0
        self.temperature = 0
        self.powerFactor = 1
        self.powerUsageReal = 0
        self.powerUsageApparent = 0
        self.accumulatedEnergy = 0
        self.setupMode = False
        self.stateOfExternalCrownstone = False
        self.data = None
        self.dataString = ""
        self.dimmerReady = False
        self.dimmingAllowed = False
        self.hasError = False
        self.switchLocked = False
        self.partialTimestamp = 0
        self.timestamp = -1
        self.validation = 0x00  # Will be 0xFAif it is set.
   
        self.errorTimestamp = 0
        self.errorsBitmask = 0
        self.errorMode = False
        self.timeIsSet = False
        self.switchCraftEnabled = False
        self.uniqueIdentifier = 0
   
        self.validData = False
        self.dataReadyForUse = False  # decryption is successful if this is true

        self.tapToToggleEnabled = False
        self.behaviourEnabled = True
        self.behaviourOverridden = False
        self.behaviourMasterHash = 0
    
        self.deviceType = DeviceType.UNDEFINED
        self.rssiOfExternalCrownstone = 0
 
        self.encryptedData = []
        self.encryptedDataStartIndex = 0
        
        self.data = data
        self.parse(unencrypted)

    def parse(self, unencrypted=False):
        self.validData = True
        if len(self.data) == 18:
            self.opCode = self.data[0]
            self.encryptedData = self.data[2:]
            self.encryptedDataStartIndex = 2
        elif len(self.data) == 17:
            self.opCode = self.data[0]
            self.encryptedData = self.data[1:]
            self.encryptedDataStartIndex = 1
        elif len(self.data) == 16 and unencrypted:
            self.encryptedData = self.data
            self.opCode = 7
        else:
            self.validData = False

        if self.validData:
            if self.opCode == 3:
                parseOpCode3(self, self.encryptedData)
            elif self.opCode == 4:
                parseOpCode4(self, self.encryptedData)
            elif self.opCode == 5 or self.opCode == 7:
                self.getDeviceTypeFromPublicData()
                parseOpCode5(self, self.encryptedData)
            elif self.opCode == 6:
                self.getDeviceTypeFromPublicData()
                parseOpCode6(self, self.encryptedData)
            else:
                self.getDeviceTypeFromPublicData()
                parseOpCode5(self, self.encryptedData)
            
    def getDeviceTypeFromPublicData(self):
        if len(self.data) == 18:
            if DeviceType.has_value(self.data[1]):
                self.deviceType = type

    def isInSetupMode(self):
        if not self.validData:
            return False
    
        return self.setupMode
    
    
    def getDictionary(self):
        errorsDictionary = CrownstoneErrors(self.errorsBitmask).getDictionary()
        
        returnDict = {}
        
        returnDict["opCode"]                    = self.opCode
        returnDict["dataType"]                  = self.dataType
        returnDict["stateOfExternalCrownstone"] = self.stateOfExternalCrownstone
        returnDict["hasError"]                  = self.hasError
        returnDict["setupMode"]                 = self.isInSetupMode()
        returnDict["id"]                        = self.crownstoneId
        returnDict["switchState"]               = self.switchState.raw
        returnDict["flagsBitmask"]              = self.flagsBitmask
        returnDict["temperature"]               = self.temperature
        returnDict["powerFactor"]               = self.powerFactor
        returnDict["powerUsageReal"]            = self.powerUsageReal
        returnDict["powerUsageApparent"]        = self.powerUsageApparent
        returnDict["accumulatedEnergy"]         = self.accumulatedEnergy
        returnDict["timestamp"]                 = self.timestamp
        returnDict["dimmerReady"]               = self.dimmerReady
        returnDict["dimmingAllowed"]            = self.dimmingAllowed
        returnDict["switchLocked"]              = self.switchLocked
        returnDict["switchCraftEnabled"]        = self.switchCraftEnabled
        returnDict["tapToToggleEnabled"]        = self.tapToToggleEnabled
        returnDict["behaviourEnabled"]          = self.behaviourEnabled
        returnDict["behaviourOverridden"]       = self.behaviourOverridden
        returnDict["behaviourMasterHash"]       = self.behaviourMasterHash

        returnDict["errorMode"]                 = self.errorMode
        returnDict["errors"]                    = errorsDictionary
    
        returnDict["uniqueElement"]             =  self.uniqueIdentifier
        returnDict["timeIsSet"]                 =  self.timeIsSet

        returnDict["rssiOfExternalCrownstone"]  = self.rssiOfExternalCrownstone
    
        return returnDict
    
    
    def getSummary(self, address):
        errorsDictionary = CrownstoneErrors(self.errorsBitmask).getDictionary()
    
        returnDict = {}
    
        returnDict["id"] = self.crownstoneId
        returnDict["address"] = address
        returnDict["setupMode"] = self.isInSetupMode()
        returnDict["switchState"] = self.switchState.raw
        returnDict["temperature"] = self.temperature
        returnDict["powerFactor"] = self.powerFactor
        returnDict["powerUsageReal"] = self.powerUsageReal
        returnDict["powerUsageApparent"] = self.powerUsageApparent
        returnDict["accumulatedEnergy"] = self.accumulatedEnergy
        returnDict["dimmerReady"] = self.dimmerReady
        returnDict["dimmingAllowed"] = self.dimmingAllowed
        returnDict["switchLocked"] = self.switchLocked
        returnDict["switchCraftEnabled"] = self.switchCraftEnabled
        returnDict["timeIsSet"] = self.timeIsSet
        returnDict["timestamp"] = self.timestamp
        returnDict["hasError"] = self.hasError
        returnDict["errorMode"] = self.errorMode
        returnDict["errors"] = errorsDictionary
    
        return returnDict


    def decrypt(self, keyHexString):
        if self.validData and len(self.encryptedData) == 16 and len(keyHexString) >= 16:
            if not self.setupMode:
                result = EncryptionHandler.decryptECB(self.encryptedData, keyHexString)

                for i in range(0, len(self.encryptedData)):
                    self.data[i + self.encryptedDataStartIndex] = result[i]

                self.parse()
            self.dataReadyForUse = True
        else:
            self.dataReadyForUse = False

