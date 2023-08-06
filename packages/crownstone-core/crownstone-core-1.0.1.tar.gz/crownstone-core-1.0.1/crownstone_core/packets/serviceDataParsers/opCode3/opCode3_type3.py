from crownstone_core.packets.serviceDataParsers.opCode3.opCode3_type1 import parseOpCode3_type1


def parseOpCode3_type3(serviceData, data):
    if len(data) == 16:
        parseOpCode3_type1(serviceData, data)

        # apply differences between type 1 and type 4
        serviceData.stateOfExternalCrownstone = True
        serviceData.powerUsageReal = 0
        serviceData.validation = data[15]
