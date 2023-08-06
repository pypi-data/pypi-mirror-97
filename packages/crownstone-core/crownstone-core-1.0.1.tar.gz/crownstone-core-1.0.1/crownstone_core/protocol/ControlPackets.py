from crownstone_core.protocol.BlePackets import ControlPacket, FactoryResetPacket
from crownstone_core.protocol.BluenetTypes import ControlType
from crownstone_core.util.Conversion import Conversion
from crownstone_core.util.BufferFiller import BufferFiller

class ControlPacketsGenerator:

	@staticmethod
	def getFactoryResetPacket():
		return Conversion.uint32_to_uint8_array(0xdeadbeef)


	@staticmethod
	def getCommandFactoryResetPacket():
		return FactoryResetPacket().getPacket()

	@staticmethod
	def getSwitchCommandPacket(switchVal: int):
		"""
		:param switchVal: percentage [0..100] or special value (SwitchValSpecial).
		"""
		return ControlPacket(ControlType.SWITCH).loadUInt8(switchVal).getPacket()

	@staticmethod
	def getResetPacket():
		return ControlPacket(ControlType.RESET).getPacket()

	@staticmethod
	def getPutInDFUPacket():
		return ControlPacket(ControlType.GOTO_DFU).getPacket()

	@staticmethod
	def getDisconnectPacket():
		return ControlPacket(ControlType.DISCONNECT).getPacket()

	@staticmethod
	def getRelaySwitchPacket(turnOn: bool):
		"""
		:param turnOn: True to turn relay on.
		"""
		switchVal = 0
		if turnOn:
			switchVal = 1

		return ControlPacket(ControlType.RELAY).loadUInt8(switchVal).getPacket()

	@staticmethod
	def getDimmerSwitchPacket(intensity: int):
		"""
		:param intensity: percentage [0..100]
		"""
		return ControlPacket(ControlType.PWM).loadUInt8(intensity).getPacket()


	@staticmethod
	def getResetErrorPacket(errorMask):
		return ControlPacket(ControlType.RESET_ERRORS).loadUInt32(errorMask).getPacket()

	@staticmethod
	def getSetTimePacket(time):
		"""
		This is a LOCAL timestamp since epoch in seconds

		so if you live in GMT + 1 add 3600 to the timestamp
		:param time:
		:return:
		"""
		return ControlPacket(ControlType.SET_TIME).loadUInt32(time).getPacket()

	@staticmethod
	def getAllowDimmingPacket(allow: bool):
		"""

		:param allow: bool
		:return:
		"""

		allowByte = 0
		if allow:
			allowByte = 1

		return ControlPacket(ControlType.ALLOW_DIMMING).loadUInt8(allowByte).getPacket()

	@staticmethod
	def getLockSwitchPacket(lock: bool):
		"""
		:param lock: bool
		:return:
		"""

		lockByte = 0
		if lock:
			lockByte = 1

		return ControlPacket(ControlType.LOCK_SWITCH).loadUInt8(lockByte).getPacket()

	@staticmethod
	def getMicroAppUploadPacket(microapp_packet):
		"""
        :param protocol:        uint8 number
        :param app_id:          uint8 number
        :param opcode:          uint8 number
        :param index:           uint8 number
        :param checksum:        uint16 number
        :param buffer:          byteString (no conversion required)
        :return:
        """
		data = []
		data.append(microapp_packet.protocol)
		data.append(microapp_packet.app_id)
		data.append(microapp_packet.opcode)
		data.append(microapp_packet.index)
		data += Conversion.uint16_to_uint8_array(microapp_packet.checksum)
		data += list(microapp_packet.buffer)
		return ControlPacket(ControlType.MICROAPP).loadByteArray(data).getPacket()

	@staticmethod
	def getMicroAppRequestPacket(packet):
		"""
        :param protocol:        uint8 number
        :param app_id:          uint8 number
        :param opcode:          uint8 number
        :param size:            uint16 number
        :param count:           uint8 number
        :param chunk_size:      uint8 number
        :return:
        """
		data = []
		data.append(packet.protocol)
		data.append(packet.app_id)
		data.append(packet.opcode)
		data += Conversion.uint16_to_uint8_array(packet.size)
		data.append(packet.count)
		data.append(packet.chunk_size)
		return ControlPacket(ControlType.MICROAPP).loadByteArray(data).getPacket()

	@staticmethod
	def getMicroAppValidatePacket(packet):
		"""
        :param protocol:        uint8 number
        :param app_id:          uint8 number
        :param opcode:          uint8 number
        :param size:            uint16 number
        :param checksum:        uint16 number
        :return:
        """
		data = []
		data.append(packet.protocol)
		data.append(packet.app_id)
		data.append(packet.opcode)
		data += Conversion.uint16_to_uint8_array(packet.size)
		data += Conversion.uint16_to_uint8_array(packet.checksum)
		return ControlPacket(ControlType.MICROAPP).loadByteArray(data).getPacket()



	@staticmethod
	def getMicroAppEnablePacket(microapp_packet):
		"""
        :param protocol:        uint8 number
        :param app_id:          uint8 number
        :param opcode:          uint8 number
        :param param0:          uint16 number
        :return:
        """
		data = []
		data.append(microapp_packet.protocol)
		data.append(microapp_packet.app_id)
		data.append(microapp_packet.opcode)
		data += Conversion.uint16_to_uint8_array(microapp_packet.param0)
		return ControlPacket(ControlType.MICROAPP).loadByteArray(data).getPacket()

	@staticmethod
	def getSetupPacket(
		crownstoneId: int,
		sphereId: int,
		adminKey,
		memberKey,
		basicKey,
		serviceDataKey,
		localizationKey,
		meshDeviceKey,
		meshAppKey,
		meshNetworkKey,
		ibeaconUUID: str,
		ibeaconMajor: int,
		ibeaconMinor: int
	):
		"""
		:param crownstoneId:  		uint8 number
		:param sphereId:  	     	uint8 number
		:param adminKey:      		byteString (no conversion required)
		:param memberKey:     		byteString (no conversion required)
		:param basicKey:      		byteString (no conversion required)
		:param serviceDataKey: 	    byteString (no conversion required)
		:param localizationKey: 	byteString (no conversion required)
		:param meshDeviceKey: 	    byteString (no conversion required)
		:param meshAppKey: 	        byteString (no conversion required)
		:param meshNetworkKey: 	    byteString (no conversion required)
		:param ibeaconUUID: 		string  (ie. "1843423e-e175-4af0-a2e4-31e32f729a8a")
		:param ibeaconMajor:        uint16 number
		:param ibeaconMinor:        uint16 number
		:return:
		"""
		data = []
		data.append(crownstoneId)
		data.append(sphereId)

		data += list(adminKey)
		data += list(memberKey)
		data += list(basicKey)
		data += list(serviceDataKey)
		data += list(localizationKey)

		MDKey = meshDeviceKey
		if type(meshDeviceKey) is str:
			MDKey = Conversion.ascii_or_hex_string_to_16_byte_array(meshDeviceKey)

		data += list(MDKey)
		data += list(meshAppKey)
		data += list(meshNetworkKey)

		data += Conversion.ibeaconUUIDString_to_reversed_uint8_array(ibeaconUUID)
		data += Conversion.uint16_to_uint8_array(ibeaconMajor)
		data += Conversion.uint16_to_uint8_array(ibeaconMinor)

		return ControlPacket(ControlType.SETUP).loadByteArray(data).getPacket()


	@staticmethod
	def getIBeaconConfigIdPacket(id, timestamp, interval):
		data = []
		data.append(id)
		data += Conversion.uint32_to_uint8_array(timestamp)
		data += Conversion.uint16_to_uint8_array(interval)

		return ControlPacket(ControlType.SET_IBEACON_CONFIG_ID).loadByteArray(data).getPacket()

	@staticmethod
	def getPowerSamplesRequestPacket(samplesType, index):
		buffer = BufferFiller()
		buffer.putUInt8(samplesType)
		buffer.putUInt8(index)
		data = buffer.getBuffer()
		return ControlPacket(ControlType.GET_POWER_SAMPLES).loadByteArray(data).getPacket()
