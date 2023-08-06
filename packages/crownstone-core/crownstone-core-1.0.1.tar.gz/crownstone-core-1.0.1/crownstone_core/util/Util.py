
# BLE specification's rules are defined in Core spec 4.2 Vol. 6 Part B Chapter 2.1.2 and are as follows:

# The initiator shall ensure that the Access Address meets the following requirements:
# • It shall not be the advertising channel packets’ Access Address.
# • It shall not have all four octets equal.
# • It shall not be a sequence that differs from the advertising channel packets’ Access Address by only one bit.
# • It shall have no more than six consecutive zeros or ones.
# • It shall have no more than 24 transitions.
# • It shall have a minimum of two transitions in the most significant six bits.
import random

from crownstone_core.util.Conversion import Conversion

ADVERTISING_ACCESS_ADDRESS = 0x8E89BED6

class Util:
    
    @staticmethod
    def generateMeshAccessAddress(retries = 0):
        randomArray = [random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        if not Util.validateMeshAccessAddress(randomArray) and retries < 100:
            retries += 1
            return Util.generateMeshAccessAddress(retries)
        
        return Conversion.uint8_array_to_uint32(randomArray)

    @staticmethod
    def validateMeshAccessAddress(randomArray):
        address = Conversion.uint8_array_to_uint32(randomArray)
        bitArray = Conversion.uint32_to_bit_array(address)
        bitArrayAdvertising = Conversion.uint32_to_bit_array(ADVERTISING_ACCESS_ADDRESS)
        
        # Requirement: It shall not be the advertising channel packets’ Access Address.
        if address == ADVERTISING_ACCESS_ADDRESS:
            # print("1")
            return False
        
        # Requirement: It shall not have all four octets equal.
        if randomArray[0] == randomArray[1] and randomArray[0] == randomArray[2] and randomArray[0] == randomArray[3]:
            # print("2")
            return False
    
        # Requirement: It shall not be a sequence that differs from the advertising channel packets’ Access Address by only one bit.
        diffCount = 0
        for idx, bit in enumerate(bitArray):
            if bit != bitArrayAdvertising[idx]:
                diffCount += 1
                
            if diffCount > 1:
                break
        
        if diffCount <= 1:
            # print("3")
            return False
        
        # Requirement: It shall have no more than six consecutive zeros or ones.
        consZero = 0
        consOne = 0
        for bit in bitArray:
            if bit:
                consOne += 1
                consZero = 0
            else:
                consZero += 1
                consOne = 0
                
            if consOne > 5 or consZero > 5:
                break
    
        if consOne > 5 or consZero > 5:
            # print("4")
            return False
    
        # Requirement: It shall have no more than 24 transitions.
        transitions = 0
        for i in range(1, len(bitArray)):
            if bitArray[i] != bitArray[i-1]:
                transitions += 1
        
        if transitions > 24:
            # print("5")
            return False
    
        # Requirement: It shall have a minimum of two transitions in the most significant six bits.
        transitions = 0
        for i in range(1, 6):
            if bitArray[i] != bitArray[i - 1]:
                transitions += 1
        
        if transitions < 2:
            # print("6")
            return False
    
        transitions = 0
        for i in range(len(bitArray)-5, len(bitArray)):
            if bitArray[i] != bitArray[i - 1]:
                transitions += 1
    
        if transitions < 2:
            # print("7")
            return False
        
        return True
