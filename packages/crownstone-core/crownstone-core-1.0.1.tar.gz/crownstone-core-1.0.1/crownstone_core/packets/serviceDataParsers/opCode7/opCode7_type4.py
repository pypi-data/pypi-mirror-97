import time

from crownstone_core.protocol.SwitchState import SwitchState
from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.DataStepper import DataStepper
from crownstone_core.util.Timestamp import reconstructTimestamp


def parseOpCode7_type4(serviceData, data):
    if len(data) == 16:
        # dataType = data[0]
        
        serviceData.stateOfExternalCrownstone = False

        payload = DataStepper(data)

        payload.skip() # first byte is the  datatype.
        serviceData.crownstoneId = payload.getUInt8()
        serviceData.switchState = SwitchState(payload.getUInt8())
        serviceData.flagsBitmask = payload.getUInt8()
        serviceData.behaviourMasterHash = payload.getUInt16()
        payload.skip(6)
        serviceData.partialTimestamp = payload.getUInt16()
        payload.skip()
        serviceData.validation = payload.getUInt8()

        # bitmask states
        bitmaskArray = Conversion.uint8_to_bit_array(serviceData.flagsBitmask)
        
        serviceData.dimmerReady        = bitmaskArray[0]
        serviceData.dimmingAllowed     = bitmaskArray[1]
        serviceData.hasError           = bitmaskArray[2]
        serviceData.switchLocked       = bitmaskArray[3]
        serviceData.timeIsSet          = bitmaskArray[4]
        serviceData.switchCraftEnabled = bitmaskArray[5]

        serviceData.tapToToggleEnabled = bitmaskArray[6]
        serviceData.behaviourOverridden = bitmaskArray[7]

        serviceData.partialTimestamp = Conversion.uint8_array_to_uint16([data[12], data[13]])
        serviceData.uniqueIdentifier = serviceData.partialTimestamp
        
        if serviceData.timeIsSet:
            serviceData.timestamp = reconstructTimestamp(time.time(), serviceData.partialTimestamp)
        else:
            serviceData.timestamp = serviceData.partialTimestamp # this is now a counter
