

from enum import IntEnum
from typing import List


# broadcast to all:
# value: 1
#
# broadcast to all, but retry until ID's in list have acked or timeout
# value: 3
#
# 1:1 message to N crownstones with acks (only N = 1 supported for now)
# value: 2

class MeshModes(IntEnum):
    BROADCAST           = 1
    SINGLE_TARGET_ACKED = 2
    BROADCAST_ACKED_IDS = 3


class _MeshCommandPacket:

    def __init__(self, crownstoneIds : List[int], payload, mesh_command_mode: MeshModes, timeout_or_transmissions):
        self.type = 0 # reserved
        self.crownstoneIds = crownstoneIds
        self.payload = payload
        self.flags = mesh_command_mode.value
        self.timeout_or_transmissions = timeout_or_transmissions

    def getPacket(self):
        packet = []
        packet.append(self.type)
        packet.append(self.flags)
        packet.append(self.timeout_or_transmissions)
        packet.append(len(self.crownstoneIds))
        packet += self.crownstoneIds
        packet += self.payload

        return packet

class MeshBroadcastPacket(_MeshCommandPacket):

    def __init__(self, payload, number_of_transmissions : int = 0):
        """
            number_of_transmissions 0 uses the default number_of_transmissions which is 3
        """
        super().__init__([], payload, MeshModes.BROADCAST, number_of_transmissions)

class MeshSetStatePacket(_MeshCommandPacket):

    def __init__(self, crownstoneId : int, setStatePacket, timeout_seconds : int = 0 ):
        """
        timeout_seconds 0 uses the default timeout of 10 seconds
        """
        super().__init__([crownstoneId], setStatePacket, MeshModes.SINGLE_TARGET_ACKED, timeout_seconds)

class MeshBroadcastAckedPacket(_MeshCommandPacket):
    """
    This is currently only supported for type setIBeaconConfig
    """
    def __init__(self, crownstoneIds: List[int], payload, timeout_seconds : int = 0):
        """
        timeout_seconds 0 uses the default timeout of 10 seconds
        """
        super().__init__(crownstoneIds, payload, MeshModes.BROADCAST_ACKED_IDS, timeout_seconds)


class StoneMultiSwitchPacket:

    def __init__(self, crownstoneId: int, switchVal: int):
        """
        :param crownstoneId:
        :param switchVal:  percentage [0..100] or special value (SwitchValSpecial).

        """
        self.crownstoneId = crownstoneId
        self.state = switchVal


    def getPacket(self):
        packet = []
        packet.append(self.crownstoneId)
        packet.append(self.state)

        return packet


class MeshMultiSwitchPacket:

    def __init__(self, packets=None):
        if packets is None:
            packets = []
        self.packets = packets

    def getPacket(self):
        packet = []
        packet.append(len(self.packets))
        for stonePacket in self.packets:
            packet += stonePacket.getPacket()

        return packet