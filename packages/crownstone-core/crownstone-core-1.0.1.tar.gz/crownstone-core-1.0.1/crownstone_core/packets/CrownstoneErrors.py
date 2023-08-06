from crownstone_core.util.Conversion import Conversion


class CrownstoneErrors:
    
    def __init__(self, bitMask):
        self.bitMask = bitMask
    
        bitArray = Conversion.uint32_to_bit_array_reversed(bitMask)
    
        self.overCurrent        = bitArray[31 - 0]
        self.overCurrentDimmer  = bitArray[31 - 1]
        self.temperatureChip    = bitArray[31 - 2]
        self.temperatureDimmer  = bitArray[31 - 3]
        self.dimmerOnFailure    = bitArray[31 - 4]
        self.dimmerOffFailure   = bitArray[31 - 5]
    
    def hasErrors(self):
        return self.bitMask == 0
    
    def getDictionary(self):
        returnDict = {
            "overCurrent":        self.overCurrent,
            "overCurrentDimmer":  self.overCurrentDimmer,
            "temperatureChip":    self.temperatureChip,
            "temperatureDimmer":  self.temperatureDimmer,
            "dimmerOnFailure":    self.dimmerOnFailure,
            "dimmerOffFailure":   self.dimmerOffFailure,
            "bitMask":            self.bitMask
        }
        
        return returnDict
    