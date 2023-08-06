import time

from crownstone_core.util.Conversion import Conversion


def obtainTimestamp(fullTimeStamp, lsb):
	timestampBytes = Conversion.uint32_to_uint8_array(int(fullTimeStamp))
	lsbBytes = Conversion.uint16_to_uint8_array(lsb)

	restoredTimestamp = Conversion.uint8_array_to_uint32([lsbBytes[0],lsbBytes[1],timestampBytes[2],timestampBytes[3]])

	return restoredTimestamp


def reconstructTimestamp(currentTimestamp, lsbTimestamp):
	# embed location data in the timestamp
	secondsFromGMT = round(time.time() - time.mktime(time.gmtime()))
	correctedTimestamp = currentTimestamp + secondsFromGMT

	# attempt restoration
	restoredTimestamp = obtainTimestamp(correctedTimestamp, lsbTimestamp)

	halfUInt16 = 0x7FFF # roughly 9 hours in seconds

	# correct for overflows, check for drift from current time
	delta = correctedTimestamp - restoredTimestamp

	if -halfUInt16 < delta < halfUInt16:
		return restoredTimestamp
	elif delta < -halfUInt16:
		restoredTimestamp = obtainTimestamp(correctedTimestamp - 0xFFFF, lsbTimestamp)
	elif delta > halfUInt16:
		restoredTimestamp = obtainTimestamp(correctedTimestamp + 0xFFFF, lsbTimestamp)

	return restoredTimestamp

def getCorrectedLocalTimestamp(currentTimestamp):
	secondsFromGMT = round(time.time() - time.mktime(time.gmtime()))
	correctedTimestamp = currentTimestamp + secondsFromGMT
	return correctedTimestamp