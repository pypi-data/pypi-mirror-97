from crownstone_core.Exceptions import CrownstoneError
from crownstone_core.util.Conversion import Conversion

# TODO: rename to DataParser or so?
class DataStepper :
    """
    Class to parse a data buffer.

    It keeps up a position in the buffer, so you can do consecutive calls to get.

    Function calls will raise an exception on error.
    """
    def __init__(self, data):
        """
        Constructor

        data : list of bytes, being the buffer.
        """
        self.data = data
        self.length = len(self.data)

        self.position = 0
        self.markPosition = 0


    def getUInt8(self):
        """ Get a uint8 from the current position, and advance the position. """
        return self._request(1)[0]

    def getInt8(self):
        """ Get an int8 from the current position, and advance the position. """
        return Conversion.uint8_to_int8(self.getUInt8())

    def getUInt16(self):
        """ Get a uint16 from the current position, and advance the position. """
        return Conversion.uint8_array_to_uint16(self._request(2))

    def getInt16(self):
        """ Get an int16 from the current position, and advance the position. """
        return Conversion.uint8_array_to_int16(self._request(2))

    def getUInt32(self):
        """ Get a uint32 from the current position, and advance the position. """
        return Conversion.uint8_array_to_uint32(self._request(4))

    def getInt32(self):
        """ Get an int32 from the current position, and advance the position. """
        return Conversion.uint8_array_to_int32(self._request(4))

    def getUInt64(self):
        """ Get a uint64 from the current position, and advance the position. """
        return Conversion.uint8_array_to_uint64(self._request(8))

    def getFloat(self):
        """ Get a float from the current position, and advance the position. """
        return Conversion.uint8_array_to_float(self._request(4))

    def skip(self, count=1):
        """ Advance the position by N bytes. """
        self._request(count)

    # TODO: rename to getRawBytes() or so, now it looks as if you're getting the buffer size.
    def getAmountOfBytes(self, amount):
        """ Get N bytes of data. """
        return self._request(amount)

    def getRemainingBytes(self):
        """ Get remaining bytes of data. """
        return self._request(self.remaining())

    def mark(self):
        """ Mark the current position, so you can return to it later with reset(). """
        self.markPosition = self.position

    def reset(self):
        """ Reset the position to the last marked position. """
        self.position = self.markPosition

    def remaining(self):
        """ Return the number of bytes remaining in the buffer. """
        return self.length - self.position

    def _request(self, size):
        if self.position + size <= self.length:
            start = self.position
            self.position += size
            return self.data[start:self.position]
        else:
            raise CrownstoneError.INVALID_DATA_LENGTH




