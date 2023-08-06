import logging

from crownstone_core.packets.BasePacket import BasePacket
from crownstone_core.util.BufferReader import BufferReader

_LOGGER = logging.getLogger(__name__)

class UartLogHeaderPacket(BasePacket):
	"""
	UART log header packet:
	4B filename hash
	2B line number
	1B log level
	1B flags:
	- bit 0 = newLine
	"""

	def __init__(self, data = None):
		self.fileNameHash = None
		self.lineNr = None
		self.logLevel = None
		# Flags:
		self.newLine = False

		if data is not None:
			self.parse(data)

	def _parse(self, reader: BufferReader):
		self.fileNameHash = reader.getUInt32()
		self.lineNr = reader.getUInt16()
		self.logLevel = reader.getUInt8()

		flags = reader.getUInt8()
		self.newLine = (flags & (1 << 0)) != 0

	def __str__(self):
		return f"UartLogHeaderPacket(" \
		       f"fileNameHash={self.fileNameHash}, " \
		       f"lineNr={self.lineNr}, " \
		       f"logLevel={self.logLevel}, " \
		       f"newLine={self.newLine})"
