from crownstone_core.protocol.BluenetTypes import ControlType
from crownstone_core.util.DataStepper import DataStepper


class SessionDataPacket:
    
    def __init__(self, data) :
        self.validation = ControlType.UNSPECIFIED
        self.protocol = 0
        self.sessionNonce = 0
        self.validationKey = 0
        self.valid = True

        self.payload = []
        self.load(data)
    

    def load(self, data):
        if len(data) == 16:
            payload = DataStepper(data)

            self.validation = payload.getUInt32()
            self.protocol = payload.getUInt8()
            self.sessionNonce = payload.getAmountOfBytes(5)
            self.validationKey = payload.getAmountOfBytes(4)
        else:
            self.valid = False