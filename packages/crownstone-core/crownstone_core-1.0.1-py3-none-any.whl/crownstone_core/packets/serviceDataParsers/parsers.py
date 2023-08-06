from crownstone_core.packets.serviceDataParsers.opCode3.opCode3_type0 import parseOpCode3_type0
from crownstone_core.packets.serviceDataParsers.opCode3.opCode3_type1 import parseOpCode3_type1
from crownstone_core.packets.serviceDataParsers.opCode3.opCode3_type2 import parseOpCode3_type2
from crownstone_core.packets.serviceDataParsers.opCode3.opCode3_type3 import parseOpCode3_type3
from crownstone_core.packets.serviceDataParsers.opCode4.opCode4_type0 import parseOpCode4_type0
from crownstone_core.packets.serviceDataParsers.opCode7.opCode7_type4 import parseOpCode7_type4
from crownstone_core.util.Conversion import Conversion


def parseOpCode3(serviceData, data):
    if len(data) == 16:
        serviceData.dataType = data[0]
        if serviceData.dataType == 0:
            parseOpCode3_type0(serviceData, data)
        elif serviceData.dataType == 1:
            parseOpCode3_type1(serviceData, data)
        elif serviceData.dataType == 2:
            parseOpCode3_type2(serviceData, data)
        elif serviceData.dataType == 3:
            parseOpCode3_type3(serviceData, data)
        else:
            parseOpCode3_type0(serviceData, data)






def parseOpCode4(serviceData, data):
    if len(data) == 16:
        serviceData.dataType = data[0]
        serviceData.setupMode = True
        if serviceData.dataType == 0:
            parseOpCode4_type0(serviceData, data)
        else:
            parseOpCode4_type0(serviceData, data)


def parseOpCode5(serviceData, data):
    if len(data) == 16:
        serviceData.dataType = data[0]

        if serviceData.dataType == 0:
            parseOpCode3_type0(serviceData, data)
        elif serviceData.dataType == 1:
            parseOpCode3_type1(serviceData, data)
        elif serviceData.dataType == 2:
            parseOpCode3_type2(serviceData, data)
            serviceData.rssiOfExternalCrownstone = Conversion.uint8_to_int8(data[15])
        elif serviceData.dataType == 3:
            parseOpCode3_type3(serviceData, data)
            serviceData.rssiOfExternalCrownstone = Conversion.uint8_to_int8(data[15])
        elif serviceData.dataType == 4:
            parseOpCode7_type4(serviceData, data)
        else:
            parseOpCode3_type0(serviceData, data)


def parseOpCode6(serviceData, data):
    if len(data) == 16:
        serviceData.dataType = data[0]
    
        serviceData.setupMode = True
        
        if serviceData.dataType == 0:
            parseOpCode4_type0(serviceData, data)
        else:
            parseOpCode4_type0(serviceData, data)
        


