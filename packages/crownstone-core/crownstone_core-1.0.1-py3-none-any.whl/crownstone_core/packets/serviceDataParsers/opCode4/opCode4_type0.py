from crownstone_core.protocol.SwitchState import SwitchState
from crownstone_core.util.Conversion import Conversion

def parseOpCode4_type0(serviceData, data):
    if len(data) == 16:
        # dataType = data[0]

        serviceData.switchState  = SwitchState(data[1])
        serviceData.flagsBitmask = data[2]
        
        # bitmask states
        bitmaskArray                 = Conversion.uint8_to_bit_array(serviceData.flagsBitmask)
        serviceData.dimmerReady      = bitmaskArray[0]
        serviceData.dimmingAllowed   = bitmaskArray[1]
        serviceData.hasError         = bitmaskArray[2]
        serviceData.switchLocked     = bitmaskArray[3]
        serviceData.timeIsSet        = bitmaskArray[4]
        
        serviceData.temperature  = Conversion.uint8_to_int8(data[3])
        
        powerFactor = Conversion.uint8_to_int8(data[4])
        realPower = Conversion.uint16_to_int16(Conversion.uint8_array_to_uint16([data[5], data[6]]))

        serviceData.powerFactor = float(powerFactor) / 127.0
        
        # we cannot have a 0 for a power factor.To avoid division by 0, we set it to be either 0.01 or -0.01
        if 0 <= serviceData.powerFactor < 0.01:
            serviceData.powerFactor = 0.01
        elif -0.01 < serviceData.powerFactor < 0:
            serviceData.powerFactor = -0.01

        
        serviceData.powerUsageReal = float(realPower) / 8.0
        serviceData.powerUsageApparent = serviceData.powerUsageReal / serviceData.powerFactor
        
        serviceData.accumulatedEnergy = Conversion.uint32_to_int32(
            Conversion.uint8_array_to_uint32([
                data[7],
                data[8],
                data[9],
                data[10]
            ])
        )
        serviceData.accumulatedEnergy = serviceData.accumulatedEnergy * 64 # correction to display in J

        serviceData.uniqueIdentifier = data[11]