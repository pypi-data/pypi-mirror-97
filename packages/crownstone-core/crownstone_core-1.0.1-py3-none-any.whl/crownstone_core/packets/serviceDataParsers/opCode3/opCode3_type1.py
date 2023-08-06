import time

from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.Timestamp import reconstructTimestamp


def parseOpCode3_type1(serviceData, data):
    if len(data) == 16:
        # dataType = data[0]
        
        serviceData.errorMode = True
        
        serviceData.crownstoneId = data[1]
        serviceData.errorsBitmask = Conversion.uint8_array_to_uint32([
            data[2],
            data[3],
            data[4],
            data[5]
        ])
        
        serviceData.errorTimestamp = Conversion.uint8_array_to_uint32([
            data[6],
            data[7],
            data[8],
            data[9]
        ])
        
        serviceData.flagsBitmask = data[10]
        # bitmask states
        bitmaskArray = Conversion.uint8_to_bit_array(serviceData.flagsBitmask)
        
        serviceData.dimmerReady   = bitmaskArray[0]
        serviceData.dimmingAllowed     = bitmaskArray[1]
        serviceData.hasError           = bitmaskArray[2]
        serviceData.switchLocked       = bitmaskArray[3]
        serviceData.timeIsSet          = bitmaskArray[4]
        serviceData.switchCraftEnabled = bitmaskArray[5]
        
        serviceData.temperature = Conversion.uint8_to_int8(data[11])

        serviceData.partialTimestamp = Conversion.uint8_array_to_uint16([data[12], data[13]])
        serviceData.uniqueIdentifier = serviceData.partialTimestamp

        if serviceData.timeIsSet:
            serviceData.timestamp = reconstructTimestamp(time.time(), serviceData.partialTimestamp)
        else:
            serviceData.timestamp = serviceData.partialTimestamp # this is now a counter
        
        realPower = Conversion.uint16_to_int16(
            Conversion.uint8_array_to_uint16([
                data[14],
                data[15]
            ])
        )
        
        serviceData.powerUsageReal = float(realPower) / 8.0
        
        # this packet has no validation
        serviceData.validation = 0
