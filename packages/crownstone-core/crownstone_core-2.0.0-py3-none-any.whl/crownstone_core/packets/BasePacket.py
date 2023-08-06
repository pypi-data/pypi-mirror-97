from crownstone_core.util.BufferReader import BufferReader

class BasePacket:
	def _parse(self, reader: BufferReader):
		"""
		The function to be implemented by derived classes.
		:param reader: The data to be parsed.
		"""
		raise NotImplementedError

	def parse(self, data):
		if isinstance(data, BufferReader):
			self._parse(data)
		elif isinstance(data, list):
			reader = BufferReader(data)
			self._parse(reader)
		else:
			raise TypeError
