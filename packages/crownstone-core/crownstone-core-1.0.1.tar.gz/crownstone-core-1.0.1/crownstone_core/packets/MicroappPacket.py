from crownstone_core.util.fletcher import fletcher32_uint8Arr
import math

from crownstone_core.protocol.BluenetTypes import MicroappOpcode

# Object to be filled by the user. It contains a subset of the data required in the 
# packet, which e.g. also contains opcodes, checksum, etc.
class MicroappUploadCmd(object):
    def __init__(self, protocol, app_id, buf, chunk_size):
        self.protocol = protocol
        self.app_id = app_id
        self.buffer = buf
        self.size = len(buf)
        self.chunk_size = chunk_size

# Object to be filld by the user.
class MicroappRequestCmd(object):
    def __init__(self, protocol, app_id, buf, chunk_size):
        self.protocol = protocol
        self.app_id = app_id
        self.size = len(buf)
        self.count = math.ceil(self.size / chunk_size)
        self.chunk_size = chunk_size

# Object to be filld by the user. We need the entire buffer to calculate a checksum
class MicroappValidateCmd(object):
    def __init__(self, protocol, app_id, buf, chunk_size):
        self.protocol = protocol
        self.app_id = app_id
        self.buffer = buf 
        self.size = len(buf)
        self.chunk_size = chunk_size

# Object, convenient to be filled by the user.
class MicroappEnableCmd(object):
    def __init__(self, protocol, app_id, enable, offset):
        self.protocol = protocol
        self.app_id = app_id
        self.enable = enable
        self.param0 = offset



# All the packet fields required by the receiving Crownstone. 
class MicroappUploadPacket(object):
    def __init__(self, protocol, app_id, index, checksum, buf):
        self.protocol = protocol
        self.app_id = app_id
        self.opcode = MicroappOpcode.UPLOAD
        self.index = index
        self.checksum = checksum
        self.buffer = buf

# All the packet fields required by the receiving Crownstone. Expects a MicroappRequestCmd as input.
class MicroappRequestPacket(object):
    def __init__(self, command):
        self.protocol = command.protocol
        self.app_id = command.app_id
        self.opcode = MicroappOpcode.REQUEST
        self.size = command.size
        self.count = command.count
        self.chunk_size = command.chunk_size

# All the packet fields required by the receiving Crownstone. Expects a MicroappUploadCmd as input.
class MicroappValidatePacket(object):
    def __init__(self, command):
        self.protocol = command.protocol
        self.app_id = command.app_id
        self.opcode = MicroappOpcode.VALIDATE
        self.size = command.size
        self.checksum = 0xFF
        self.buffer = command.buffer

    def calculateChecksum(self):
        n = len(self.buffer)
        buf = bytearray(n)
        buf[0:n] = self.buffer[0:n]
        if len(buf) % 2 != 0:
            print("To check: do we make this even as well? For checksum calc")
            buf.append(0)
        self.checksum = fletcher32_uint8Arr(buf)
        print("LOG: checksum used: ", hex(self.checksum & 0xFFFF))

# All the packet fields required by the receiving Crownstone. Expects a MicroappEnableCmd as input.
class MicroappEnablePacket(object):
    def __init__(self, command):
        self.protocol = command.protocol
        self.app_id = command.app_id
        if command.enable:
            self.opcode = MicroappOpcode.ENABLE
        else:
            self.opcode = MicroappOpcode.DISABLE
        self.param0 = command.param0



class MicroappPacketInternal(object):

    def __init__(self, data):
        self.index = 0
        self.checksum = 0xCAFE
        self.count = math.ceil(data.size / data.chunk_size)
        self.chunk = bytearray(data.chunk_size)
        self.data = data
        if data.buffer:
            self.chunk[0 : data.chunk_size] = data.buffer[0 : data.chunk_size]

    def update(self):
        # if next is available, go to next index
        if (not self.nextAvailable()):
            return
        self.index += 1
        offset = self.index * self.data.chunk_size
        if (not self.last()):
            self.chunk[0 : self.data.chunk_size] = self.data.buffer[offset : offset + self.data.chunk_size]
        else:
            print("LOG: last piece")
            # Divide into remaining parts [data 0xFF]
            remaining0 = self.data.size - offset
            remaining1 = self.data.chunk_size - remaining0
            fill_buffer = bytearray([0xFF] * remaining1)
            self.chunk[0 : remaining0] = self.data.buffer[offset : offset + remaining0]
            self.chunk[remaining0 : self.data.chunk_size] = fill_buffer[0 : remaining1]
        print("LOG: size chunk is ", len(self.chunk))

    def last(self):
        offset = self.index * self.data.chunk_size
        if self.data.size > (offset + self.data.chunk_size):
            return False
        return True

    def nextAvailable(self):
        if ((self.index + 1) < self.count):
            return True
        return False

    def getPacket(self):
        self.calculateChecksum()
        packet = MicroappUploadPacket(self.data.protocol, self.data.app_id, self.index,
                self.checksum, self.chunk)
        return packet

    def calculateChecksum(self):
        # Needs padding if the default chunk can be odd-sized
        buf = bytearray(len(self.chunk))
        buf[0:len(self.chunk)] = self.chunk[0:len(self.chunk)]
        if len(buf) % 2 != 0:
            buf.append(0)
        self.checksum = fletcher32_uint8Arr(buf)
        print("LOG: checksum used: ", hex(self.checksum & 0xFFFF))
