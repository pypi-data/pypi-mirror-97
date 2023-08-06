from crownstone_core.packets.serviceDataParsers.opCode3.opCode3_type0 import parseOpCode3_type0


def parseOpCode3_type2(serviceData, data):
    if len(data) == 16:
        parseOpCode3_type0(serviceData, data)
    
        # apply differences between type 0 and type 2
        serviceData.stateOfExternalCrownstone = True
